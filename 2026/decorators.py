import functools
import inspect
import time
from pprint import pformat

from loguru import logger


def timer(func):
    """Log the runtime of the decorated function."""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()

        try:
            return func(*args, **kwargs)
        finally:
            run_time = time.perf_counter() - start_time
            logger.info(
                "Finished {!r} in {:.6f} secs",
                func.__qualname__,
                run_time,
            )

    return wrapper_timer


def debug(func):
    """Log the function call, arguments, return value, and exceptions."""

    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [f"{type(arg).__name__}:\n  {pformat(arg)}" for arg in args] or [
            "None"
        ]

        kwargs_repr = [f"{key}={pformat(value)}" for key, value in kwargs.items()] or [
            "None"
        ]

        frame = inspect.currentframe()

        try:
            caller_frame = frame.f_back if frame else None

            caller_name = caller_frame.f_code.co_name if caller_frame else "<unknown>"

            callers_caller_frame = caller_frame.f_back if caller_frame else None

            callers_caller_name = (
                callers_caller_frame.f_code.co_name
                if callers_caller_frame
                else "<unknown>"
            )

            logger.info(
                "{}: was called by: {}",
                caller_name,
                callers_caller_name,
            )
            logger.info(
                "{}: Calling {}",
                caller_name,
                func.__qualname__,
            )
            logger.info(
                "{}: Args:\n{}",
                func.__qualname__,
                "\n,\n".join(args_repr),
            )
            logger.info(
                "{}: Kwargs:\n{}",
                func.__qualname__,
                "\n,\n".join(kwargs_repr),
            )

            try:
                value = func(*args, **kwargs)
            except Exception:
                logger.exception(
                    "{}: raised an exception",
                    func.__qualname__,
                )
                raise

            logger.info(
                "{}: returned\n{}",
                func.__qualname__,
                pformat(value),
            )

            return value

        finally:
            # Avoid keeping frame reference cycles alive.
            del frame

    return wrapper_debug


def get_owner_class(method):
    """Return the class that owns a bound or unbound method."""

    if inspect.ismethod(method):
        cls = (
            method.__self__
            if inspect.isclass(method.__self__)
            else type(method.__self__)
        )

        for candidate in inspect.getmro(cls):
            if method.__name__ in candidate.__dict__:
                return candidate

        return None

    if inspect.isfunction(method):
        module = inspect.getmodule(method)

        if module is None:
            return None

        qualname = method.__qualname__.split(".<locals>", 1)[0]
        owner_path = qualname.split(".")[:-1]

        owner = module

        for name in owner_path:
            owner = getattr(owner, name, None)
            if owner is None:
                return None

        return owner if inspect.isclass(owner) else None

    return None
