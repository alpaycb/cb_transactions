# ACID Transactions in Couchbase Showcase & Documentation

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

## FAQ

### What are ACID transactions?
1. Atomicity: This principle ensures that a transaction is treated as a single unit, which either fully happens or doesn't happen at all. It prevents partial updates to the database, which can lead to data inconsistency.

Example: Consider a banking system where you want to transfer $100 from Account A to Account B. This operation involves two steps: debiting $100 from Account A and crediting it to Account B. Atomicity ensures that both steps are completed successfully. If for some reason crediting Account B fails (maybe due to a technical error), the transaction is rolled back, and Account A is not debited.

2. Consistency: Consistency ensures that a transaction can only bring the database from one valid state to another, maintaining database invariants. Before and after a transaction, all the database rules, constraints, and triggers must be respected.

Example: If your database has a rule that the balance of any bank account must not go below $0, a transaction that attempts to withdraw more money than the account holds would violate this rule. The consistency principle ensures that the transaction is rejected, keeping the database in a valid state.

3. Isolation: This principle ensures that the concurrent execution of transactions leaves the database in the same state as if the transactions were executed serially (one after the other). This principle helps prevent transactions from interfering with each other.

Example: If two transactions try to update the same bank account simultaneously, isolation ensures that one transaction completes before the other begins, preventing them from seeing intermediate, uncommitted states of each other. For instance, if one transaction is transferring money out of an account while another is calculating the interest, isolation ensures that these transactions do not produce incorrect results due to simultaneous execution.

4. Durability: Durability guarantees that once a transaction has been committed, it will remain so, even in the event of power loss, crashes, or errors. This ensures that the effects of the transaction are permanently recorded in the database.

Example: After completing a transaction that credits $100 to Account B, durability ensures that this change is saved to disk and will not be lost even if the database system crashes immediately after. When the system restarts, Account B will still show the credited amount.
Together, these ACID principles ensure that database transactions are processed reliably, keeping the data accurate and consistent, even in the face of errors, failures, or concurrent access.




## Links
Transactions: https://docs.couchbase.com/server/current/learn/data/transactions.html

Transaction Concepts: https://docs.couchbase.com/python-sdk/current/concept-docs/transactions.html

Using Transactions with Python SDK (How-To): https://docs.couchbase.com/python-sdk/current/howtos/distributed-acid-transactions-from-the-sdk.html



## Blogs
Understanding Understanding How Transactions Work in Cross Data Center Replications (XDCR): https://www.couchbase.com/blog/couchbase-xdcr-transactions/
