from datetime import timedelta
import logging
import traceback
import os
from dotenv import load_dotenv

import couchbase
from couchbase.exceptions import CouchbaseException
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster, QueryOptions, QueryScanConsistency
from couchbase.options import ClusterOptions, SearchOptions
from couchbase.mutation_state import MutationState
# from couchbase.search import SearchOptions, SearchScanConsistency, QueryStringQuery

# output log messages to example.log
logging.basicConfig(filename='exampleRYOW.log',
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
    "name": "Couchbase RYOW Airways",
}

sample_airlineA = {
    "type": "airline",
    "id": 8092,
    "callsign": "CBD",
    "iata": None,
    "icao": None,
    "name": "CBDB Airways",
}
keyA = "airline_8092"

sample_airlineB = {
    "type": "airline",
    "id": 8093,
    "callsign": "CBN",
    "iata": None,
    "icao": None,
    "name": "CBNS Airlines",
}
keyB = "airline_8093"

# Initialize the Couchbase cluster
# cluster = Cluster(connection_str, ClusterOptions(PasswordAuthenticator(username, password)))

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
    queryRYOW = ''' SELECT name FROM `travel-sample`.inventory.airline WHERE id = 8091 '''

    # Simple K-V operation - to create a document with specific ID
    try:
        resultA = cb_coll.insert(key, sample_airlineA)
        print("\nCreate 1st document success. CAS: ", resultA.cas)

        resultB = cb_coll.insert(keyA, sample_airline)
        print("\nCreate 2nd document success. CAS: ", resultB.cas)

        result = cb_coll.insert(keyB, sample_airline)
        print("\nCreate 3rd (RYOW) document success. CAS: ", result.cas)

        # Insert or upsert the document and capture the mutation state        
        mutation_state = MutationState(result)

        queryResult = scope.query(queryRYOW, scan_consistency=QueryScanConsistency.AT_PLUS, consistent_with=mutation_state)
        # queryResult = scope.query(query, SearchOptions(consistent_with=mutation_state))

        for row in queryResult:            
            print(f'\nName of airline after insert, querying with AT_PLUS/RYOW: {row["name"]}')
    except CouchbaseException as e:
        logger.error(traceback.format_exc())
        print(e)

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
        #logger.info('Delete 3rd (RYOW) document success. CAS: ', result.cas)
        resultA = cb_coll.remove(keyA)
        #logger.info('Delete 1st document success. CAS: ', resultA.cas)
        resultB = cb_coll.remove(keyB)
        #logger.info('Delete 2nd document success. CAS: ', resultB.cas)
    except CouchbaseException as e:
        print(e)
        logger.error(e)

except Exception as e:
    logger.error(traceback.format_exc())
    traceback.print_exc()
