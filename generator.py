import inspect
from pathlib import Path
from typing import Any

from motor import metaprogramming  # noqa


def get_import_text():
    return """
from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    Iterable,
    List,
    Mapping,
    MutableMapping,
    NoReturn,
    Optional,
    Sequence,
    Tuple,
    Union,
    Dict,
    TypeVar,
)

from bson.codec_options import CodecOptions
from bson.objectid import ObjectId
from bson.raw_bson import RawBSONDocument
from bson.son import SON
from bson.timestamp import Timestamp
from pymongo import common, helpers, message
from pymongo.aggregation import (
    _CollectionAggregationCommand,
    _CollectionRawAggregationCommand,
)
from pymongo.bulk import _Bulk
from pymongo.change_stream import CollectionChangeStream
from pymongo.collation import validate_collation_or_none
from pymongo.command_cursor import CommandCursor, RawBatchCommandCursor
from pymongo.cursor import Cursor, RawBatchCursor
from pymongo.errors import (
    ConfigurationError,
    InvalidName,
    InvalidOperation,
    OperationFailure,
)
from pymongo.helpers import _check_write_command_response
from pymongo.message import _UNICODE_REPLACE_CODEC_OPTIONS
from pymongo.operations import (
    DeleteMany,
    DeleteOne,
    IndexModel,
    InsertOne,
    ReplaceOne,
    UpdateMany,
    UpdateOne,
)
from pymongo.read_preferences import ReadPreference, _ServerMode
from pymongo.results import (
    BulkWriteResult,
    DeleteResult,
    InsertManyResult,
    InsertOneResult,
    UpdateResult,
)
from pymongo.typings import _CollationIn, _DocumentIn, _DocumentType, _Pipeline
from pymongo.client_session import ClientSession
from pymongo.mongo_client import MongoClient
from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern

from pymongo.collection import Collection
from pymongo.database import Database
from bson.dbref import DBRef
from bson.son import SON

_FIND_AND_MODIFY_DOC_FIELDS = {"value": 1}


_WriteOp = Union[InsertOne, DeleteOne, DeleteMany, ReplaceOne, UpdateOne, UpdateMany]
# Hint supports index name, "myIndex", or list of index pairs: [('x', 1), ('y', -1)]
_IndexList = Sequence[Tuple[str, Union[int, str, Mapping[str, Any]]]]
_IndexKeyHint = Union[str, _IndexList]
_CodecDocumentType = TypeVar("_CodecDocumentType", bound=Mapping[str, Any])
"""


PYI_TMP_DIR = 'pyi_tmp'


def mkdir_pyi_tmp() -> str:
    target_path = Path.cwd() / PYI_TMP_DIR
    target_path.mkdir(parents=True, exist_ok=True)
    return target_path.as_posix()


def gen(motor_cls):
    target_path = mkdir_pyi_tmp()
    cls = motor_cls.__delegate_class__
    cls_members: list[tuple[str, Any]] = inspect.getmembers(cls)
    cls_dict = {name: attr for name, attr in cls_members}
    filename = f'{target_path}/{cls.__name__.lower()}.pyi'
    has_file = False
    maybe_manually_add_members = []
    added_member = {}
    for base in reversed(inspect.getmro(motor_cls)):
        if base.__name__ != motor_cls.__name__:
            continue
        has_file = True
        with open(filename, mode='w+') as f:
            f.write(get_import_text())
            f.write('\n')
            f.write('\n')
            f.writelines([f'class {motor_cls.__name__}:'])
            f.write('\n')

        for name, attr in base.__dict__.items():
            if name.startswith('__'):
                maybe_manually_add_members.append((name, attr))
                continue
            async_prefix = '_async_'
            name = name.replace(async_prefix, '') if name.startswith(async_prefix) else name
            original_item = cls_dict.get(name)
            if not original_item:
                maybe_manually_add_members.append((name, attr))
                # print(name, 'not found')
                continue
            if isinstance(original_item, property):
                maybe_manually_add_members.append((name, attr))
                # print(name, 'is property')
                continue
            if name in added_member:
                print('pass added member:', name)
                continue
            sig = None
            is_async_method = isinstance(attr, metaprogramming.Async)
            # print(name, attr)
            sig = inspect.signature(original_item)
            with open(filename, mode='a+') as f:
                f.write('\tasync ' if is_async_method else '\t')
                f.write(f'def {name}(' + ', '.join([str(v) for v in sig.parameters.values()]) + ')')
                f.write('->')
                f.write(str(sig.return_annotation) if not inspect.isclass(sig.return_annotation) else sig.return_annotation.__name__)
                f.write(': ...')
                f.write('\n')
                f.write('\n')
            added_member[name] = True
    if has_file:
        replacement(filename)

    if maybe_manually_add_members:
        with open(filename, mode='a+') as f:
            f.write('\t# maybe manually add following func(s)\n')
            for name, attr in maybe_manually_add_members:
                f.write(f'\t# def {name}(self, ...): ...\n')


def replacement(filename):
    with open(filename, mode='rt') as f:
        text = f.read()
    transform_target = {
        'typing.List': 'List',
        'typing.Optional': 'Optional',
        'typing.Any': 'Any',
        'typing.MutableMapping': 'MutableMapping',
        'typing.Dict': 'Dict',
        'bson.dbref.DBRef': 'DBRef',
        'bson.codec_options.CodecOptions': 'CodecOptions',
        'bson.timestamp.Timestamp': 'Timestamp',
        'pymongo.read_preferences._ServerMode': '_ServerMode',
        'pymongo.write_concern.WriteConcern': 'WriteConcern',
        'pymongo.collection.Collection': 'Collection',
        'pymongo.cursor.Cursor[~_DocumentType]': 'Cursor[_DocumentType]',
        'pymongo.command_cursor.CommandCursor': 'CommandCursor',
        'pymongo.cursor.RawBatchCursor[~_DocumentType]': 'RawBatchCursor[_DocumentType]',
        'pymongo.change_stream.CollectionChangeStream': 'CollectionChangeStream',
        "ForwardRef('ClientSession')": '"ClientSession"',
        "ForwardRef('ReadConcern')": '"ReadConcern"',
        "ForwardRef('WriteConcern')": '"WriteConcern"',
        'Database[_DocumentType]': '"Database[_DocumentType]"',
        'Collection[_DocumentType]': '"Collection[_DocumentType]"',
        'Sequence[Union[pymongo.operations.InsertOne, pymongo.operations.DeleteOne, pymongo.operations.DeleteMany, pymongo.operations.ReplaceOne, pymongo.operations.UpdateOne, pymongo.operations.UpdateMany]]': 'Sequence[_WriteOp]',
        'Sequence[pymongo.operations.IndexModel]': 'IndexModel',
        "Union[Mapping[str, Any], ForwardRef('Collation'), NoneType]": 'Optional[_CollationIn]',
        'Union[str, Sequence[Tuple[str, Union[int, str, Mapping[str, Any]]]], NoneType]': 'Optional[_IndexKeyHint]',
        "Union[MutableMapping[str, Any], ForwardRef('RawBSONDocument')]": '_DocumentIn',
        'Union[Mapping[str, Any], Sequence[Mapping[str, Any]]]': 'Union[Mapping[str, Any], _Pipeline]',
        'Union[Mapping[str, Any], Iterable[str], NoneType]': 'Optional[Union[Mapping[str, Any], Iterable[str]]]',
        'Union[str, pymongo.collection.Collection]': 'Union[str, Collection]',
        '~_DocumentType': '_DocumentType',
        '~_CodecDocumentType': '_CodecDocumentType',
    }
    for ori_txt, new_txt in transform_target.items():
        text = text.replace(ori_txt, new_txt)
    with open(filename, mode='wt') as f:
        f.write(text)
