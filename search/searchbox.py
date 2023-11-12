from flask import render_template, request, Blueprint
from markupsafe import escape
import math
from search import es

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
    page_size = 5 # documents per shown page
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

    res = es.search(index=['pdt'], body=body)
    res2 = es.search(index=['raw'], body=body)
    hits = [{'name': doc['_source']['name'], 'description': doc['_source']['description'], 'created': doc['_source']['created']} for doc in res['hits']['hits']]
    hits += [{'name': doc['_source']['name'], 'description': doc['_source']['description'], 'submitted': doc['_source']['submitted']} for doc in res2['hits']['hits']]
    totalPages = math.ceil(((res['hits']['total']['value'])+(res2['hits']['total']['value']))/page_size) # calculate the total pages of returned results
    return render_template('results.html',keyword=keyword, results=hits, page_no=page_no, totalPages=totalPages)
    return render_template('results.html', page_no=5, totalPages=10)

# show indenpendent (selected/clicked) result
@search.route("/result/lookup/<name>")
def result(name):
     # some part of the code below adapted from Pisol Ruenin
    page_size = 3 # documents per shown page
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

    res = es.search(index=['pdt'], body=body)
    res2 = es.search(index=['raw'], body=body)
    hits = [{'name': doc['_source']['name'], 'description': doc['_source']['description'], 'created': doc['_source']['created']} for doc in res['hits']['hits']]
    hits += [{'name': doc['_source']['name'], 'description': doc['_source']['description'], 'submitted': doc['_source']['submitted']} for doc in res2['hits']['hits']]
    totalPages = math.ceil(((res['hits']['total']['value'])+(res2['hits']['total']['value']))/page_size) # calculate the total pages of returned results
    return render_template('results.html',keyword=name, results=hits, page_no=page_no, totalPages=totalPages)
  
    return render_template("result.html", title=title,content=None)