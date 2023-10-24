from requests import Response

from sapling.objects import String, Int


class webResponse:
    __name__ = 'webResponse'
    type = 'webResponse'
    
    def repr(self, _) -> str:
        return f'webResponse(status: {self._status_code.value}, url: {self._url.value})'
    
    def __init__(self, response: Response) -> None:
        self._html = String(-1, -1, response.text)
        self._url = String(-1, -1, response.url)
        self._status_code = Int(-1, -1, response.status_code)
