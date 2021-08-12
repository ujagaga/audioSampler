# Audio Sampler Website #

I decided to build a personal assistant software like Google assistant, Alexa,... The only way I could make it work in my native language, Serbian, was to use online services like Google Speach API.
This tends to be slow and obviosly not so private, but mainly for speed, I needed to find an offline solution. 
The best open source solution I found is VOSK:

    https://github.com/alphacep/vosk-api

but it does not support Serbian language, so I have to train it. For this I need a pool of audio recordings of more than 10 people. I wrote a Flask website deployed on [Heroky](https://audiosampler.herokuapp.com/) that simplifies for people to record their voice and send it to me via email. Unfortunatelly, this does not yet work on Android, only on desktops.

### How to start? ###

Install requirements. Make sure you have Python3 installed. On linux just run install_requirements.sh. On other platforms execute:

    pip install -r requirements.txt

After this just run:

    python sampler.py


## Using the app for another language  ##

The "language" folder contains files for specific languages. To add your own language, copy english.json and rename it to your preferance. Then alter the content to contain your own language,
In the sampler.py you will find a variable called "LOCALE". Change it to the name you gave your language file. Also take a look at other configuration variables, like email, name,...

## Contact ##

* [Rada Berar](ujagaga@gmail.com)

Feel free to use as you wish. I would appreciate if you create a pull request or at least send me the language file you write yourself, so I can add it to this repo.

