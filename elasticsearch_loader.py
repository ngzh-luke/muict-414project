# Adapted from the code from Pisol Ruenin

from elasticsearch import Elasticsearch, helpers
import ndjson
import argparse
import uuid
from decouple import config as envar # import .env contents, you may COMMENT OUT this line

ELASTIC_PASSWORD = envar("ELASTIC_PASSWORD","password") # ASSIGN your password this line
es = Elasticsearch( "https://localhost:9200", basic_auth=("elastic", ELASTIC_PASSWORD), verify_certs=False)

parser = argparse.ArgumentParser()
parser.add_argument('--file')
parser.add_argument('--index')
# parser.add_argument('--type')

args = parser.parse_args()

index = args.index
file = args.file
# doc_type = args.type


with open(file) as json_file:
    json_docs = ndjson.load(json_file)

def bulk_json_data(json_list, _index):
    for doc in json_list:

        if '{"index"' not in doc:
            yield {
                "_index": _index,
                # "_type": doc_type,
                "_id": uuid.uuid4(),
                "_source": doc
            }

try:
    # make the bulk call, and get a response
    response = helpers.bulk(es, bulk_json_data(json_docs, index))
    print ("\nRESPONSE:", response)
except Exception as e:
    print("\nERROR:", e)