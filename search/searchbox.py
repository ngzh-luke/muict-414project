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
                'fields': ['name', 'description', 'ID', 'region', 'history', 'step', 'ingredient', 'minutes'],
                'fuzziness': 'AUTO'
            }
        }
    }

    # index1 = "pdt"
    # index2 = "raw"
    index = 'food'

    es.index(index=index, body=body, id=1)
    # es.index(index=index2, body=body, id=2)

    res = es.search(index=[index], body=body)
    hits = [{'name': doc['_source']['name'], 'description': doc['_source']['description'], 'ID': doc['_source']['ID'], 'region': doc['_source']['region']
             } for doc in res['hits']['hits']]  # calculate the total pages of returned results
    totalPages = math.ceil((res['hits']['total']['value'])/page_size)
    return render_template('results.html', keyword=keyword, results=hits, page_no=page_no, totalPages=totalPages, kw=keyword)


# show indenpendent (selected/clicked) result
@search.route("/result/lookup/<int:id>/")
def result(id):
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
                'ID.keyword': id
            }
        }
    }

    # index1 = "pdt"
    # index2 = "raw"
    index = 'food'

    es.index(index=index, body=body, id=1)
    # es.index(index=index2, body=body, id=2)

    res = es.search(index=[index], body=body)
    hits = [{'name': doc['_source']['name'], 'description': doc['_source']['description'], 'history': doc['_source']['history'], 'minutes': doc['_source']['minutes'], 'region': doc['_source']['region'], 'n_step': doc['_source']['n_step'], 'n_ingredient': doc['_source']['n_ingredient'], 'step': doc['_source']['step'], 'ingredient': doc['_source']['ingredient'], 'id': doc['_source']['ID']
             } for doc in res['hits']['hits']]  # calculate the total pages of returned results
    totalPages = math.ceil((res['hits']['total']['value'])/page_size)
    name = str([{'name': doc['_source']['name']}
                for doc in res['hits']['hits']][0]['name'])  # select the first result then select only value then convert the whole to string
    return render_template('result.html', keyword=keyword, result=hits, page_no=page_no, totalPages=totalPages, title=name, id=id)
