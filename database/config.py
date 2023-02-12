from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging

from settings import settings

try:

    engine_a = create_async_engine(settings.ENGINE_1, echo=True, future=True)
    engine_b = create_async_engine(settings.ENGINE_2, echo=True, future=True)
    
    # AsyncSession is a subclass of Session
    session_a = sessionmaker(engine_a, class_=AsyncSession, expire_on_commit=False)
    session_b = sessionmaker(engine_b, class_=AsyncSession, expire_on_commit=False)

    Base = declarative_base()

except Exception as e:
    logging.error(e)