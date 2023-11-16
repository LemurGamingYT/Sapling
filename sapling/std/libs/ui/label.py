from sapling.std.call_decorator import call_decorator
from sapling.objects import String, Nil

from customtkinter import CTkLabel


class Label:
    __name__ = 'Label'
    type = 'Label'
    
    
    def __init__(self, **kwargs):
        self.w = CTkLabel(**kwargs)
        
    
    @call_decorator({'text': {'type': 'string'}}, req_vm=False)
    def _set_text(self, text: String) -> Nil:
        self.l.configure(text=text.value)
        return Nil(text.line, text.column)
    
    @call_decorator({'bg': {'type': 'string'}}, req_vm=False)
    def _set_bg(self, bg: String) -> Nil:
        self.l.configure(bg_olor=bg.value)
        return Nil(bg.line, bg.column)
    
    @call_decorator({'fg': {'type': 'string'}}, req_vm=False)
    def _set_fg(self, fg: String) -> Nil:
        self.l.configure(fg=fg.value)
        return Nil(fg.line, fg.column)
    
    @call_decorator({'font': {'type': 'Font'}}, req_vm=False)
    def _set_font(self, font) -> Nil:
        self.l.configure(font=font.as_font())
        return Nil(font.line, font.column)
