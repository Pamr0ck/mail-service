from gino import Gino

db: Gino = Gino()


async def connect_to_db(
        user: str, password: str, host: str, port: str, name: str
) -> None:
    await db.set_bind(
        f"postgresql://{user}:{password}@{host}:{port}/{name}", statement_cache_size=0, ssl=True
    )


async def disconnect_from_db() -> None:
    await db.pop_bind().close()
