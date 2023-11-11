from decouple import config as envar
from flask import Flask, Blueprint, render_template
from datetime import timedelta

TIMEOUT = timedelta(hours=1)
PORT = envar("PORT", 5500)


try:
    DOMAIN = envar('DOMAIN_NAME')
except:
    DOMAIN = f"indev.lukecreated.com:{PORT}"


def createApp():
    app = Flask(__name__)
    # Encrepted with Environment Variable
    app.config['SECRET_KEY'] = envar('search', 'searchsecret')
    app.config['REMEMBER_COOKIE_SECURE'] = True
    # set session timeout (need to use with before_request() below)
    # app.config['PERMANENT_SESSION_LIFETIME'] = TIMEOUT
    app.config['TIMEZONE'] = 'Asia/Bangkok'
    app.config['SERVER_NAME'] = DOMAIN or "indev.lukecreated.com"

    from .searchbox import search
    # from .edit import edit
    app.register_blueprint(rootView, url_prefix='/dev')
    app.register_blueprint(search, url_prefix='/search')
    # app.register_blueprint(edit, url_prefix='/edit')
    # app.register_blueprint(features, url_prefix='/')
    app.register_error_handler(404, notFound)

    return app


class About():
    version = float()
    status = str()
    build = int()
    version_note = str()

    def __init__(self, version: float = float(0.0), status: str = 'None Stated', build: int = 20221100, version_note: str = "None Stated"):
        self.version = version
        self.status = status
        self.build = build
        self.version_note = version_note

    def __str__(self) -> str:
        return str("{ " + f"Version: {self.version} | Status: {self.status} | Build: {self.build} | Updates: {self.version_note}" + " }")

    def getSystemVersion(self) -> str:
        return str(self.version)


systemInfoObject = About(version=0.1, status='development',
                         build=20231111, version_note='initialized')
systemInfo = systemInfoObject.__str__()
systemVersion = systemInfoObject.getSystemVersion()

rootView = Blueprint('rootView', __name__)

@rootView.route("/root-view", methods=['GET'])
def root():
    return render_template('root.html')

# handle http 404 error
def notFound(e):
    """ not found 404 """
    return "Sorry, we don't found what you are looking for."

