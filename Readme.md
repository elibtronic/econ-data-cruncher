
# Econ Data Cruncher #

updated for Nov, 2019

- Slowly porting to Python 3

## Python Packages needed ##
- [Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/#Download)
- [Couchpy](https://pypi.python.org/pypi/couchpy/0.2dev)

## Additional Software ##
- [CouchDB](https://couchdb.apache.org/) please consult project docs on how to install configure

### Getting this running ###
- copy *setting.py.orig* to *settting.py*
- fill in details about couch database server
- run `python settings.py` to create directories, only need to do this once



### Downloading the Data ###
- will port previous version
- details soon

### Loading Data to DB ###
- previous step will download raw HTML and clean it
- Assure all data ready to be loaded is in: `AN_IN`
- run `python load_db.py` to attempt database inserts of all files
- successfully loaded files show up in `AN_OUT`
- errored out files will end up in `AN_ERROR`

### Cleaning the Data ###
- some cleanup is done during download/change/upload to DB process
- TBD for rest of process

### Analyzing the Data ###
- TBD. _(Most likely will be a Jupyter Notebook)_