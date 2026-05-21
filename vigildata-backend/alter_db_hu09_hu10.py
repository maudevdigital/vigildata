"""Migracion idempotente para Sprint 3 (HU-09 y HU-10).

Agrega columnas que SQLAlchemy no agrega solo si la tabla ya existe:
  - incidentes.incidente_raiz_id (INT, FK opcional a incidentes.id)
  - incidentes.reportes_asociados (INT default 1)
  - usuarios.provider (VARCHAR default 'local')

Compatible con SQLite y PostgreSQL.
"""
from app.database import engine
from sqlalchemy import text


def _existe_columna(con, tabla: str, columna: str) -> bool:
    dialect = engine.dialect.name
    if dialect == "sqlite":
        rows = con.execute(text(f"PRAGMA table_info({tabla})")).fetchall()
        return any(r[1] == columna for r in rows)
    rows = con.execute(text(
        "SELECT 1 FROM information_schema.columns WHERE table_name=:t AND column_name=:c"
    ), {"t": tabla, "c": columna}).fetchall()
    return bool(rows)


def main():
    with engine.connect() as con:
        if not _existe_columna(con, "incidentes", "incidente_raiz_id"):
            con.execute(text("ALTER TABLE incidentes ADD COLUMN incidente_raiz_id INTEGER"))
            print("OK incidentes.incidente_raiz_id")
        if not _existe_columna(con, "incidentes", "reportes_asociados"):
            con.execute(text("ALTER TABLE incidentes ADD COLUMN reportes_asociados INTEGER DEFAULT 1"))
            print("OK incidentes.reportes_asociados")
        if not _existe_columna(con, "usuarios", "provider"):
            con.execute(text("ALTER TABLE usuarios ADD COLUMN provider VARCHAR DEFAULT 'local'"))
            print("OK usuarios.provider")
        con.commit()


if __name__ == "__main__":
    main()
