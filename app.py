import os
import hmac
from hashlib import sha1

from flask import Flask, g, render_template, session, abort, request
from werkzeug.security import safe_str_cmp
import flask_sijax

import markdown
from markdown import Markdown
from markdown_checklist.extension import ChecklistExtension
from mdx_unimoji import UnimojiExtension

app = Flask(__name__)
app.secret_key = os.urandom(128)
app.config["SIJAX_STATIC_PATH"] = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')
app.config["SIJAX_JSON_URI"] = '/static/js/sijax/json2.js'
flask_sijax.Sijax(app)

@app.template_global('csrf_token')
def csrf_token():
    """
    Generate a token string from bytes arrays. The token in the session is user
    specific.
    """
    if "_csrf_token" not in session:
        session["_csrf_token"] = os.urandom(128)
    return hmac.new(app.secret_key, session["_csrf_token"],
            digestmod=sha1).hexdigest()

@app.before_request
def check_csrf_token():
    """Checks that token is correct, aborting if not"""
    if request.method in ("GET",): # not exhaustive list
        return
    token = request.form.get("csrf_token")
    if token is None:
        app.logger.warning("Expected CSRF Token: not present")
        abort(400)
    if not safe_str_cmp(token, csrf_token()):
        app.logger.warning("CSRF Token incorrect")
        abort(400)

# Setup for markdown extensions

extensions=[
    ChecklistExtension(),
    UnimojiExtension(), 
    'fenced_code', 
    'codehilite',
    'extra', 
    'tables'
    ]

# Initialize markdown object

md = Markdown(extensions=extensions)


class SijaxHandler(object):
    
    @staticmethod
    def save_message(obj_response, message):

        message = message.strip()
        if message == '':
            return obj_response.alert("Empty texts are not allowed!")

        # Save message to database or whatever..

        import time, hashlib
        time_txt = time.strftime("%H:%M:%S", time.gmtime(time.time()))
        message_id = 'message_mkdown' 

        mkd = md.convert(message)

        message = """
        <div id="%s" style="opacity: 1;">
        %s
        </div>
        """ % (message_id, mkd)

        obj_response.html('#viewMarkdown', message)

        # Clear the textbox and give it focus in case it has lost it
        # obj_response.attr('#mkdown', 'value', '')
        # obj_response.script("$('#mkdown').focus();")

        obj_response.script("$('#viewMarkdown').attr('scrollTop', $('#viewMarkdown').attr('scrollHeight'));")

        # Make the new message appear in 400ms
        obj_response.script("$('#%s').animate({opacity: 1}, 400);" % message_id)

        


    @staticmethod
    def clear_messages(obj_response):

        # Delete all messages from the database

        # Clear the messages container
        obj_response.html('#viewMarkdown', '')

        # Clear the textbox
        obj_response.attr('#mkdown', 'value', '')

        # Ensure the texbox has focus
        obj_response.script("$('#mkdown').focus();")


# views here

@flask_sijax.route(app, "/")
def home():

    # if request.method == "POST":

    #     mkd = md.convert(request.form['simplemarkdown'])

    #     return render_template('home.html', mkd=mkd)
    
    # mkd = ''

    if g.sijax.is_sijax_request:
        g.sijax.register_object(SijaxHandler)
        return g.sijax.process_request()

    return render_template('home.html')


if __name__ == '__main__':
    app.run()
