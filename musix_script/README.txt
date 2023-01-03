hello,

here is some example for optional commands.

python main.py
python main.py -l "Hello"
python main.py -l "On fire"

If you see "401" Error, please try to replace the "API_KEY" in config.json file.
To get more result you can increase "PAGE_SIZE" value in the config.json file.



you can run also with docker file.

for example:
docker build -t mob/musix:latest .
docker run  mob/musix:latest -l "On fire".





