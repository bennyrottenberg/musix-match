#from queue import Empty
from pydantic import BaseModel
from musixmatch import Musixmatch
import json
from datetime import datetime
import logging

f = open('config.json',)
configFile = json.load(f)

api_key = configFile['API_KEY']

class MusixAPI(BaseModel):
    """Model for Musix REST API"""
    lyrics: str

class Musix:
    def __init__(self, musix_api: MusixAPI) -> None:
        self._xmusixmatch = Musixmatch(api_key)
        self._lyrics = musix_api.lyrics
        self._logger = logging.getLogger("musixlogger")

    def check_albums_release_date(self, _album_data):
        """
        this function will check if album release date is prior to the date 01-01-2010 :
        rerutn True if dtae is prior
        otherwise False
        """
        try:
            album_release_date = ""
            given_date_str = configFile['DATE_LIMIT']
            given_date = datetime.strptime(given_date_str, "%Y-%m-%d")
            album_release_date_str = _album_data['message']['body']['album']['album_release_date']

            if(album_release_date_str != None and album_release_date_str != ""):
                date_size = album_release_date_str.split('-')
                if len(date_size) == 3:
                    album_release_date = datetime.strptime(album_release_date_str, "%Y-%m-%d")
                elif (len(date_size) == 2):
                    album_release_date = datetime.strptime(album_release_date_str, "%Y-%m")
                elif (len(date_size) == 1):
                    album_release_date = datetime.strptime(album_release_date_str, "%Y")
                else:
                    album_release_date = ""
            else:
                self._logger.info("There is no data for albums_release_date datetime:")

        except KeyError:
            album_release_date = ""
            self._logger.info("No key <album_release_date> for given album")

        if(album_release_date == ""):
            return False
        if(album_release_date < given_date):
            self._logger.info(f"Albums release date: {album_release_date} prior {given_date_str}")
            return True
        self._logger.info(f"Albums release date: {album_release_date} is after {given_date_str}")    
        return False

    def get_album_id(self, _track):
        self._logger.info("get_track_id started")
        """
        this function will return album_id for given track:
        :param _track:
        :return: int
        """
        try:
            album_id = _track['track']['album_id']
            if (album_id == None or album_id <= 0):
                album_id = 0
        except KeyError:
            self._logger.info("no key <album_id> for this track")
            album_id = 0
            
        return (album_id)

    def is_track_include_in_album(self, _track):
        """
        this function will return:
        true --> if track include in album.
        false --> if track not include in album.
        Assuming that if track not include in album, there is 2 option:
        "album_id" key is not exist.
        the value of "album_id" is not grater then 0.


        :param _track:
        :return: boolean
        """
        self._logger.info("is_song_include_in_album ....")
        self._logger.info(type(_track))

        try:
            album_id = _track['track']['album_id']
            if (album_id == None or album_id <= 0):
                album_id = 0
        except KeyError:
            self._logger.info("no key <album_id> for this track")
            album_id = 0
            pass

        return (album_id != 0)

    def filter_tracks(self, tracks_data):
        """
        this function get tracks_data parameter, and filter the tracks with the given requirments.
        param Dict.
        return: list of Dict.
        """
        self._logger.info("filter_tracks started")
        try:
            track_list =[]
            track_list_filtered = {}
            track_list = tracks_data['message']['body']['track_list']
            if(len(track_list) > 0 ):
                i=0
                for track in track_list:
                    if (self.is_track_include_in_album(track)):
                        album_id = self.get_album_id(track)
                        album_data = self._xmusixmatch.album_get(album_id)
                        is_date_prior_to_given_date = self.check_albums_release_date(album_data)
                        if(is_date_prior_to_given_date):
                            track_data =  {}
                            track_data["song_name"] = track['track']["track_name"]   
                            track_data["performer_name"] = track['track']["artist_name"]
                            track_data["album_name"] = track['track']["album_name"]
                            track_data["song_share_URL"] = track['track']["track_share_url"]


                            track_list_filtered[i] = track_data
                            i = i + 1
                        else:
                            self._logger.info("is_date_prior_to_given_date is: False not adding track to rhe list")
                    else:
                        self._logger.info("is_track_include_in_album is: False not adding track to rhe list")
            else:
                self._logger.info("There is no songs with given lyrics")
            return track_list_filtered
        except KeyError:
            self._logger.info("Error on filter_tracks")

    def run(self):
        self._logger.info(f"Lyrics Are: {self._lyrics}")
        tracks_data = self._xmusixmatch.track_search(self._lyrics,page = 1,page_size=configFile['PAGE_SIZE'],f_lyrics_language='en')  # first function, get song list with the given lyrics
        if(tracks_data['message']['header']['status_code'] == 401):
            self._logger.info("401 Unauthorized")
            tracks_data["musix-info"] = "please try to replace the API_KEY in config.json file"
            return tracks_data
        tracks_list_filtered = self.filter_tracks(tracks_data)
        return tracks_list_filtered