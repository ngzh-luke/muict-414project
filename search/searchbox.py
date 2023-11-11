from flask import render_template, request, Blueprint
from markupsafe import escape
from elasticsearch import Elasticsearch
from decouple import config as envar
import math

ELASTIC_PASSWORD = envar("ELASTIC_PASSWORD","test123")

es = Elasticsearch("https://localhost:9200", http_auth=("elastic", ELASTIC_PASSWORD), verify_certs=False)

search = Blueprint('search', __name__)

@search.route('/', methods=['GET'])
def searchHome():
    return render_template("searchbox.html")

@search.route('/results', methods=['POST', 'GET'])
def searchResult():
    page_size = 10
    keyword = request.args.get('keyword')
    if request.args.get('page'):
        page_no = int(request.args.get('page'))
    else:
        page_no = 1

    body = {
        'size': page_size,
        'from': page_size * (page_no-1),
        'query': {
            'multi_match': {
                'query': keyword,
                'fields': ['name', 'description']
            }
        }
    }

    res = es.search(index='products', body=body)
    hits = [{'name': doc['_source']['name'], 'description': doc['_source']['description'], 'created': doc['_source']['created']} for doc in res['hits']['hits']]
    page_total = math.ceil(res['hits']['total']['value']/page_size)
    return render_template('results.html',keyword=keyword, hits=hits, page_no=page_no, page_total=page_total)