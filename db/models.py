from sqlalchemy import Table, Column, Integer, String, MetaData, JSON

metadata_obj = MetaData()


users_table = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String),
    Column("password", String)
)

strategies_table = Table(
    "strategies",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer),
    Column("strategy", JSON)
)