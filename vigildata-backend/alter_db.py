from app.database import engine
from sqlalchemy import text

with engine.begin() as con:
    con.execute(text('ALTER TABLE incidentes ADD COLUMN IF NOT EXISTS nivel_riesgo VARCHAR'))
