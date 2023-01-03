from musixmatch import Musixmatch
import json
from datetime import datetime
import logging
import csv

f = open('config.json',)
configFile = json.load(f)

api_key = configFile['API_KEY']

class Musix:
    def __init__(self, args) -> None:
        self._xmusixmatch = Musixmatch(api_key)
        self._lyrics = args.lyrics
        self._logger = logging.getLogger("musixlogger")

    def generate_csv_file(self, track_list):
        try:
            """
            the parametr is: list of <Dict>
            this function create csv file from track list
            """
            self._logger.info("track list to save to csv:")
            self._logger.info(json.dumps(track_list, sort_keys=True, indent=2))

            keys = track_list[0].keys()
            now = datetime.now()
            file_name_args = "_".join( self._lyrics.split() )
            current_time = now.strftime("%H_%M_%S")
            csv_file_name = f"track_list_{current_time}_{file_name_args}.csv"
            with open(csv_file_name, 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(track_list)
            self._logger.info(f"csv file: {csv_file_name} created.")
        except KeyError:
            self._logger.info("Error on generate csv file")



    def check_albums_release_date(self, _album_data):
        """
        this function will check if album release date is prior to the date 01-01-2010 :
        rerutn True if dtae is prior
        otherwise False
        """
        album_release_date = ""
        given_date_str = configFile['DATE_LIMIT']
        
        given_date = datetime.strptime(given_date_str, "%Y-%m-%d")

        try:
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
            pass

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

        try:
            track_list =[]
            track_list_filtered = []  #list of tracks that match the conditions
            try:
                track_list = tracks_data['message']['body']['track_list']
            except KeyError:
                pass

            if(len(track_list) > 0 ):
                for track in track_list:
                    self._logger.info("====================================================================")

                    if (self.is_track_include_in_album(track)):

                        self._logger.info(F"Track name is: {track['track']['track_name']}")
                        self._logger.info("This track include in albom.")
                        self._logger.info("Check album release date ...")
                        album_id = self.get_album_id(track)
                        album_data = self._xmusixmatch.album_get(album_id)
                        is_date_prior_to_given_date = self.check_albums_release_date(album_data)
                        if(is_date_prior_to_given_date):
                            track_data =  {}
                            track_data["song_name"] = track['track']["track_name"] 
                            track_data["performer_name"] = track['track']["artist_name"]
                            track_data["album_name"] = track['track']["album_name"]
                            track_data["song_share_URL"] = track['track']["track_share_url"]

                            track_list_filtered.append(track_data)
                            self._logger.info(f"Add this track to the list...")    
                        else:
                            self._logger.info("Skipping this track ...")

                    else:
                        self._logger.info("This track is not include in album.")
            else:
                self._logger.info("There is no tracks with given lyrics.")

            return track_list_filtered
        except KeyError:
                self._logger.info("Error in filter_tracks")
    

    def run(self):
            try:
                self._logger.info(f"Lyrics argument are: {self._lyrics}")
                tracks_data = self._xmusixmatch.track_search(self._lyrics,page = 1,page_size=configFile['PAGE_SIZE'],f_lyrics_language='en')  # first function, get song list with the given lyrics
                if(tracks_data['message']['header']['status_code'] == 401):
                    self._logger.info("401 Unauthorized")
                else:
                    tracks_list_filtered = self.filter_tracks(tracks_data)

                    self._logger.info("====================================================================")
                    self._logger.info("Filtering finished, generate csv file ...")
                    self.generate_csv_file(tracks_list_filtered)
                    self._logger.info("Done.")
                    f.close()
            except KeyError:
                self._logger.info("Finish with Error")
