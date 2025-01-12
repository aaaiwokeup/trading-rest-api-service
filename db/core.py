from sqlalchemy import text, insert, select, delete, update
from db.database import engine
from db.models import metadata_obj, users_table, strategies_table

def create_tables():
    engine.echo = False
    metadata_obj.create_all(engine)
    engine.echo = True

if __name__ == "__main__":
    with engine.connect() as conn:
        res = conn.execute(text("SELECT VERSION()"))
        print(f"{res.all()=}")