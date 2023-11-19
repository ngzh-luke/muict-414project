from decouple import config as envar
from flask import Flask, Blueprint, render_template, request, redirect, url_for
from elasticsearch import Elasticsearch

PORT = envar("PORT", 5500)

# ASSIGN your password this line
ELASTIC_PASSWORD = envar("ELASTIC_PASSWORD", "password")

es = Elasticsearch("https://localhost:9200",
                   http_auth=("elastic", ELASTIC_PASSWORD), verify_certs=False)

try:
    DOMAIN = envar('DOMAIN_NAME')
except:
    DOMAIN = f"127.0.0.1:{PORT}"


def createApp():
    app = Flask(__name__)
    # Encrepted with Environment Variable
    app.config['SECRET_KEY'] = envar('search', 'searchsecret')
    app.config['REMEMBER_COOKIE_SECURE'] = True
    app.config['TIMEZONE'] = 'Asia/Bangkok'
    app.config['SERVER_NAME'] = DOMAIN or "indev.lukecreated.com"

    from .searchbox import search
    # from .edit import edit
    app.register_blueprint(rootView, url_prefix='/dev')
    app.register_blueprint(search, url_prefix='/search')
    # app.register_blueprint(edit, url_prefix='/edit')
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


systemInfoObject = About(version=0.65, status='beta release',
                         build=20231120, version_note='show keyword in results page')
systemInfo = systemInfoObject.__str__()
systemVersion = systemInfoObject.getSystemVersion()

rootView = Blueprint('rootView', __name__)


@rootView.route("/root-view", methods=['GET'])
def root():
    return render_template('root.html')

# handle http 404 error


def notFound(e):
    """ not found 404 """
    if (request.full_path == '/?') or (request.full_path == '/'):
        # if it is root url, then redirect to the search page, otherwise return the error page
        return redirect(url_for('search.searchHome'))
    # request.full_path, request.url_root
    return render_template('404.html', path=request.full_path)
