from typing import TypeVar

from .core import AgnosticDatabase, AgnosticCollection

T = TypeVar('T')

def create_asyncio_class(cls: T) -> T: ...

AsyncIOMotorDatabase: AgnosticDatabase
AsyncIOMotorCollection: AgnosticCollection
