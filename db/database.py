from sqlalchemy import create_engine, text
from db.config import settings

engine = create_engine(
    url=settings.database_url,
    echo=True
)


if __name__ == "__main__":
    engine.echo = False
    with engine.connect() as conn:
        res = conn.execute(text("SELECT VERSION()"))
        print(f"{res.all()=}")