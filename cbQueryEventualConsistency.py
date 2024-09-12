from datetime import timedelta
import logging
import traceback
# For exceptions
import couchbase
from couchbase.exceptions import CouchbaseException
# Required for any cluster connection
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.n1ql import QueryScanConsistency
# Required for options -- cluster, timeout, SQL++ (N1QL) query, etc.
from couchbase.options import ClusterOptions

# output log messages to example.log
logging.basicConfig(filename='example.log',
                    filemode='w', 
                    level=logging.DEBUG,
                    format='%(levelname)s::%(asctime)s::%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger()
couchbase.configure_logging(logger.name, level=logger.level) 

# Couchbase Connection
endpoint = "couchbases://cb.qp6j2fqsqf9t5hd6.cloud.couchbase.com" # Replace this with Connection String
username = "techuser" # Replace this with username from database access credentials
password = "techU$er01" # Replace this with password from database access credentials
bucket_name = "travel-sample"
scope_name = "inventory"
collection_name = "airline"

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
    
    # Get the number of airlines before insert
    query = ''' SELECT COUNT(1) as airlineCount FROM `travel-sample`.inventory.airline WHERE type='airline' '''

    try:
        result = scope.query(query)
        for row in result:            
            print(f'\nNumber of airlines before insert: {row["airlineCount"]}')
    except CouchbaseException as ex:
        logger.error(traceback.format_exc())
    except Exception as e:
        logger.error(e)
    
    # Simple K-V operation - to create a document with specific ID
    try:
        result = cb_coll.insert(key, sample_airline)
        print("\nCreate document success. CAS: ", result.cas)
    except CouchbaseException as e:
        logger.error(traceback.format_exc())
        print(e)

    try:
        result = scope.query(query)
        # result = scope.query(query, scan_consistency=QueryScanConsistency.NOT_BOUNDED)
        for row in result:            
            print(f'\nNumber of airlines after insert: {row["airlineCount"]}')
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
