musix docker service - find songs with Lyrics.


build and run docker file

for example:
docker build -t mob/musix-api:latest .
docker run -p 9002:9002 mob/musix-api

then go to "http://<host>:9002/docs"
expand "Get Lyrics" POST.
click "try it out", insert string parameter, and click "execute",
you will see the output results below.

If you see "401" Error, please try to replace the "API_KEY" in config.json file.
To get more result you can increase "PAGE_SIZE" value in the config.json file.

thanks.
