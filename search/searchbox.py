from flask import render_template, request, Blueprint
from markupsafe import escape
import math
from search import es

search = Blueprint('search', __name__)


@search.route('/', methods=['GET'])  # return a searchbox page
def searchHome():
    if request.method == 'POST':
        return 'render_template("searchbox.html")'
    else:
        return render_template("searchbox.html")


@search.route('/results', methods=['GET'])  # return a list of results
def searchResults():
    # some part of the code below adapted from Pisol Ruenin
    page_size = 5  # documents per shown page
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
                'fields': ['name', 'description'],
                'fuzziness': 'AUTO'
            }
        }
    }

    index1 = "pdt"
    index2 = "raw"

    es.index(index=index1, body=body, id=1)
    es.index(index=index2, body=body, id=2)

    res = es.search(index=[index1, index2], body=body)
    hits = [{'name': doc['_source']['name'], 'description': doc['_source']['description'],
             } for doc in res['hits']['hits']]  # calculate the total pages of returned results
    totalPages = math.ceil((res['hits']['total']['value'])/page_size)
    return render_template('results.html', keyword=keyword, results=hits, page_no=page_no, totalPages=totalPages)


# show indenpendent (selected/clicked) result
@search.route("/result/lookup/<name>")
def result(name):
    # some part of the code below adapted from Pisol Ruenin
    page_size = 3  # documents per shown page
    keyword = request.args.get('match')
    if request.args.get('page'):
        page_no = int(request.args.get('page'))
    else:
        page_no = 1

    body = {
        'size': page_size,
        'from': page_size * (page_no-1),
        'query': {
            'term': {
                'name.keyword': name
            }
        }
    }

    index1 = "pdt"
    index2 = "raw"

    es.index(index=index1, body=body, id=1)
    es.index(index=index2, body=body, id=2)

    res = es.search(index=[index1, index2], body=body)
    hits = [{'name': doc['_source']['name'], 'description': doc['_source']['description'],
             } for doc in res['hits']['hits']]  # calculate the total pages of returned results
    totalPages = math.ceil((res['hits']['total']['value'])/page_size)
    return render_template('result.html', keyword=keyword, result=hits, page_no=page_no, totalPages=totalPages, title=name)
