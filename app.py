import asyncio
import time
import logging
from sqlalchemy.future import select

from database.config import session_a, engine_a, session_b, engine_b
from models.user import User


# obtener el SEQ mas reciente de la tabla users de la base de datos 1
async def get_last_seq_db1():
    async with session_a() as session:
        async with session.begin():
            result = await session.execute(select(User).order_by(User.seq.desc()).limit(1))
            for row in result.scalars():
                return row.seq


# obtener los datos de la tabla users de la base de datos 2 que sean mayores al SEQ mas reciente de la base de datos 1
async def get_data_db2(seq):
    async with session_b() as session:
        async with session.begin():
            result = await session.execute(select(User).filter(User.seq > seq))
            return result.scalars().all()


# checar si la informacion a sincronizar no este ya en la base de datos 1
async def check_data_db1(data):
    async with session_a() as session:
        async with session.begin():
            for row in data:
                result = await session.execute(select(User).filter(User.seq == row.seq))
                if result.scalars().all():
                    return False
            return True


# insertar los datos obtenidos de la base de datos 2 en la base de datos 1
async def sync_data_db1(data):
    async with session_a() as session:
        async with session.begin():
            start = time.time()
            for row in data:
                user = User(name=row.name, fullname=row.fullname, password=row.password, seq=row.seq)
                session.add(user)
            end = time.time()
            logging.info(f"Tiempo de inserción: {round(end - start, 2)} segundos")


async def main():
    seq = await get_last_seq_db1()
    print(f"El SEQ mas reciente de la base de datos 1 es: {seq}")
    data = await get_data_db2(seq)
    if data:
        if await check_data_db1(data):
            await sync_data_db1(data)
        else:
            print('La información ya se encuentra en la base de datos 1')
    else:
        print('No hay información nueva para sincronizar')


if __name__ == "__main__":
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    # crear cron job para ejecutar la funcion main cada hora
    scheduler = AsyncIOScheduler()
    scheduler.add_job(main, 'interval', seconds=3600)
    scheduler.start()
    asyncio.get_event_loop().run_forever()