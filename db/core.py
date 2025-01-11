from sqlalchemy import text, insert, select, delete, update
from db.database import engine
from db.models import metadata_obj, users_table, strategies_table

def create_tables():
    engine.echo = False
    metadata_obj.create_all(engine)
    engine.echo = True

def insert_data(username, password):
    with engine.connect() as conn:
        query = insert(users_table).values([{"username": username, "password": password}])
        conn.execute(query)
        conn.commit()

def exist_username(username):
    with engine.connect() as conn:
        query = select(users_table.c.username).where(users_table.c.username == username)
        result = conn.execute(query)
        exists = result.fetchone() is not None
        return exists

def get_password_by_username(username):
    with engine.connect() as conn:
        query = select(users_table.c.password).where(users_table.c.username == username)
        result = conn.execute(query)
        try:
            password = result.fetchone()[0]
            return password
        except TypeError:
            return None

def get_user_id(username):
    with engine.connect() as conn:
        query = select(users_table.c.id).where(users_table.c.username == username)
        result = conn.execute(query)
        try:
            user_id = result.fetchone()[0]
            return user_id
        except TypeError:
            return None

def insert_strategy(user_id, json):
    with engine.connect() as conn:
        query = insert(strategies_table).values(user_id=user_id, strategy=json)
        conn.execute(query)
        conn.commit()

def get_strategy(strategy_id):
    with engine.connect() as conn:
        query = select(strategies_table.c.strategy).where(strategies_table.c.id == strategy_id)
        result = conn.execute(query)
        try:
            strategy = result.fetchone()[0]
            return strategy
        except TypeError:
            return None

def del_strategy(strategy_id):
    with engine.connect() as conn:
        query = delete(strategies_table).where(strategies_table.c.id == strategy_id)
        conn.execute(query)
        conn.commit()

def up_to_date_strategy(strategy_id, updated_data):
    with engine.connect() as conn:
        query = update(strategies_table).where(strategies_table.c.id == strategy_id).values(strategy=updated_data)
        conn.execute(query)
        conn.commit()

if __name__ == "__main__":
    with engine.connect() as conn:
        res = conn.execute(text("SELECT VERSION()"))
        print(f"{res.all()=}")