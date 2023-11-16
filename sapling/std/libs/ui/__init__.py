from sapling.std.call_decorator import call_decorator
from sapling.objects import Int, String, Class
from .window import Window
from .label import Label
from .font import Font


class ui:
    type = 'ui'
    
    _RED = String(-1, -1, 'red')
    _GREEN = String(-1, -1, 'green')
    _BLUE = String(-1, -1, 'blue')
    _YELLOW = String(-1, -1, 'yellow')
    _CYAN = String(-1, -1, 'cyan')
    _MAGENTA = String(-1, -1, 'magenta')
    _BLACK = String(-1, -1, 'black')
    _WHITE = String(-1, -1, 'white')
    _GRAY = String(-1, -1, 'gray')
    _LIGHT_GRAY = String(-1, -1, 'light gray')
    _DARK_GRAY = String(-1, -1, 'dark gray')
    _PINK = String(-1, -1, 'pink')
    _ORANGE = String(-1, -1, 'orange')
    _BROWN = String(-1, -1, 'brown')
    _GOLD = String(-1, -1, 'gold')
    _SILVER = String(-1, -1, 'silver')
    
    
    @call_decorator({'family': {'type': 'string'}, 'size': {'type': 'int'}}, req_vm=False)
    def _font(self, family: String, size: Int) -> Class:
        return Class.from_py_cls(
            Font(family=family.value, size=size.value),
            family.line, family.column
        )
    
    @call_decorator({
        'title': {'type': 'string', 'default': (String, 'Sapling')},
        'width': {'type': 'int', 'default': (Int, 800)},
        'height': {'type': 'int', 'default': (Int, 600)}
    })
    def _create_window(self, vm, title: String, width: Int, height: Int) -> Class:
        return Class.from_py_cls(
            Window(title=title.value, width=width.value, height=height.value),
            *vm.loose_pos
        )
    
    @call_decorator({
        'parent': {'type': 'Window'},
        'width': {'type': 'int', 'default': (Int, 0)},
        'height': {'type': 'int', 'default': (Int, 28)},
        'corner_radius': {'type': 'int', 'default': (Int, 0)},
        'bg': {'type': 'string', 'default': (String, 'white')},
        'fg': {'type': 'string', 'default': (String, 'white')},
        'text_colour': {'type': 'string', 'default': (String, 'black')},
        'text': {'type': 'string', 'default': (String, '')},
        'font': {'type': 'Font', 'default': lambda ln, col: Class.from_py_cls(Font(
            'Arial', 10
        ), ln, col)},
        'compound': {'type': 'string', 'default': (String, 'center')},
        'anchor': {'type': 'string', 'default': (String, 'center')}
    })
    def _create_label(
        self,
        vm,
        parent,
        width: Int,
        height: Int,
        corner_radius: Int,
        bg: String,
        fg: String,
        text_colour: String,
        text: String,
        f: Font,
        compound: String,
        anchor: String
        ) -> Class:
        return Class.from_py_cls(
            Label(
                master=parent.python_class.w, width=width.value, height=height.value,
                corner_radius=corner_radius.value, bg_color=bg.value, fg_color=fg.value,
                text_color=text_colour.value, text=text.value, font=f.python_class.as_font(),
                compound=compound.value, anchor=anchor.value
            ), *vm.loose_pos
        )
