#from queue import Empty

import argparse
from musix import Musix

import coloredlogs

if __name__ == "__main__":
    coloredlogs.install(isatty=True)
    parser = argparse.ArgumentParser(
        description="Find lyrics in musixmatch"
    )
    parser.add_argument(
        "-l",
        "--lyrics",
        help="""wellcom to musixmatch. 
                here you can search songs in english that contian specific lyrics,
                parameter need to be one word or more, with spaces and with quote.""",
        type=str,
        default="car", # This will work when running script directly from main.py
    )
    args = parser.parse_args()
    lyrics_getter = Musix(args)
    lyrics_getter.run()





