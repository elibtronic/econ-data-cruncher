#http://admin:J7mPxZC6mr@rtod.library.brocku.ca:32771/econ_data_working

from settings import *
import couchdb
couch = couchdb.Server(CDB_HOST)
db = couch["econ_data_working"]
