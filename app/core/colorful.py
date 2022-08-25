from colorful_print import color


def colorful_dispatcher(c: str, msg, *args, **kwargs):
    dispatch = getattr(color, c)
    dispatch(msg, bold=True, *args, **kwargs)


def green(msg, *args, **kwargs):
    colorful_dispatcher('green', msg, *args, **kwargs)


def cyan(msg, *args, **kwargs):
    colorful_dispatcher('cyan', msg, *args, **kwargs)


def yellow(msg, *args, **kwargs):
    colorful_dispatcher('yellow', msg, *args, **kwargs)


def red(msg, *args, **kwargs):
    colorful_dispatcher('red', msg, *args, **kwargs)