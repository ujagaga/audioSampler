#!/usr/bin/env python3

from flask import Flask, render_template, send_from_directory, make_response, request
import os
from flask_mail import Mail, Message

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__, static_url_path='/assets', static_folder='assets')

app.config.update(
    TESTING=False,
    SECRET_KEY="SomeRandomKey",
    MAIL_SERVER="Your.SMTP.server.here",
    MAIL_PORT=26,
    MAIL_USE_TLS=False,
    MAIL_USE_SSL=False,
    MAIL_USERNAME="Your@Email.here",
    MAIL_PASSWORD="YourPasswordHere",
    MAIL_DEFAULT_SENDER="Your@Email.here"
)

mail = Mail(app)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/collect', methods=['POST'])
def send_sample():
    # sample_data = request.form.get('sample_data', None)
    file = request.files['file']
    error = None
    if file:
        name = file.filename
        file_name = "{}.ogg".format(name.strip().replace(' ', '_'))

        try:
            msg = Message("Audio od korisnika: {}".format(name), recipients=["ujagaga@gmail.com"])
            msg.attach(filename=file_name, content_type="video/mpeg", data=file.read())
            mail.send(msg)

            return make_response('Audio zapis je uspešno poslat. Hvala Vam na učestvovanju.', 200)
        except Exception as e:
            print("ERROR sending email:", e)
            error = e

    else:
        error = "No file received"

    if error is not None:
        # Send error notification email
        try:
            msg = Message("Greska prilikom slanja email-a sa aplikacije Audiosampler: {}".format(e), recipients=["ujagaga@gmail.com"])
            mail.send(msg)
            return make_response('Došlo je do greške prilikom slanja zapisa. Radimo na otklanjanju. Molim Vas pokušajte sutra.', 200)
        except Exception as e2:
            print("ERROR sending email bug report:", e2)
            return make_response('Došlo je do greške prilikom slanja zapisa. Radimo na otklanjanju. Molim Vas prijavite je autoru.', 200)
    else:
        return make_response('Došlo je do greške prilikom slanja zapisa. Radimo na otklanjanju. Molim Vas prijavite je autoru.', 200)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(SCRIPT_PATH, 'assets/favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

