from typing import TypeVar, Union, Callable
import inspect
_T = TypeVar("_T")

_args: tuple
_instance: "Handler"
_pkg_name: str


def remote_call(*args):
    args = args or _args
    _instance.send_data(_pkg_name, *args)


class Handler:
    def __init__(self):
        self.handlers: dict[str, BoundPackage] = {}

    def clear_handlers(self):
        self.handlers.clear()

    def send_data(self, pkg_name, *args):
        ...

    def recv_data(self):
        ...


class Package:
    pkg_handler: Callable
    parameters: list[inspect.Parameter]

    def __init__(self, func):
        self.func = func
        self.name = func.__name__

    def handler(self, pkg_handler):
        self.pkg_handler = pkg_handler
        self.parameters = list(inspect.signature(pkg_handler).parameters.values())
        self.parameters.pop(0)  # self

    def __get__(self, instance, owner):
        return BoundPackage(instance, self)


in_client = Package
in_server = Package


class BoundPackage:
    def __init__(self, instance: Handler, package: Package):
        self.package = package
        self.instance = instance

    def __call__(self, *args, **kwargs):
        global _args, _instance, _pkg_name
        if self.instance:
            _instance = self.instance
        else:
            _instance = args[0]
            args = args[1:]
        _args = args
        _pkg_name = self.package.name
        self.package.func(_instance, *args, **kwargs)

    def handle(self, *args):
        self.package.pkg_handler(self.instance, *args)

    @property
    def parameters(self) -> list[inspect.Parameter]:
        return self.package.parameters

    def enable(self):
        self.instance.handlers[self.package.name] = self

    def disable(self):
        self.instance.handlers.pop(self.package.name, None)
