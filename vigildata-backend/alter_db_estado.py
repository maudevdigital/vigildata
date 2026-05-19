from app.database import engine
from sqlalchemy import text

with engine.begin() as con:
    con.execute(text("ALTER TABLE incidentes ADD COLUMN IF NOT EXISTS estado VARCHAR NOT NULL DEFAULT 'pendiente'"))
    con.execute(text("ALTER TABLE incidentes ADD COLUMN IF NOT EXISTS revisado_por_id INTEGER REFERENCES usuarios(id)"))
    con.execute(text("ALTER TABLE incidentes ADD COLUMN IF NOT EXISTS fecha_revision TIMESTAMP WITH TIME ZONE"))
