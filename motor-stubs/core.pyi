from asyncio import Future
from typing import (
    Any,
    Iterable,
    List,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Tuple,
    Union,
    Dict,
    TypeVar,
    Callable,
    Type,
)

from bson.codec_options import CodecOptions, TypeRegistry
from bson.dbref import DBRef
from bson.timestamp import Timestamp
from pymongo.client_session import ClientSession
from pymongo.collection import Collection
from pymongo.change_stream import CollectionChangeStream
from pymongo.command_cursor import CommandCursor
from pymongo.cursor import RawBatchCursor
from pymongo.database import Database
from pymongo.operations import (
    DeleteMany,
    DeleteOne,
    IndexModel,
    InsertOne,
    ReplaceOne,
    UpdateMany,
    UpdateOne,
)
from pymongo.read_concern import ReadConcern
from pymongo.read_preferences import _ServerMode
from pymongo.results import (
    BulkWriteResult,
    DeleteResult,
    InsertManyResult,
    InsertOneResult,
    UpdateResult,
)
from pymongo.typings import _CollationIn, _DocumentIn, _DocumentType, _Pipeline
from pymongo.write_concern import WriteConcern

from motor.metaprogramming import coroutine_annotation

_FIND_AND_MODIFY_DOC_FIELDS = {"value": 1}

_WriteOp = Union[InsertOne, DeleteOne, DeleteMany, ReplaceOne, UpdateOne, UpdateMany]
# Hint supports index name, "myIndex", or list of index pairs: [('x', 1), ('y', -1)]
_IndexList = Sequence[Tuple[str, Union[int, str, Mapping[str, Any]]]]
_IndexKeyHint = Union[str, _IndexList]
_CodecDocumentType = TypeVar("_CodecDocumentType", bound=Mapping[str, Any])

T = TypeVar('T')
TCursor = TypeVar('TCursor')
TSelf = TypeVar('TSelf')

class AgnosticBase(object):
    def __init__(self, delegate: T): ...

class AgnosticBaseProperties(AgnosticBase):
    codec_options: ...
    read_preference: ...
    read_concern: ...
    write_concern: ...

class AgnosticBaseCursor(AgnosticBase):
    delegate: TCursor
    started: bool
    closed: bool
    collection: T

    address: ...
    cursor_id: ...
    alive: ...
    session: ...

    def __init__(self, cursor: TCursor, collection: T): ...
    def __aiter__(self: TSelf) -> TSelf: ...
    async def next(self) -> TCursor: ...
    async def __anext__(self) -> TCursor: ...
    @property
    @coroutine_annotation
    def fetch_next(self) -> Future[Any]: ...
    def next_object(self): ...
    def each(self, callback): ...
    @coroutine_annotation
    def to_list(self, length: int) -> Future[List]: ...
    def get_io_loop(self): ...
    async def close(self): ...
    def batch_size(self: TSelf, batch_size: int) -> TSelf: ...

class AgnosticCursor(AgnosticBaseCursor):
    def collation(self: TSelf, *args, **kwargs) -> TSelf: ...
    def add_option(self: TSelf, *args, **kwargs) -> TSelf: ...
    def remove_option(self: TSelf, *args, **kwargs) -> TSelf: ...
    def limit(self: TSelf, *args, **kwargs) -> TSelf: ...
    def skip(self: TSelf, *args, **kwargs) -> TSelf: ...
    def max_scan(self: TSelf, *args, **kwargs) -> TSelf: ...
    def sort(self: TSelf, *args, **kwargs) -> TSelf: ...
    def hint(self: TSelf, *args, **kwargs) -> TSelf: ...
    def where(self: TSelf, *args, **kwargs) -> TSelf: ...
    def max_await_time_ms(self: TSelf, *args, **kwargs) -> TSelf: ...
    def max_time_ms(self: TSelf, *args, **kwargs) -> TSelf: ...
    def min(self: TSelf, *args, **kwargs) -> TSelf: ...
    def max(self: TSelf, *args, **kwargs) -> TSelf: ...
    def comment(self: TSelf, *args, **kwargs) -> TSelf: ...
    def allow_disk_use(self: TSelf, *args, **kwargs) -> TSelf: ...
    async def distinct(self): ...
    async def explain(self): ...

class AgnosticClient(AgnosticBaseProperties):
    def __init__(
        self,
        host: Optional[Union[str, Sequence[str]]] = None,
        port: Optional[int] = None,
        document_class: Optional[Type[_DocumentType]] = None,
        tz_aware: Optional[bool] = None,
        connect: Optional[bool] = None,
        type_registry: Optional[TypeRegistry] = None,
        io_loop=None,
        **kwargs: Any,
    ): ...

class AgnosticDatabase(AgnosticBaseProperties):
    async def command(
        self,
        command: Union[str, MutableMapping[str, Any]],
        value: Any = 1,
        check: bool = True,
        allowable_errors: Optional[Sequence[Union[str, int]]] = None,
        read_preference: Optional[_ServerMode] = None,
        codec_options: 'Optional[CodecOptions[_CodecDocumentType]]' = None,
        session: Optional["ClientSession"] = None,
        comment: Optional[Any] = None,
        **kwargs: Any,
    ) -> _CodecDocumentType: ...
    async def create_collection(
        self,
        name: str,
        codec_options: Optional[CodecOptions] = None,
        read_preference: Optional[_ServerMode] = None,
        write_concern: Optional["WriteConcern"] = None,
        read_concern: Optional["ReadConcern"] = None,
        session: Optional["ClientSession"] = None,
        **kwargs: Any,
    ) -> Collection[_DocumentType]: ...
    async def dereference(
        self, dbref: DBRef, session: Optional["ClientSession"] = None, comment: Optional[Any] = None, **kwargs: Any
    ) -> Optional[_DocumentType]: ...
    async def drop_collection(
        self, name_or_collection: Union[str, Collection], session: Optional["ClientSession"] = None, comment: Optional[Any] = None
    ) -> Dict[str, Any]: ...
    def get_collection(
        self,
        name: str,
        codec_options: Optional[CodecOptions] = None,
        read_preference: Optional[_ServerMode] = None,
        write_concern: Optional["WriteConcern"] = None,
        read_concern: Optional["ReadConcern"] = None,
    ) -> Collection[_DocumentType]: ...
    async def list_collection_names(
        self, session: Optional["ClientSession"] = None, filter: Optional[Mapping[str, Any]] = None, comment: Optional[Any] = None, **kwargs: Any
    ) -> List[str]: ...
    async def list_collections(
        self, session: Optional["ClientSession"] = None, filter: Optional[Mapping[str, Any]] = None, comment: Optional[Any] = None, **kwargs: Any
    ) -> CommandCursor[Dict[str, Any]]: ...
    async def validate_collection(
        self,
        name_or_collection: Union[str, Collection],
        scandata: bool = False,
        full: bool = False,
        session: Optional["ClientSession"] = None,
        background: Optional[bool] = None,
        comment: Optional[Any] = None,
    ) -> Dict[str, Any]: ...
    def with_options(
        self,
        codec_options: Optional[CodecOptions] = None,
        read_preference: Optional[_ServerMode] = None,
        write_concern: Optional["WriteConcern"] = None,
        read_concern: Optional["ReadConcern"] = None,
    ) -> "Database[_DocumentType]": ...

class AgnosticCollection(AgnosticBaseProperties):
    name: ...
    full_name: ...
    database: AgnosticDatabase

    async def bulk_write(
        self,
        requests: Sequence[_WriteOp],
        ordered: bool = True,
        bypass_document_validation: bool = False,
        session: Optional["ClientSession"] = None,
        comment: Optional[Any] = None,
        let: Optional[Mapping] = None,
    ) -> BulkWriteResult: ...
    async def count_documents(
        self, filter: Mapping[str, Any], session: Optional["ClientSession"] = None, comment: Optional[Any] = None, **kwargs: Any
    ) -> int: ...
    async def create_index(
        self,
        keys: Union[str, Sequence[Tuple[str, Union[int, str, Mapping[str, Any]]]]],
        session: Optional["ClientSession"] = None,
        comment: Optional[Any] = None,
        **kwargs: Any,
    ) -> str: ...
    async def create_indexes(
        self, indexes: IndexModel, session: Optional["ClientSession"] = None, comment: Optional[Any] = None, **kwargs: Any
    ) -> List[str]: ...
    async def delete_many(
        self,
        filter: Mapping[str, Any],
        collation: Optional[_CollationIn] = None,
        hint: Optional[_IndexKeyHint] = None,
        session: Optional["ClientSession"] = None,
        let: Optional[Mapping[str, Any]] = None,
        comment: Optional[Any] = None,
    ) -> DeleteResult: ...
    async def delete_one(
        self,
        filter: Mapping[str, Any],
        collation: Optional[_CollationIn] = None,
        hint: Optional[_IndexKeyHint] = None,
        session: Optional["ClientSession"] = None,
        let: Optional[Mapping[str, Any]] = None,
        comment: Optional[Any] = None,
    ) -> DeleteResult: ...
    async def distinct(
        self,
        key: str,
        filter: Optional[Mapping[str, Any]] = None,
        session: Optional["ClientSession"] = None,
        comment: Optional[Any] = None,
        **kwargs: Any,
    ) -> List: ...
    async def drop(self, session: Optional["ClientSession"] = None, comment: Optional[Any] = None) -> None: ...
    async def drop_index(
        self,
        index_or_name: Union[str, Sequence[Tuple[str, Union[int, str, Mapping[str, Any]]]]],
        session: Optional["ClientSession"] = None,
        comment: Optional[Any] = None,
        **kwargs: Any,
    ) -> None: ...
    async def drop_indexes(self, session: Optional["ClientSession"] = None, comment: Optional[Any] = None, **kwargs: Any) -> None: ...
    async def estimated_document_count(self, comment: Optional[Any] = None, **kwargs: Any) -> int: ...
    async def find_one(self, filter: Optional[Any] = None, *args: Any, **kwargs: Any) -> Optional[_DocumentType]: ...
    async def find_one_and_delete(
        self,
        filter: Mapping[str, Any],
        projection: Optional[Union[Mapping[str, Any], Iterable[str]]] = None,
        sort: Optional[Sequence[Tuple[str, Union[int, str, Mapping[str, Any]]]]] = None,
        hint: Optional[_IndexKeyHint] = None,
        session: Optional["ClientSession"] = None,
        let: Optional[Mapping[str, Any]] = None,
        comment: Optional[Any] = None,
        **kwargs: Any,
    ) -> _DocumentType: ...
    async def find_one_and_replace(
        self,
        filter: Mapping[str, Any],
        replacement: Mapping[str, Any],
        projection: Optional[Union[Mapping[str, Any], Iterable[str]]] = None,
        sort: Optional[Sequence[Tuple[str, Union[int, str, Mapping[str, Any]]]]] = None,
        upsert: bool = False,
        return_document: bool = False,
        hint: Optional[_IndexKeyHint] = None,
        session: Optional["ClientSession"] = None,
        let: Optional[Mapping[str, Any]] = None,
        comment: Optional[Any] = None,
        **kwargs: Any,
    ) -> _DocumentType: ...
    async def find_one_and_update(
        self,
        filter: Mapping[str, Any],
        update: Union[Mapping[str, Any], _Pipeline],
        projection: Optional[Union[Mapping[str, Any], Iterable[str]]] = None,
        sort: Optional[Sequence[Tuple[str, Union[int, str, Mapping[str, Any]]]]] = None,
        upsert: bool = False,
        return_document: bool = False,
        array_filters: Optional[Sequence[Mapping[str, Any]]] = None,
        hint: Optional[_IndexKeyHint] = None,
        session: Optional["ClientSession"] = None,
        let: Optional[Mapping[str, Any]] = None,
        comment: Optional[Any] = None,
        **kwargs: Any,
    ) -> _DocumentType: ...
    async def index_information(self, session: Optional["ClientSession"] = None, comment: Optional[Any] = None) -> MutableMapping[str, Any]: ...
    async def insert_many(
        self,
        documents: Iterable[_DocumentIn],
        ordered: bool = True,
        bypass_document_validation: bool = False,
        session: Optional["ClientSession"] = None,
        comment: Optional[Any] = None,
    ) -> InsertManyResult: ...
    async def insert_one(
        self,
        document: _DocumentIn,
        bypass_document_validation: bool = False,
        session: Optional["ClientSession"] = None,
        comment: Optional[Any] = None,
    ) -> InsertOneResult: ...
    async def options(self, session: Optional["ClientSession"] = None, comment: Optional[Any] = None) -> MutableMapping[str, Any]: ...
    async def rename(
        self, new_name: str, session: Optional["ClientSession"] = None, comment: Optional[Any] = None, **kwargs: Any
    ) -> MutableMapping[str, Any]: ...
    async def replace_one(
        self,
        filter: Mapping[str, Any],
        replacement: Mapping[str, Any],
        upsert: bool = False,
        bypass_document_validation: bool = False,
        collation: Optional[_CollationIn] = None,
        hint: Optional[_IndexKeyHint] = None,
        session: Optional["ClientSession"] = None,
        let: Optional[Mapping[str, Any]] = None,
        comment: Optional[Any] = None,
    ) -> UpdateResult: ...
    async def update_many(
        self,
        filter: Mapping[str, Any],
        update: Union[Mapping[str, Any], _Pipeline],
        upsert: bool = False,
        array_filters: Optional[Sequence[Mapping[str, Any]]] = None,
        bypass_document_validation: Optional[bool] = None,
        collation: Optional[_CollationIn] = None,
        hint: Optional[_IndexKeyHint] = None,
        session: Optional["ClientSession"] = None,
        let: Optional[Mapping[str, Any]] = None,
        comment: Optional[Any] = None,
    ) -> UpdateResult: ...
    async def update_one(
        self,
        filter: Mapping[str, Any],
        update: Union[Mapping[str, Any], _Pipeline],
        upsert: bool = False,
        bypass_document_validation: bool = False,
        collation: Optional[_CollationIn] = None,
        array_filters: Optional[Sequence[Mapping[str, Any]]] = None,
        hint: Optional[_IndexKeyHint] = None,
        session: Optional["ClientSession"] = None,
        let: Optional[Mapping[str, Any]] = None,
        comment: Optional[Any] = None,
    ) -> UpdateResult: ...
    def with_options(
        self,
        codec_options: Optional[CodecOptions] = None,
        read_preference: Optional[_ServerMode] = None,
        write_concern: Optional[WriteConcern] = None,
        read_concern: Optional["ReadConcern"] = None,
    ) -> "Collection[_DocumentType]": ...
    async def aggregate(
        self,
        pipeline: Sequence[Mapping[str, Any]],
        session: Optional["ClientSession"] = None,
        let: Optional[Mapping[str, Any]] = None,
        comment: Optional[Any] = None,
        **kwargs: Any,
    ) -> CommandCursor[_DocumentType]: ...
    async def aggregate_raw_batches(
        self, pipeline: Sequence[Mapping[str, Any]], session: Optional["ClientSession"] = None, comment: Optional[Any] = None, **kwargs: Any
    ) -> RawBatchCursor[_DocumentType]: ...
    async def list_indexes(
        self, session: Optional["ClientSession"] = None, comment: Optional[Any] = None
    ) -> CommandCursor[MutableMapping[str, Any]]: ...
    def find(self, *args: Any, **kwargs: Any) -> AgnosticCursor[_DocumentType]: ...
    def find_raw_batches(self, *args: Any, **kwargs: Any) -> RawBatchCursor[_DocumentType]: ...
    def watch(
        self,
        pipeline: Optional[Sequence[Mapping[str, Any]]] = None,
        full_document: Optional[str] = None,
        resume_after: Optional[Mapping[str, Any]] = None,
        max_await_time_ms: Optional[int] = None,
        batch_size: Optional[int] = None,
        collation: Optional[_CollationIn] = None,
        start_at_operation_time: Optional[Timestamp] = None,
        session: Optional["ClientSession"] = None,
        start_after: Optional[Mapping[str, Any]] = None,
        comment: Optional[Any] = None,
    ) -> CollectionChangeStream[_DocumentType]: ...
