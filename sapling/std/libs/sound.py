from sapling.std.call_decorator import call_decorator
from sapling.objects import String, Class, Nil, Float
from sapling.error import STypeError

from just_playback import Playback


class Player:
    type = 'Player'
    
    def repr(self, _) -> str:
        return f'Player on \'{self.file}\''

    
    def __init__(self, file: String) -> None:
        self.file = file.value
        self.pb = Playback(self.file)
    
    
    @call_decorator()
    def _play(self, vm):
        self.pb.play()
        return Nil(*vm.loose_pos)
    
    @call_decorator()
    def _pause(self, vm):
        self.pb.pause()
        return Nil(*vm.loose_pos)
    
    @call_decorator()
    def _stop(self, vm):
        self.pb.stop()
        return Nil(*vm.loose_pos)
    
    @call_decorator()
    def _resume(self, vm):
        self.pb.resume()
        return Nil(*vm.loose_pos)

    @call_decorator({'vol': {'type': {'int', 'float'}}})
    def _volume(self, vm, v: Float):
        if 1 < v.value < 0:
            vm.error(STypeError('Volume must be between 0 and 1', v.pos))

        self.pb.set_volume(v.value)
        return Nil(*vm.loose_pos)
    
    @call_decorator()
    def _get_volume(self, vm):
        return Float(*vm.loose_pos, self.pb.volume)
    
    @call_decorator()
    def _get_duration(self, vm):
        return Float(*vm.loose_pos, self.pb.duration)


class sound:
    type = 'sound'
    
    @call_decorator({'file': {'type': 'string'}}, req_vm=False)
    def _sound(self, file: String) -> Class:
        return Class.from_py_cls(Player(file), file.line, file.column)
