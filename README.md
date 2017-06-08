# webstats

A simple web aplication that shows server's GPU, CPU and memory load on the browser. On the server side, you need to install `sysstat`:

```
sudo apt-get install sysstat
```

The code will perform commands like. More info [here](http://www.thegeekstuff.com/2011/03/sar-examples/?utm_source=feedburner):

```
uname -a
sar -P ALL 1 1
nvidia-smi
sar -r 1 1
```

and will present the results as a dynamically generated web page.

## Running the CGI version using python server

In order to run the server you may:

```
python3 -m http.server --bind localhost --cgi 8000
```

remember that the CGI must be in a directory called `/cgi-bin`. This is relative to where you have started the server, which becomes the new `/` even if you have started the server in `/home/<USER>`

Then you can call the script like this in a browser:

```
http://localhost:8000/cgi-bin/webstats.py
```

## Running the flask version using systemd

This is the more elegant way, using gunicorn und nginx. Please follow the instructions on this [gist](https://gist.github.com/xaratustrah/0e648a0dca74c661c1a1c78acbd5e224). ).
