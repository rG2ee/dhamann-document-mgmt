import logging

import duckdb
import riffq

from src.alle_freelancer_rechnungen.load_csv.load_haspa_kontobewegungen import (
    load_haspa_history,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

LISTEN_ADDR = "127.0.0.1:5433"

duckdb_con: duckdb.DuckDBPyConnection | None = None


def build_duckdb() -> duckdb.DuckDBPyConnection:
    logger.info("Lade Haspa-Kontobewegungen …")
    kontobewegungen = load_haspa_history()
    logger.info(
        "  %d Zeilen, %d Spalten geladen", kontobewegungen.height, kontobewegungen.width
    )

    con = duckdb.connect()
    con.register("kontobewegungen", kontobewegungen.to_arrow())
    logger.info("DuckDB bereit – registrierte Tabellen: %s", con.execute("SHOW TABLES").fetchall())
    return con


class Connection(riffq.BaseConnection):
    def handle_auth(self, user, password, host, database=None, callback=callable):
        callback(True)

    def _handle_query(self, sql: str, callback, **kwargs):
        try:
            cur = duckdb_con.cursor()
            reader = cur.execute(sql).fetch_record_batch()
            self.send_reader(reader, callback)
        except Exception as exc:
            logger.warning("Query-Fehler: %s\n  SQL: %s", exc, sql)
            batch = self.arrow_batch(
                [("ERROR", str(exc))],
                ["status", "message"],
            )
            self.send_reader(batch, callback)

    def handle_query(self, sql, callback=callable, **kwargs):
        self.executor.submit(self._handle_query, sql, callback, **kwargs)


def main():
    global duckdb_con
    duckdb_con = build_duckdb()

    server = riffq.RiffqServer(LISTEN_ADDR, connection_cls=Connection)
    logger.info("SQL-Server läuft auf %s – verbinde dich z.B. mit:", LISTEN_ADDR)
    logger.info("  psql -h 127.0.0.1 -p 5433")
    logger.info("  oder DataGrip: PostgreSQL, Host=localhost, Port=5433")
    server.start()


if __name__ == "__main__":
    main()
