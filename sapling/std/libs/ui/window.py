from sapling.std.call_decorator import call_decorator
from sapling.objects import Int, String, Nil

from customtkinter import CTk


class Window:
    __name__ = 'Window'
    type = 'Window'
    
    
    def __init__(self, **kwargs):
        self.w = CTk()
        
        self.w.title(kwargs['title'])
        self.w.geometry(f'{kwargs['width']}x{kwargs['height']}')

    
    @call_decorator({
        'widget': {},
        'x': {'type': 'int', 'default': (Int, 0)},
        'y': {'type': 'int', 'default': (Int, 0)}
    })
    def _add_widget(self, vm, widget, x: Int, y: Int) -> Nil:
        widget.python_class.w.place(x=x.value, y=y.value)
        return Nil(*vm.loose_pos)

    @call_decorator({'new': {'type': 'string'}}, req_vm=False)
    def _set_title(self, new: String) -> Nil:
        self.w.title(new.value)
        return Nil(new.line, new.column)
    
    @call_decorator({'new_width': {'type': 'int'}, 'new_height': {'type': 'int'}}, req_vm=False)
    def _set_size(self, new_width: Int, new_height: Int) -> Nil:
        self.w.geometry(f'{new_width.value}x{new_height.value}')
        return Nil(new_width.line, new_width.column)

    @call_decorator()
    def _run(self, vm) -> Nil:
        self.w.mainloop()
        return Nil(*vm.loose_pos)
