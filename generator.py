import inspect
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
from pymongo.write_concern import WriteConcern

_FIND_AND_MODIFY_DOC_FIELDS = {"value": 1}


_WriteOp = Union[InsertOne, DeleteOne, DeleteMany, ReplaceOne, UpdateOne, UpdateMany]
# Hint supports index name, "myIndex", or list of index pairs: [('x', 1), ('y', -1)]
_IndexList = Sequence[Tuple[str, Union[int, str, Mapping[str, Any]]]]
_IndexKeyHint = Union[str, _IndexList]
"""


def gen(motor_cls):
    cls = motor_cls.__delegate_class__
    cls_members: list[tuple[str, Any]] = inspect.getmembers(cls)
    cls_dict = {name: attr for name, attr in cls_members}
    filename = f'{cls.__name__.lower()}.pyi'
    has_file = False
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
                continue
            sig = None
            if isinstance(attr, metaprogramming.MotorAttributeFactory):
                is_async_method = isinstance(attr, metaprogramming.Async)
                # print(name, attr)
                original_item = cls_dict.get(name)
                if not original_item:
                    # print(name, 'not found')
                    continue
                if isinstance(original_item, property):
                    # print(name, 'is property')
                    continue
                try:
                    sig = inspect.signature(original_item)
                    with open(filename, mode='a+') as f:
                        f.write('\tasync ' if is_async_method else '\t')
                        f.write(f'def {name}(' + ', '.join([str(v) for v in sig.parameters.values()]) + ')')
                        f.write('->')
                        f.write(str(sig.return_annotation) if not inspect.isclass(sig.return_annotation) else sig.return_annotation.__name__)
                        f.write(':')
                        f.write('\n')
                        f.writelines(['\t\t...'])
                        f.write('\n')
                        f.write('\n')
                except Exception as ex:
                    print(ex)
                    print('error', name)
    if has_file:
        replacement(filename)


def replacement(filename):
    with open(filename, mode='rt') as f:
        text = f.read()
    transform_target = {
        'typing.List': 'List',
        'typing.Optional': 'Optional',
        'typing.Any': 'Any',
        'typing.MutableMapping': 'MutableMapping',
        "ForwardRef('ClientSession')": 'Optional["ClientSession"]',
        'bson.codec_options.CodecOptions': 'CodecOptions',
        'pymongo.read_preferences._ServerMode': '_ServerMode',
        'pymongo.write_concern.WriteConcern': 'WriteConcern',
        "ForwardRef('ReadConcern')": '"ReadConcern"',
        'Collection[_DocumentType]': '"Collection[_DocumentType]"',
        'Sequence[Union[pymongo.operations.InsertOne, pymongo.operations.DeleteOne, pymongo.operations.DeleteMany, pymongo.operations.ReplaceOne, pymongo.operations.UpdateOne, pymongo.operations.UpdateMany]]': 'Sequence[_WriteOp]',
        'Sequence[pymongo.operations.IndexModel]': 'IndexModel',
        "Union[Mapping[str, Any], ForwardRef('Collation'), NoneType]": 'Optional[_CollationIn]',
        'Union[str, Sequence[Tuple[str, Union[int, str, Mapping[str, Any]]]], NoneType]': 'Optional[_IndexKeyHint]',
        "Union[MutableMapping[str, Any], ForwardRef('RawBSONDocument')]": '_DocumentIn',
        'Union[Mapping[str, Any], Sequence[Mapping[str, Any]]]': 'Union[Mapping[str, Any], _Pipeline]',
        'Union[Mapping[str, Any], Iterable[str], NoneType]': 'Optional[Union[Mapping[str, Any], Iterable[str]]]',
    }
    for ori_txt, new_txt in transform_target.items():
        text = text.replace(ori_txt, new_txt)
    with open(filename, mode='wt') as f:
        f.write(text)
