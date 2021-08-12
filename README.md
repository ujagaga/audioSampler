# Audio Sampler Website #

I decided to build a personal assistant software like Google assistant, Alexa,... The only way I could make it work in my native language, Serbian, was to use online services like Google Speach API.
This tends to be slow and obviosly not so private, but mainly for speed, I needed to find an offline solution. 
The best open source solution I found is VOSK:

    https://github.com/alphacep/vosk-api

but it does not support Serbian language, so I have to train it. For this I need a pool of audio recordings of more than 10 people, so I wrote a Flask website deployed on Heroky that simplifies for people to record their voice and send it to me via email. 

### How to start? ###

Install requirements. Make sure you have Python3 installed. On linux just run install_requirements.sh. On other platforms execute:

    pip install -r requirements.txt

After this just run:

    python sampler.py


## Contact ##

* [Rada Berar](ujagaga@gmail.com)






