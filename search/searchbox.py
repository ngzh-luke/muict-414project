from flask import render_template, request, Blueprint

search = Blueprint('search', __name__)

@search.route('/', methods=['GET'])
def searchHome():
    return render_template("searchbox.html")