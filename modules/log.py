# /*******************************************************************************
# Copyright Intel Corporation.
# This software and the related documents are Intel copyrighted materials, and your use of them
# is governed by the express license under which they were provided to you (License).
# Unless the License provides otherwise, you may not use, modify, copy, publish, distribute, disclose
# or transmit this software or the related documents without Intel's prior written permission.
# This software and the related documents are provided as is, with no express or implied warranties,
# other than those that are expressly stated in the License.
#
# *******************************************************************************/

import logging
from pathlib import Path
import inspect  # noqa: F401
from typing import Callable, Any, Optional  # noqa: F401


stream_formatter = logging.Formatter('%(levelname)s: %(message)s')
file_formatter = logging.Formatter('%(asctime)s %(process)d %(levelname)7s %(filename)s:%(lineno)d %(funcName)s | %(message)s')  # noqa: E501


def _configure_console_logging(logging_level: int) -> None:
    _default_logger = logging.getLogger("")
    for handler in _default_logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            handler.close()
            _default_logger.removeHandler(handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging_level)
    console_handler.setFormatter(stream_formatter)
    _default_logger.addHandler(console_handler)


def _configure_file_logging(logging_level: int, logging_file: Path) -> None:
    _default_logger = logging.getLogger("")
    file_handler = logging.FileHandler(filename=logging_file, mode="a")
    file_handler.setLevel(logging_level)
    file_handler.setFormatter(file_formatter)
    _default_logger.addHandler(file_handler)


def _verbosity2loglevel(verbosity: int) -> int:
    """
        Verbosity -1 -> 40 - Critical, Error
        Verbosity  0 -> 30 - Warning and above
        Verbosity  1 -> 20 - Info and above
        Verbosity  4 -> 10 - Debug and above
    """

    if verbosity < -1:
        raise ValueError("Wrong verbosity level")
    if 4 < verbosity:
        verbosity = 4
    log_num = 0
    if -1 <= verbosity <= 0:
        log_num = 30
    elif 1 <= verbosity <= 3:
        log_num = 20
    else:
        log_num = 10
    return log_num


def configure_logger(verbosity: int, logging_file: Optional[Path]) -> None:
    _default_logger = logging.getLogger("")
    logging_level = _verbosity2loglevel(verbosity)
    _default_logger.setLevel(logging_level)
    _configure_console_logging(logging_level)
    if logging_file is not None:
        _configure_file_logging(logging_level, logging_file)


_trace = """
def _is_self(func: Callable) -> bool:
    args = list(inspect.signature(func).parameters.keys())
    return len(args) > 0 and args[0] == 'self'


def _log_arguments(log_args: bool, func: Callable, args, kwargs) -> None:
    if log_args:
        # Skip "self" for methods
        offset = 1 if _is_self(func) else 0
        str_args = ', '.join([str(arg) for arg in args[offset:]])
        str_kwargs = ', '.join([f"{str(arg)}={str(value)}" for arg, value in kwargs.items()])
        if str_args and str_kwargs:
            str_arguments = str_args + ', ' + str_kwargs
        else:
            str_arguments = str_args or str_kwargs
    else:
        str_arguments = '...'
    logging.debug(f"{func.__qualname__}({str_arguments})")


def _log_ret(log_args: bool, func: Callable, ret: Any) -> None:
    if log_args:
        logging.debug(f'{func.__qualname__} returns "{str(ret)}"')
    else:
        logging.debug(f'{func.__qualname__} exit')


def make_decorate_with_parameters(decorator: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            return decorator(*args, **kwargs)
        else:
            return lambda func: decorator(func, *args, **kwargs)
    return wrapper


@make_decorate_with_parameters
def trace(func: Callable, err_msg: str = None, log_args: bool = False) -> Callable:
    def wrapper(*args, **kwargs):
        _log_arguments(log_args, func, args, kwargs)
        try:
            ret = func(*args, **kwargs)
            _log_ret(log_args, func, ret)
            return ret
        except Exception as err:
            msg = err_msg or f'{func.__qualname__} fails: {{}}'
            logging.error(msg.format(err))
            raise
    return wrapper
"""
exec(compile(_trace, logging._srcfile, "exec"))  # type: ignore
