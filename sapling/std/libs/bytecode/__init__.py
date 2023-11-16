from sapling.std.call_decorator import call_decorator
from sapling.objects import String, Class
from sapling.vmutils import get_bytecode

import sapling.codes as codes
from .nodes import *


def get_bytecode_class(node, pos: list, node_pos: list[Int, Int]):
    if isinstance(node, codes.Call):
        args = ArgsNode(*node_pos, Array(*pos, [ArgNode(*node_pos, arg) for arg in node.args]))
        
        return CallNode(
            *node_pos,
            String(*pos, node.func.value),
            args
        )


class bytecode:
    type = 'bytecode'
    
    @call_decorator({'source': {'type': 'string'}})
    def _parse(self, vm, src: String):
        bc = get_bytecode(src.value)
        
        stmts = bc.stmts
        for i, stmt in enumerate(stmts):
            stmts[i] = get_bytecode_class(
                stmt,
                vm.loose_pos,
                [
                    Int(*vm.loose_pos, vm.loose_pos[0]),
                    Int(*vm.loose_pos, vm.loose_pos[1])
                ]
            )
        
        return Class.from_py_cls(CodeNode(
            Int(*vm.loose_pos, 0),
            Int(*vm.loose_pos, 0),
            Array.from_py_iter(stmts, *vm.loose_pos)
        ), *vm.loose_pos)
