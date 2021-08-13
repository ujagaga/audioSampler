#!/usr/bin/env python3

from flask import Flask, render_template, send_from_directory, make_response, request
from flask_mail import Mail, Message
import json
import os
from flask_sslify import SSLify

# Change this to False to switch to production mode and force https
ALLOW_HTTP = True

app = Flask(__name__, static_url_path='/assets', static_folder='assets')

app.config.update(
    TESTING=False,
    SECRET_KEY="SomeRandomKey123",
    MAIL_SERVER="Your.SMTP.server.here",
    MAIL_PORT=26,
    MAIL_USE_TLS=False,
    MAIL_USE_SSL=False,
    MAIL_USERNAME="Your@Email.here",
    MAIL_PASSWORD="YourPasswordHere",
    MAIL_DEFAULT_SENDER="Your@Email.here"
)
ADMIN_EMAIL = "ujagaga@gmail.com"
ADMIN_NAME = "Rada Berar"
mail = Mail(app)

LOCALE = 'english'
LANGUAGE = {}

# When testing locally comment this out as it will force https which will fail on localhost
sslify = SSLify(app)


def load_language():
    global LANGUAGE

    lang_dir = 'language'
    lang_file = os.path.join(lang_dir, LOCALE + ".json")

    if not os.path.isdir(lang_dir):
        os.mkdir(lang_dir)

    if not os.path.isfile(lang_file):
        with open(lang_file, 'w') as f:
            data = json.dumps(LANGUAGE)
            f.write(data.replace('{', '{\n').replace('}', '\n}').replace(',', ',\n'))

    try:
        f = open(lang_file, 'r')
        raw_data = f.read()
        f.close()

        LANGUAGE = json.loads(raw_data)
    except Exception as e:
        print("ERROR parsing language", e)


@app.route('/', methods=['GET'])
def home():
    load_language()
    return render_template('index.html', lang=LANGUAGE, admin_email=ADMIN_EMAIL, admin_name=ADMIN_NAME)


@app.route('/collect', methods=['POST'])
def send_sample():
    load_language()
    file = request.files['file']
    error = None
    if file:
        name = file.filename
        file_name = "{}.ogg".format(name.strip().replace(' ', '_'))

        try:
            msg = Message("{}: {}".format(LANGUAGE["audio_received"], name), recipients=[ADMIN_EMAIL])
            msg.attach(filename=file_name, content_type="video/mpeg", data=file.read())
            mail.send(msg)

            return make_response(LANGUAGE["thank_you_msg"], 200)
        except Exception as e:
            print("ERROR sending email:", e)
            error = e

    else:
        error = "No file received"

    if error is not None:
        # Send error notification email to admin
        try:
            msg = Message("ERROR in sending sample: {}".format(e), recipients=[ADMIN_EMAIL])
            mail.send(msg)
            return make_response(LANGUAGE["error_1"], 200)
        except Exception as e2:
            print("ERROR sending email bug report:", e2)
            return make_response(LANGUAGE["error_2"], 200)
    else:
        return make_response(LANGUAGE["error_2"], 200)


@app.route('/favicon.ico')
def favicon():
    script_path = os.path.dirname(os.path.realpath(__file__))
    return send_from_directory(script_path, 'assets/favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=ALLOW_HTTP)

