import asyncio
import time

from sqlalchemy import select

try:
    from models.user import User
except ImportError:
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from models.user import User
from database.config import session_a, engine_a, session_b, engine_b, Base


async def create_table():
    async with engine_a.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with engine_b.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def insert_data():
    time_start = time.time()
    async with session_a() as session:
        async with session.begin():
            for i in range(1, 1001):
                user = User(name=f"User {i}", fullname=f"User {i}", password=f"Password {i}", seq=i)
                session.add(user)

    async with session_b() as session:
        async with session.begin():
            for i in range(1, 2001):
                user = User(name=f"User {i}", fullname=f"User {i}", password=f"Password {i}", seq=i)
                session.add(user)
    print(f"Tiempo de inserción: {round(time.time() - time_start, 2)} segundos")


async def print_data():
    async with session_a() as session:
        async with session.begin():
            result = await session.execute(select(User))
            for row in result.scalars():
                print('session1')
                print(f"{row.id} - {row.name} - {row.fullname} - {row.password} - {row.seq}")

    async with session_b() as session:
        async with session.begin():
            result = await session.execute(select(User))
            for row in result.scalars():
                print('session2')
                print(f"{row.id} - {row.name} - {row.fullname} - {row.password} - {row.seq}")


async def main():
    await create_table()
    await insert_data()
    # await print_data()


if __name__ == "__main__":
    asyncio.run(main())
