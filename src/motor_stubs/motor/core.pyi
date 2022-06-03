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
    TypeVar,
)

from bson.codec_options import CodecOptions
from pymongo.operations import (
    DeleteMany,
    DeleteOne,
    IndexModel,
    InsertOne,
    ReplaceOne,
    UpdateMany,
    UpdateOne,
)
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

_FIND_AND_MODIFY_DOC_FIELDS = {"value": 1}

_WriteOp = Union[InsertOne, DeleteOne, DeleteMany, ReplaceOne, UpdateOne, UpdateMany]
# Hint supports index name, "myIndex", or list of index pairs: [('x', 1), ('y', -1)]
_IndexList = Sequence[Tuple[str, Union[int, str, Mapping[str, Any]]]]
_IndexKeyHint = Union[str, _IndexList]

T = TypeVar('T')

class AgnosticBase(object):
    def __init__(self, delegate: T) -> T: ...

class AgnosticBaseProperties(AgnosticBase):
    pass

class AgnosticCollection(AgnosticBaseProperties):
    async def bulk_write(
        self,
        requests: Sequence[_WriteOp],
        ordered: bool = True,
        bypass_document_validation: bool = False,
        session: Optional[Optional["ClientSession"]] = None,
        comment: Optional[Any] = None,
        let: Optional[Mapping] = None,
    ) -> BulkWriteResult: ...
    async def count_documents(
        self, filter: Mapping[str, Any], session: Optional[Optional["ClientSession"]] = None, comment: Optional[Any] = None, **kwargs: Any
    ) -> int: ...
    async def create_index(
        self,
        keys: Union[str, Sequence[Tuple[str, Union[int, str, Mapping[str, Any]]]]],
        session: Optional[Optional["ClientSession"]] = None,
        comment: Optional[Any] = None,
        **kwargs: Any,
    ) -> str: ...
    async def create_indexes(
        self, indexes: IndexModel, session: Optional[Optional["ClientSession"]] = None, comment: Optional[Any] = None, **kwargs: Any
    ) -> List[str]: ...
    async def delete_many(
        self,
        filter: Mapping[str, Any],
        collation: Optional[_CollationIn] = None,
        hint: Optional[_IndexKeyHint] = None,
        session: Optional[Optional["ClientSession"]] = None,
        let: Optional[Mapping[str, Any]] = None,
        comment: Optional[Any] = None,
    ) -> DeleteResult: ...
    async def delete_one(
        self,
        filter: Mapping[str, Any],
        collation: Optional[_CollationIn] = None,
        hint: Optional[_IndexKeyHint] = None,
        session: Optional[Optional["ClientSession"]] = None,
        let: Optional[Mapping[str, Any]] = None,
        comment: Optional[Any] = None,
    ) -> DeleteResult: ...
    async def distinct(
        self,
        key: str,
        filter: Optional[Mapping[str, Any]] = None,
        session: Optional[Optional["ClientSession"]] = None,
        comment: Optional[Any] = None,
        **kwargs: Any,
    ) -> List: ...
    async def drop(self, session: Optional[Optional["ClientSession"]] = None, comment: Optional[Any] = None) -> None: ...
    async def drop_index(
        self,
        index_or_name: Union[str, Sequence[Tuple[str, Union[int, str, Mapping[str, Any]]]]],
        session: Optional[Optional["ClientSession"]] = None,
        comment: Optional[Any] = None,
        **kwargs: Any,
    ) -> None: ...
    async def drop_indexes(self, session: Optional[Optional["ClientSession"]] = None, comment: Optional[Any] = None, **kwargs: Any) -> None: ...
    async def estimated_document_count(self, comment: Optional[Any] = None, **kwargs: Any) -> int: ...
    async def find_one(self, filter: Optional[Any] = None, *args: Any, **kwargs: Any) -> Optional[~_DocumentType]: ...
    async def find_one_and_delete(
        self,
        filter: Mapping[str, Any],
        projection: Optional[Union[Mapping[str, Any], Iterable[str]]] = None,
        sort: Optional[Sequence[Tuple[str, Union[int, str, Mapping[str, Any]]]]] = None,
        hint: Optional[_IndexKeyHint] = None,
        session: Optional[Optional["ClientSession"]] = None,
        let: Optional[Mapping[str, Any]] = None,
        comment: Optional[Any] = None,
        **kwargs: Any,
    ) -> ~_DocumentType: ...
    async def find_one_and_replace(
        self,
        filter: Mapping[str, Any],
        replacement: Mapping[str, Any],
        projection: Optional[Union[Mapping[str, Any], Iterable[str]]] = None,
        sort: Optional[Sequence[Tuple[str, Union[int, str, Mapping[str, Any]]]]] = None,
        upsert: bool = False,
        return_document: bool = False,
        hint: Optional[_IndexKeyHint] = None,
        session: Optional[Optional["ClientSession"]] = None,
        let: Optional[Mapping[str, Any]] = None,
        comment: Optional[Any] = None,
        **kwargs: Any,
    ) -> ~_DocumentType: ...
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
        session: Optional[Optional["ClientSession"]] = None,
        let: Optional[Mapping[str, Any]] = None,
        comment: Optional[Any] = None,
        **kwargs: Any,
    ) -> ~_DocumentType: ...
    async def index_information(
        self, session: Optional[Optional["ClientSession"]] = None, comment: Optional[Any] = None
    ) -> MutableMapping[str, Any]: ...
    async def insert_many(
        self,
        documents: Iterable[_DocumentIn],
        ordered: bool = True,
        bypass_document_validation: bool = False,
        session: Optional[Optional["ClientSession"]] = None,
        comment: Optional[Any] = None,
    ) -> InsertManyResult: ...
    async def insert_one(
        self,
        document: _DocumentIn,
        bypass_document_validation: bool = False,
        session: Optional[Optional["ClientSession"]] = None,
        comment: Optional[Any] = None,
    ) -> InsertOneResult: ...
    async def options(self, session: Optional[Optional["ClientSession"]] = None, comment: Optional[Any] = None) -> MutableMapping[str, Any]: ...
    async def rename(
        self, new_name: str, session: Optional[Optional["ClientSession"]] = None, comment: Optional[Any] = None, **kwargs: Any
    ) -> MutableMapping[str, Any]: ...
    async def replace_one(
        self,
        filter: Mapping[str, Any],
        replacement: Mapping[str, Any],
        upsert: bool = False,
        bypass_document_validation: bool = False,
        collation: Optional[_CollationIn] = None,
        hint: Optional[_IndexKeyHint] = None,
        session: Optional[Optional["ClientSession"]] = None,
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
        session: Optional[Optional["ClientSession"]] = None,
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
        session: Optional[Optional["ClientSession"]] = None,
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
