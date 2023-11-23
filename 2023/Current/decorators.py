import functools
import inspect
import sys
import time
from pprint import pformat

getframe_expr = "sys._getframe({}).f_code.co_name"


def timer(func):
    """Print the runtime of the decorated function"""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        # before function call
        start_time = time.perf_counter()

        value = func(*args, **kwargs)

        # after function call
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time:f} secs")
        return value

    return wrapper_timer


def debug(func):
    """Print the function signature and return value"""

    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        # before function call
        # kw/args generation
        args_repr = [f"{str(type(a))}:\n  {pformat(a)}" for a in args]
        if len(args_repr) == 0:
            args_repr.append("None")
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        if len(kwargs_repr) == 0:
            kwargs_repr.append("None")

        argstr = "\n,\n".join(args_repr)
        kwargstr = "\n,\n".join(kwargs_repr)

        # get callers of the func
        caller = eval(getframe_expr.format(2))
        callers_caller = eval(getframe_expr.format(3))

        Logger.info(f"{caller}: was called by: {callers_caller}")
        Logger.info(f"{caller}: Calling {func.__name__},")
        Logger.info(f"{func.__name__}: Args:\n {argstr}")
        Logger.info(f"{func.__name__}: Kwargs:\n {kwargstr}")

        value = func(*args, **kwargs)

        # after function call
        Logger.info(f"{func.__name__}: returned\n {pformat(value)!s}")
        return value

    return wrapper_debug


def get_owner_class(meth):
    for cls in inspect.getmro(meth.im_class):
        if meth.__name__ in cls.__dict__:
            return cls
    return None
