from typing import TypeVar

from .core import AgnosticCollection

T = TypeVar('T')

def create_asyncio_class(cls: T) -> T: ...

AsyncIOMotorCollection: AgnosticCollection
