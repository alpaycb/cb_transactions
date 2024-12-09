# ACID Transactions in Couchbase Showcase & Documentation

Demos, Documentations &amp; Links for Couchbase ACID Transactions and Queries with different consistency levels

This demo consists of following parts:
- We need to create a Couchbase cluster with at least three nodes incl. Data, Query, Index & Search services
  - We'll have Docker Container and Capella
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
git clone https://github.com/alpaycb/cb_transactions.git
```

Open the source codes in your favorite IDE (VScode, etc.)

### 3. Create Python Virtual Environment (optional)

In order to install the dependencies in a dedicated folder, you need to create a virtual environment.

For this purpose, change the directory on which Python virtual environment will be created and run the following command

#### On Windows (with PowerShell)

```sh
cd path\to\your\project
python -m venv acidDemo
.\acidDemo\Scripts\Activate.ps1
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


## Running the Queries & Scripts

### Queries in Query Workbench

# THEORY

## The CAP Theorem Explained
The CAP Theorem, also known as Brewer's Theorem, applies to distributed systems, essentially stating that you can have at most two out of three desirable properties:

1. Consistency: All nodes have the same data at the same time (strong consistency) or see an error if unavailable (eventual consistency).
2. Availability: Every request receives a response, even if it might be stale data.
3. Partition Tolerance: The system continues to operate even if network partitions occur, isolating nodes.

In essence, you have to choose two:

* CP (Consistent & Partition Tolerant): Data is always consistent across all nodes, but the system might become unavailable during network partitions. (Example: Blockchain)
* AP (Available & Partition Tolerant): The system is always available even during partitions, but data might be temporarily inconsistent across nodes. (Example: Cassandra)
* CA (Consistent & Available): Both consistency and availability are guaranteed, but this sacrifices partition tolerance. (Almost impossible to achieve in practice)
Outcomes for RDBMS and NoSQL:

### RDBMS (Relational Databases):
* Typically prioritize CP.
* Offer strong consistency guarantees, ensuring all nodes have the same data view.
* May sacrifice availability during network partitions or high load.
* Less suitable for large-scale, highly distributed systems.

### NoSQL Databases:
Offer various trade-offs depending on the specific type:
* Eventual Consistency NoSQL (Cassandra, CouchDB): Prioritize AP. High availability even during partitions, but data might not be immediately consistent across nodes.
* Strong Consistency NoSQL (DynamoDB, CockroachDB): Aim for CP, but achieve it through different mechanisms than RDBMS, potentially impacting other aspects like latency.
* Provide flexibility and scalability for distributed systems.

### Choosing the Right Approach:
The best choice depends on your specific application needs. Consider factors like:

* Data integrity requirements: How crucial is always having the latest data?
* Availability needs: Can your system tolerate downtime?
* Distribution and partitioning potential: Does your system face frequent network issues?
* Performance requirements: How important are fast read/write speeds?

Understanding the CAP Theorem helps you make informed decisions when designing and selecting database solutions for your distributed systems.

## What Kind of database is Couchbase from CAP point of view?
From a CAP perspective, Couchbase typically operates as a CP (Consistent & Partition Tolerant) database. This means it prioritizes maintaining data consistency across all nodes, even if it sacrifices some availability during network partitions.

Here's a breakdown of how Couchbase approaches the CAP properties:

* Consistency: Couchbase uses a strong replica model, ensuring all replicas within a vBucket receive updates before acknowledging a write. This guarantees strong consistency within the cluster.
* Availability: During a network partition, writes become unavailable for that specific data until the partition heals. However, read requests can still be served from replicas, potentially providing eventual consistency (depending on configuration).
* Partition Tolerance: Couchbase is designed to continue operating even when network partitions occur. It achieves this by isolating writes and maintaining consistency within each partition.

However, it's important to note that there are nuances to consider:
* Cluster vs. Cluster: While Couchbase within a cluster prioritizes CP, you can achieve AP across clusters using Continuous Data Replication (XDCR). This allows eventually consistent data exchange between geographically dispersed clusters.
* Configurability: Couchbase offers some configurability in its consistency model. You can choose between strict majority write requirements for strong consistency or relaxed consistency mechanisms for higher availability in certain situations.

Overall, understanding Couchbase's CAP trade-offs is crucial for making informed decisions about your database architecture and data access patterns. Its default CP focus ensures strong consistency within a cluster, but consider your specific needs when scaling across larger, geographically distributed environments.

### Transactions in general with Python SDK

### Eventual Consistency

Eventual consistency in Couchbase refers to a consistency model where updates to the database will eventually propagate to all nodes, but not necessarily immediately. This means that there might be a short period during which different nodes have slightly different data. However, given enough time, all nodes will converge to the same state.

In Couchbase, this model is particularly useful for ensuring high availability and partition tolerance, as described by the CAP theorem1. Couchbase allows for flexibility in consistency levels, enabling it to switch between strong consistency and eventual consistency based on the application’s needs2. This is achieved through asynchronous replication, which ensures that data is eventually consistent across the cluster while maintaining high performance and low latency

### Transactions with ReqPlus

### Transactions for RYOW

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

### What is the concept of RYOW (read your own write) in databases?
RYOW (Read Your Own Write) is a consistency model in database systems that guarantees that once a client successfully completes a write operation, any subsequent read operations made by the same client will see the updated data. In simpler terms, it ensures that you always see the changes you've made to the data.   

#### Why is RYOW important?

Without RYOW, in distributed database systems with multiple replicas or eventual consistency models, a user might update data on one replica, but then read from another replica that hasn't yet received the update. This can lead to confusion and inconsistencies, as the user might see outdated information.   

#### How is RYOW achieved?

There are several techniques to implement RYOW:

* Session Consistency: The system tracks the user's session and ensures that all reads and writes within that session are directed to the same replica or a replica that has the latest updates.   
* Pinning: The user is "pinned" to a specific replica for a certain duration after a write operation. All subsequent reads from that user are directed to the pinned replica, ensuring they see their own writes.   
* Versioning: Each write operation creates a new version of the data. The system tracks the version written by the user and ensures that subsequent reads by the same user retrieve the latest version they wrote.   

#### Benefits of RYOW:
* Improved user experience: Users see their changes reflected immediately, leading to a more intuitive and predictable experience.   
* Simplified development: Developers can rely on RYOW to avoid complex logic for handling inconsistencies.
* Data accuracy: Reduces the risk of users making decisions based on outdated information.

In summary, RYOW is an important consistency guarantee in database systems that ensures users see their own writes, leading to a more consistent and user-friendly experience.   

#### Couchbase achieves Read Your Own Write (RYOW) consistency through a combination of mechanisms:

1.  Strong Consistency for Key-Value Operations:
Couchbase's key-value operations inherently offer strong consistency. When you perform a write operation (like an insert or update) on a document using its key, the operation is replicated to a quorum of nodes before it is acknowledged as successful. This ensures that any subsequent read operation using the same key will retrieve the updated data.

2.  Scan Consistency for SQL++ Queries:
N1QL is Couchbase's query language. While key-value operations are strongly consistent, SQL++ queries introduce the concept of "scan consistency" because they might involve reading data from indexes that are updated asynchronously.   
To achieve RYOW with SQL++, you can use the at_plus consistency level. This level guarantees that a query will see all mutations performed by the same client prior to the query. It works by tracking mutation tokens and ensuring the index is updated with all mutations before the query is executed.   

3.  Durability and Failover:
Couchbase's architecture, with its focus on in-memory operations and efficient replication, contributes to RYOW. Even in case of node failures, the data is replicated and durable, ensuring that your writes are not lost and remain accessible for subsequent reads.   

4.  SDK Support:
The Couchbase SDKs provide options to further enforce RYOW. For instance, you can configure the SDK to use specific consistency levels or to perform operations with synchronous durability requirements, ensuring that writes are persisted to disk before acknowledging success.

In summary, Couchbase provides a robust foundation for achieving RYOW consistency:
* __Strong consistency__ for key-value operations ensures that you always read the latest data you wrote using the same key.
* __at_plus__ scan consistency level extends this guarantee to N1QL queries.
* __Durability__ and failover mechanisms ensure data availability and consistency even in case of failures.
* __SDK options__ provide fine-grained control over consistency levels and durability requirements.

By leveraging these features, developers can build applications on Couchbase with confidence, knowing that their users will have a consistent and predictable experience.



## Links
* Transactions: https://docs.couchbase.com/server/current/learn/data/transactions.html

* Transaction Concepts: https://docs.couchbase.com/python-sdk/current/concept-docs/transactions.html

* Using Transactions with Python SDK (How-To): https://docs.couchbase.com/python-sdk/current/howtos/distributed-acid-transactions-from-the-sdk.html

* Transactions Simulator: https://transactions.couchbase.com/

* SQL++ Support for Couchbase Transactions EE: https://docs.couchbase.com/server/current/n1ql/n1ql-language-reference/transactions.html
  * SQL++ Support for Couchbase Transactions Capella: https://docs.couchbase.com/cloud/n1ql/n1ql-language-reference/transactions.html
  *   Capella Data Tools still doesn’t support transaction: https://couchbasecloud.atlassian.net/browse/AV-54183

## YouTube Videos
* [Demo] ACID Transactions in Couchbase: Balance Transfer (2024, 1:32): https://www.youtube.com/watch?v=6X0CrfkcJxE
* Couchbase Transactions: The What and How of Going Transactional (2021, 36:26): https://www.youtube.com/watch?v=qG7YVjIgWfY
* Couchbase Server N1QL Query Scan Consistency - NotBounded RequestPlus and AtPlus (2016, 5:42): https://www.youtube.com/watch?v=v7eTeKpaqG4


## Blogs
* Understanding Understanding How Transactions Work in Cross Data Center Replications (XDCR): https://www.couchbase.com/blog/couchbase-xdcr-transactions/
