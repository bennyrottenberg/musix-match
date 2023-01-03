import requests

class Musixmatch(object):
    def __init__(self, apikey: str) -> None:
        self.__apikey = apikey
        self.__url = "http://api.musixmatch.com/ws/1.1/"

    def _get_url(self, url: str) -> str:
        return f"{self.__url}{url}&apikey={self.__apikey}"

    def _apikey(self) -> str:
        return self.__apikey

    def _request(self, url: str) -> dict:
        request = requests.get(url)
        return request.json()

    def track_search(self, q_lyrics, page, page_size, f_lyrics_language, _format="json",):
        
        data = self._request(
            self._get_url(
                "track.search?"
                "format={}"
                "&callback={}"
                "&q_lyrics={}"
                "&page={}"
                "&page_size={}"
                "&f_lyrics_language={}"
                .format(
                    _format,
                    "_callback",
                    q_lyrics,
                    page,
                    page_size,
                    f_lyrics_language, 
                ),
            ),
        )
        return data

    def album_get(self, album_id, _format="json"):
        data = self._request(
            self._get_url("album.get?album_id={}&format={}".format(album_id, _format)),
        )
        return data
