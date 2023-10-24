from sapling.std.call_decorator import call_decorator
from sapling.objects import String


class bytecode:
    type = 'bytecode'
    
    @call_decorator({'source': {'type': 'string'}}, req_vm=False)
    def _parse(self, _: String):
        from main import get_file_bytecode
