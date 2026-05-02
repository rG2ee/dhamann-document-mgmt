import logging
import sys

import polars as pl
import pyarrow as pa
import riffq

from src.alle_freelancer_rechnungen.load_csv.load_haspa_kontobewegungen import (
    load_haspa_history,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

LISTEN_ADDR = "127.0.0.1:5433"

ctx: pl.SQLContext | None = None


def build_context() -> pl.SQLContext:
    logger.info("Lade Haspa-Kontobewegungen …")
    kontobewegungen = load_haspa_history()
    logger.info(
        "  %d Zeilen, %d Spalten geladen", kontobewegungen.height, kontobewegungen.width
    )

    sql_ctx = pl.SQLContext(kontobewegungen=kontobewegungen.lazy(), eager=False)
    logger.info("SQLContext bereit – registrierte Tabellen: %s", sql_ctx.tables())
    return sql_ctx


class Connection(riffq.BaseConnection):
    def handle_auth(self, user, password, host, database=None, callback=callable):
        callback(True)

    def _handle_query(self, sql: str, callback, **kwargs):
        sql_stripped = sql.strip().rstrip(";")

        try:
            result_lf = ctx.execute(sql_stripped)
            result_df = result_lf.collect()
            arrow_table = result_df.to_arrow()
            reader = pa.RecordBatchReader.from_batches(
                arrow_table.schema, arrow_table.to_batches() or [pa.record_batch([], schema=arrow_table.schema)]
            )
            self.send_reader(reader, callback)
        except Exception as exc:
            logger.warning("Query-Fehler: %s\n  SQL: %s", exc, sql_stripped)
            batch = self.arrow_batch(
                [pa.array(["ERROR"]), pa.array([str(exc)])],
                ["status", "message"],
            )
            self.send_reader(batch, callback)

    def handle_query(self, sql, callback=callable, **kwargs):
        self.executor.submit(self._handle_query, sql, callback, **kwargs)


def main():
    global ctx
    ctx = build_context()

    server = riffq.RiffqServer(LISTEN_ADDR, connection_cls=Connection)
    logger.info("SQL-Server läuft auf %s – verbinde dich z.B. mit:", LISTEN_ADDR)
    logger.info("  psql -h 127.0.0.1 -p 5433")
    logger.info("  oder DataGrip: PostgreSQL, Host=localhost, Port=5433")
    server.start()


if __name__ == "__main__":
    main()
