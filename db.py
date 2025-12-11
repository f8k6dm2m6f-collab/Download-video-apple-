from sqlalchemy import create_engine, Column, String, Table, MetaData
from config import config

engine = create_engine(f"sqlite:///{config.DB_PATH}")
metadata = MetaData()

downloads = Table(
    "downloads",
    metadata,
    Column("url", String, primary_key=True)
)

metadata.create_all(engine)

def is_downloaded(url: str) -> bool:
    with engine.connect() as conn:
        result = conn.execute(downloads.select().where(downloads.c.url == url)).fetchone()
        return result is not None

def add_download(url: str):
    with engine.connect() as conn:
        conn.execute(downloads.insert().values(url=url))
