from datetime import timedelta
import logging
import traceback
import os
from dotenv import load_dotenv

# For exceptions
import couchbase
from couchbase.exceptions import CouchbaseException
# Required for any cluster connection
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
# Required for options -- cluster, timeout, SQL++ (N1QL) query, etc.
from couchbase.options import ClusterOptions
from couchbase.search import SearchOptions, SearchScanConsistency, QueryStringQuery
from couchbase.cluster import QueryOptions, QueryScanConsistency


# output log messages to example.log
logging.basicConfig(filename='example.log',
                    filemode='w', 
                    level=logging.DEBUG,
                    format='%(levelname)s::%(asctime)s::%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger()
couchbase.configure_logging(logger.name, level=logger.level) 

# Load the .env file
env_loaded = load_dotenv()

# Configuration variables
endpoint = os.getenv('DB_CONN_STR')
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
bucket_name = os.getenv('DB_BUCKET')
scope_name = os.getenv('DB_SCOPE')
collection_name = os.getenv('DB_COLLECTION')

# Key will equal: "airline_8091"
key = "airline_8091"

# Sample airline document
sample_airline = {
    "type": "airline",
    "id": 8091,
    "callsign": "CBS",
    "iata": None,
    "icao": None,
    "name": "Couchbase Airways",
}

# Connect options - authentication
auth = PasswordAuthenticator(username, password)
# Get a reference to our cluster
options = ClusterOptions(auth)
# Use the pre-configured profile below to avoid latency issues with your connection.
options.apply_profile("wan_development")

try:
    cluster = Cluster(endpoint, options)
    # Wait until the cluster is ready for use.
    cluster.wait_until_ready(timedelta(seconds=5))
    logger.info('Cluster ready.')
    
    # Get a reference to our bucket
    cb = cluster.bucket(bucket_name)
    # Get a reference to our collection
    scope = cb.scope('inventory')
    cb_coll = cb.scope(scope_name).collection(collection_name)
    
    
    query = ''' SELECT COUNT(1) as airlineCount FROM `travel-sample`.inventory.airline WHERE type='airline' '''

    # Get the number of airlines before insert
    try:
        result = scope.query(query)
        for row in result:            
            print(f'\nNumber of airlines before insert: {row["airlineCount"]}')
    except CouchbaseException as ex:
        logger.error(traceback.format_exc())
        traceback.print_exc()
    except Exception as e:
        logger.error(e)
        print(e)
    
    # Simple K-V operation - to create a document with specific ID
    try:
        result = cb_coll.insert(key, sample_airline)
        print("\nCreate document success. CAS: ", result.cas)
    except CouchbaseException as e:
        logger.error(traceback.format_exc())
        print(e)

    # Get the number of airlines after insert
    try:
        # result = scope.query(query, scan_consistency=QueryScanConsistency.REQUEST_PLUS)
        
        # result = scope.query(query, couchbase.options.GetOptions(consistency=couchbase.options.Consistency.REQUEST_PLUS))
        result = scope.query(query, scan_consistency=QueryScanConsistency.REQUEST_PLUS)

        for row in result:            
            print(f'\nNumber of airlines after insert with REQUEST_PLUS: {row["airlineCount"]}')
    except CouchbaseException as ex:
        logger.error(traceback.format_exc())
    except Exception as e:
        logger.error(e)
    
    # Simple K-V operation - to retrieve a document by ID
    try:
        result = cb_coll.get(key)
        print("\nFetch document success. Result: ", result.content_as[dict])
    except CouchbaseException as e:
        print(e)
        logger.error(e)
    
    # Simple K-V operation - to update a document by ID
    try:
        sample_airline["name"] = "Couchbase Airways!!"
        result = cb_coll.replace(key, sample_airline)
        print("\nUpdate document success. CAS: ", result.cas)
    except CouchbaseException as e:
        print(e)
        logger.error(e)
    
    # Simple K-V operation - to delete a document by ID
    try:
        result = cb_coll.remove(key)
        print("\nDelete document success. CAS: ", result.cas)
    except CouchbaseException as e:
        print(e)
        logger.error(e)

except Exception as e:
    logger.error(traceback.format_exc())
    traceback.print_exc()
