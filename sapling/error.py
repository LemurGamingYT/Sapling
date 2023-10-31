"""
error.py
--------

Contains the error classes used by the Sapling VM
All errors inherit from the SError (Sapling Error) class

"""


from sys import exit as sys_exit


class SError:
    """Base Sapling error class"""

    def as_string(self) -> str:
        """Unused by the Virtual Machine

        Returns:
            str: The representation of the error as a string
        """

        return 'SError()'

    def report(self):
        """The report error method
        anything the error does should be here"""

        print('An unidentified error has occurred')
        sys_exit(1)


class SFileError(SError):
    """The file error class used when a file is not found"""
    
    def __init__(self, path: str, pos: list):
        self.path = path
        
        self.pos = pos
    
    def report(self):
        print(f'FileError: File does not exist \'{self.path}\'')
        sys_exit(1)


class STypeError(SError):
    """The type error class used when the current code is expecting a certain type
    but the current type is not"""

    def __init__(self, msg: str, pos: list):
        self.msg = msg

        self.pos = pos

    def report(self):
        print(f'TypeError: {self.msg}')
        sys_exit(1)


class SIndexError(SError):
    """The index error class used when an index is out of range or a key is not found"""

    def __init__(self, msg: str, pos: list):
        self.msg = msg

        self.pos = pos

    def report(self):
        print(f'IndexError: {self.msg}')
        sys_exit(1)


class SImportError(SError):
    """The import error class used when a library is not found or is invalid"""

    def __init__(self, lib_name: str, pos: list) -> None:
        self.lib_name = lib_name

        self.pos = pos

    def report(self):
        print(f'ImportError: {self.lib_name} library not found')
        sys_exit(1)


class SAttributeError(SError):
    """The attribute error class used when an object has been given an attribute that
    doesn't exist"""

    def __init__(self, obj_type: str, attr: str, pos: list):
        self.obj_type = obj_type
        self.attr = attr

        self.pos = pos

    def report(self):
        print(f'AttributeError: \'{self.obj_type}\' type has no attribute \'{self.attr}\'')
        sys_exit(1)


class SNameError(SError):
    """The name error class used when an object (e.g. variable or function) is not defined
    in the environment"""

    def __init__(self, name: str, pos: list):
        self.name = name

        self.pos = pos

    def report(self):
        print(f'NameError: \'{self.name}\' is not defined')
        sys_exit(1)


class SRuntimeError(SError):
    """The runtime error class used when an error occurs during runtime and the
    error type cannot be inferred"""

    def __init__(self, msg: str, pos: list):
        self.msg = msg

        self.pos = pos

    def report(self):
        print(f'RuntimeError: {self.msg}')
        sys_exit(1)
