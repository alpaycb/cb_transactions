# ACID Transactions in Couchbase Showcase & Documemtation
Demos, Documentations &amp; Links for Couchbase ACID Transactions and Queries with different consistency levels
This demo consists of following parts:
- We need to create a Couchbase cluster with at least three nodes incl. Data, Query, Index & Search services
- Then we'll create our Python virtual environment (optional) and install Couchbase Python SDK components
- We're now ready to adjust the connection strings in the Python codes
- We'll then run individual Python scripts to observe the outcomes of eventual consistency, strong consistency, ACID transactions and RYOW approach

## Steps to Setup and Run the Application

### 1. Create Couchbase Cluster on Docker Container

Run the following command to create and start a Couchbase container:

```sh
docker run -d --name db1 -p 8091-8097:8091-8097 -p 9123:9123 -p 11207:11207 -p 11210:11210 -p 11280:11280 -p 18091-18097:18091-18097 couchbase:enterprise-7.6.3
docker run -d --name db2 couchbase:enterprise-7.6.3
docker run -d --name db3 couchbase:enterprise-7.6.3
```

### 2. Checkout Repository


Clone the git repository:

```sh
git clone https://github.com/grbade/cb_graphql_rest_demo.git
```

Open the source codes in your favorite IDE (VScode, etc.)

### 3. Create Python Virtual Environment (optional)

In order to install the dependencies in a dedicated folder, you need to create a virtual environment.

For this purpose, change the directory on which Python virtual environment will be created and run the following command

#### On Windows

```sh
cd path\to\your\project
python -m venv acidDemo
acidDemo\Scripts\activate
```

#### On MAC

```sh
cd /path/to/your/project
python3 -m venv acidDemo
source venv/bin/acidDemo
```

#### Deactivating the Virtual Environment (Windows and MAC)

```sh
deactivate
```


### 4. Install Requirements

We neeed to install Couchbase Python SDK

#### Windows:
```sh
python -m pip install couchbase==4.3.1
```

#### Mac
```sh
python3 -m pip install couchbase==4.3.1
```


## Running the Scripts

### Eventual Consistency

Eventual consistency in Couchbase refers to a consistency model where updates to the database will eventually propagate to all nodes, but not necessarily immediately. This means that there might be a short period during which different nodes have slightly different data. However, given enough time, all nodes will converge to the same state.

In Couchbase, this model is particularly useful for ensuring high availability and partition tolerance, as described by the CAP theorem1. Couchbase allows for flexibility in consistency levels, enabling it to switch between strong consistency and eventual consistency based on the application’s needs2. This is achieved through asynchronous replication, which ensures that data is eventually consistent across the cluster while maintaining high performance and low latency




## Links
Transactions: https://docs.couchbase.com/server/current/learn/data/transactions.html

Transaction Concepts: https://docs.couchbase.com/python-sdk/current/concept-docs/transactions.html

Using Transactions with Python SDK (How-To): https://docs.couchbase.com/python-sdk/current/howtos/distributed-acid-transactions-from-the-sdk.html



## Blogs
Understanding Understanding How Transactions Work in Cross Data Center Replications (XDCR): https://www.couchbase.com/blog/couchbase-xdcr-transactions/
