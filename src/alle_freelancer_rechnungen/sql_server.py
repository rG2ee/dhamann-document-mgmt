import logging
import re

import duckdb
import pyarrow as pa
import riffq

from alle_freelancer_rechnungen.process_kimai_haspa.process_haspa import process_haspa
from alle_freelancer_rechnungen.process_kimai_haspa.process_kimai import process_kimai
from alle_freelancer_rechnungen.rechnung_constants.process_constants import process_rechnungen_constants

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

LISTEN_ADDR = "127.0.0.1:5433"

duckdb_con: duckdb.DuckDBPyConnection | None = None

_PG_SET_RE = re.compile(r"^\s*set\s+", re.IGNORECASE)
_PG_SHOW_RE = re.compile(r"^\s*show\s+", re.IGNORECASE)


def _is_pg_compat_noise(sql: str) -> bool:
    """DataGrip/psql send PG-specific SET/SHOW commands that DuckDB doesn't support."""
    return bool(_PG_SET_RE.match(sql) or _PG_SHOW_RE.match(sql))


def build_duckdb() -> duckdb.DuckDBPyConnection:
    logger.info("Lade Haspa-Kontobewegungen …")
    kontobewegungen = process_haspa()
    logger.info(
        "  %d Zeilen, %d Spalten geladen", kontobewegungen.height, kontobewegungen.width
    )

    con = duckdb.connect()
    arrow_table = kontobewegungen.to_arrow()
    con.register("_raw", arrow_table)
    varchar_cols = [f.name for f in arrow_table.schema if pa.types.is_string(f.type) or pa.types.is_large_string(f.type)]
    select_exprs = [
        f'LOWER("{col}") AS "{col}"' if col in varchar_cols else f'"{col}"'
        for col in arrow_table.schema.names
    ]
    con.execute(f"CREATE TABLE kontobewegungen AS SELECT {', '.join(select_exprs)} FROM _raw")
    con.execute("DROP VIEW _raw")

    logger.info("Lade Kimai-Rechnungen …")
    kimai_rechnungen = process_kimai()
    logger.info(
        "  %d Zeilen, %d Spalten geladen (Kimai)", kimai_rechnungen.height, kimai_rechnungen.width
    )
    arrow_kimai = kimai_rechnungen.to_arrow()
    con.register("_raw_kimai", arrow_kimai)
    varchar_cols_kimai = [f.name for f in arrow_kimai.schema if pa.types.is_string(f.type) or pa.types.is_large_string(f.type)]
    select_exprs_kimai = [
        f'LOWER("{col}") AS "{col}"' if col in varchar_cols_kimai else f'"{col}"'
        for col in arrow_kimai.schema.names
    ]
    con.execute(f"CREATE TABLE kimai_rechnungen AS SELECT {', '.join(select_exprs_kimai)} FROM _raw_kimai")
    con.execute("DROP VIEW _raw_kimai")

    logger.info("Lade Rechnungs-Konstanten …")
    rechnungen_constants = process_rechnungen_constants()
    logger.info(
        "  %d Zeilen, %d Spalten geladen (Konstanten)", rechnungen_constants.height, rechnungen_constants.width
    )
    arrow_constants = rechnungen_constants.to_arrow()
    con.register("_raw_constants", arrow_constants)
    varchar_cols_constants = [f.name for f in arrow_constants.schema if pa.types.is_string(f.type) or pa.types.is_large_string(f.type)]
    select_exprs_constants = [
        f'LOWER("{col}") AS "{col}"' if col in varchar_cols_constants else f'"{col}"'
        for col in arrow_constants.schema.names
    ]
    con.execute(f"CREATE TABLE rechnungen_constants AS SELECT {', '.join(select_exprs_constants)} FROM _raw_constants")
    con.execute("DROP VIEW _raw_constants")

    logger.info("DuckDB bereit – registrierte Tabellen: %s", con.execute("SHOW TABLES").fetchall())
    return con


class Connection(riffq.BaseConnection):
    def handle_auth(self, user, password, host, database=None, callback=callable):
        callback(True)

    def _handle_query(self, sql: str, callback, **kwargs):
        sql_stripped = sql.strip()

        if not sql_stripped:
            batch = self.arrow_batch(
                [pa.array(["OK"]), pa.array(["empty query"])],
                ["status", "message"],
            )
            self.send_reader(batch, callback)
            return

        if _is_pg_compat_noise(sql_stripped):
            batch = self.arrow_batch(
                [pa.array(["OK"]), pa.array([sql_stripped])],
                ["status", "message"],
            )
            self.send_reader(batch, callback)
            return

        try:
            cur = duckdb_con.cursor()
            result = cur.execute(sql_stripped)
            reader = result.fetch_record_batch()
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
    global duckdb_con
    duckdb_con = build_duckdb()

    server = riffq.RiffqServer(LISTEN_ADDR, connection_cls=Connection)
    logger.info("SQL-Server läuft auf %s – verbinde dich z.B. mit:", LISTEN_ADDR)
    logger.info("  psql -h 127.0.0.1 -p 5433")
    logger.info("  oder DataGrip: PostgreSQL, Host=localhost, Port=5433")
    server.start()


if __name__ == "__main__":
    main()
