class Font:
    type = 'Font'
    
    
    __slots__ = ('family', 'size')
    
    
    def __init__(self, family: str, size: int):
        self.family = family
        self.size = size
    
    def as_font(self) -> tuple:
        return self.family, self.size
