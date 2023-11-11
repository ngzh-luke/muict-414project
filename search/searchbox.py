from flask import render_template, request, Blueprint
from markupsafe import escape
from elasticsearch import Elasticsearch
from decouple import config as envar
import math

ELASTIC_PASSWORD = envar("ELASTIC_PASSWORD","password")

es = Elasticsearch("https://localhost:9200", http_auth=("elastic", ELASTIC_PASSWORD), verify_certs=False)

search = Blueprint('search', __name__)

# return a searchbox page
@search.route('/', methods=['GET'])
def searchHome():
        if request.method == 'POST':
            return 'render_template("searchbox.html")'
        else:
            return render_template("searchbox.html")

# return a list of results
@search.route('/results', methods=['GET'])
def searchResults():
    # some part of the code below adapted from Pisol Ruenin
    page_size = 10 # documents per shown page
    # keyword = request.args.get('keyword')
    # if request.args.get('page'):
    #     page_no = int(request.args.get('page'))
    # else:
    #     page_no = 1

    # body = {
    #     'size': page_size,
    #     'from': page_size * (page_no-1),
    #     'query': {
    #         'multi_match': {
    #             'query': keyword,
    #             'fields': ['name', 'description']
    #         }
    #     }
    # }

    # res = es.search(index=['products'], body=body)
    # hits = [{'name': doc['_source']['name'], 'description': doc['_source']['description'], 'created': doc['_source']['created']} for doc in res['hits']['hits']]
    # totalPages = math.ceil(res['hits']['total']['value']/page_size) # calculate the total pages of returned results
    # return render_template('results.html',keyword=keyword, results=hits, page_no=page_no, totalPages=totalPages)
    return render_template('results.html', page_no=5, totalPages=10)

# show indenpendent (selected/clicked) result
@search.route("/result/lookup/<title>")
def result(title):
     return render_template("result.html", title=title,content=None)