# Tutorial 1 — Database Concepts
## BCL1223 / BIT1223 Database Systems

---

### Question 1

**a) Define data and information. (2 marks)**

**Data** refers to raw, unprocessed facts and figures that carry no meaning on their own — for example, the value "150" or the string "RM45.00". **Information** is data that has been processed, organized, and contextualized to make it meaningful and useful for decision-making.

**b) Explain the relationship between data and information using a business example. (4 marks)**

Consider a retail store: each sale generates raw transaction records — product IDs, quantities, prices, and timestamps. These individual records are **data**. When the store's system aggregates these records into a weekly sales report showing total revenue by product category, the result becomes **information**. Data serves as the raw material; the process of selection, aggregation, and formatting transforms it into information that managers can act upon.

**c) Why is accurate and timely information important for organizational decision-making? (4 marks)**

Accurate information ensures that decisions rest on facts rather than guesswork. For instance, a hospital relying on an inaccurate patient record system might administer incorrect treatments. Timely information ensures that decisions are made while they are still relevant — a stock trader receiving price updates five minutes late cannot execute profitable trades. Poor-quality information (inaccurate, delayed, or incomplete) leads directly to poor decisions, financial losses, and missed strategic opportunities.

---

### Question 2

**a) Define a database and a Database Management System (DBMS). (4 marks)**

A **database** is a shared, integrated collection of logically related data structured to support efficient retrieval and modification. A **Database Management System (DBMS)** is the software layer that manages, stores, retrieves, and manipulates data within a database, providing an interface between users and the underlying data.

**b) Explain the role of a DBMS as an intermediary between users and databases. (4 marks)**

The DBMS acts as middleware. When a user or application submits a query (e.g., a SQL SELECT statement), the DBMS translates the high-level request into low-level file operations, retrieves the relevant data, and presents it in the requested format. The DBMS also enforces security policies, manages concurrent access, and maintains integrity constraints — all without requiring the user to know how the data is physically stored.

**c) State and explain any THREE (3) advantages of using a DBMS. (6 marks)**

- **Data Independence:** The separation of logical and physical schemas means that changes to storage structures (e.g., adding an index) do not affect application programs. Developers modify the logical schema without rewriting code.
- **Reduced Data Redundancy:** Centralized data management minimizes unnecessary duplication. When multiple applications need the same data, they share a single copy rather than maintaining separate files.
- **Improved Data Security:** A DBMS provides authentication, authorization, and encryption mechanisms. Administrators grant granular permissions (read, write, delete) at the table or column level, preventing unauthorized access.

---

### Question 3

**a) Differentiate between a single-user database and a multiuser database. (4 marks)**

| Aspect | Single-User Database | Multiuser Database |
|---|---|---|
| Number of users | One at a time | Many simultaneously |
| Typical deployment | Desktop application (e.g., personal library) | Client-server or web-based (e.g., university portal) |
| Concurrency control | Not required | Essential (locks, transactions) |
| Performance focus | Local I/O speed | Concurrent throughput, query optimization |

**b) Compare a centralized database and a distributed database. (4 marks)**

| Aspect | Centralized Database | Distributed Database |
|---|---|---|
| Data location | Single server or mainframe | Multiple geographically separated sites |
| Management | Simpler administration, single point of control | Complex — requires replication, synchronization |
| Failure risk | Single point of failure | Partial failures; other sites continue |
| Network dependency | All users connect to one node | Sites communicate over a network |

**c) A multinational company operates branches in several countries. Recommend the most suitable database type and justify your answer. (7 marks)**

**Recommendation:** A distributed database.

*Justification:* A multinational company with branches across countries faces challenges that a centralized database cannot adequately address. Latency would be high if all branches connect to a single data center; a network outage at the central site would halt all operations globally. A distributed database stores data at each regional branch, providing local access speeds and fault tolerance — if one site fails, the others continue to operate. The distributed approach also improves data locality, reduces wide-area network traffic, and allows each branch to maintain a degree of autonomy over its own data while still enabling consolidated reporting at the headquarters level.

---

### Question 4

**a) Describe two characteristics of traditional file systems. (4 marks)**

- **Separate, isolated files:** Each application maintains its own data files with no shared structure. A payroll application might store employee data in a `.txt` file while a human-resources application keeps the same data in a separate `.csv` file.
- **Program-data dependence:** The file structure (record layout, data types) is embedded directly in the application code. Changing a field's size requires modifying every program that reads that file.

**b) Explain three limitations of file systems that led to the development of DBMSs. (6 marks)**

1. **Data Redundancy:** The same data appears in multiple files. For example, a customer's address stored in both the sales file and the billing file.
2. **Data Inconsistency:** Updates applied to one file but not another create conflicting values. The customer's address might be updated in billing but remain stale in sales.
3. **Lack of Concurrent Access Control:** When two users edit the same file simultaneously, one user's changes may overwrite the other's, leading to lost updates.

**c) Discuss how a DBMS overcomes these limitations. (5 marks)**

A DBMS addresses redundancy by centralizing data definition — each fact is stored once in a shared repository. Inconsistency is prevented through integrity constraints (e.g., CHECK, FOREIGN KEY) and ACID transactions that ensure atomic updates across related tables. Concurrent access is managed by the DBMS's concurrency control subsystem, which uses locking, timestamp ordering, or multi-version concurrency control (MVCC) to serialize conflicting operations without application-level intervention.

---

### Question 5

**a) Define data redundancy and data inconsistency. (4 marks)**

**Data redundancy** is the unnecessary duplication of the same data values across multiple files or tables within a system. **Data inconsistency** arises when different copies of the same data hold conflicting values — a sign that redundant copies have not been kept synchronized.

**b) Explain how data redundancy can lead to data inconsistency. (4 marks)**

When a system stores the same fact (e.g., a customer's phone number) in two different files, every update to that fact must be applied to both locations. If the update mechanism is not atomic or if one location is missed, the two copies diverge. The more places the data is duplicated, the greater the probability of inconsistency.

**c) Provide a real-world example illustrating this problem. (4 marks)**

A university stores a student's address in both the registration office database and the library system. When the student moves and submits a change to registration, the address is updated in the registration database but the library system is not notified. Subsequently, library notices are mailed to the old address. This mismatch — one copy correct, one copy stale — is a data inconsistency caused by the initial redundancy.

---

### Question 6

**a) What are data anomalies? (2 marks)**

Data anomalies are irregularities or inconsistencies that arise in a database as a consequence of poor design, particularly due to uncontrolled data redundancy.

**b) Explain Update, Insertion, and Deletion anomalies with suitable examples. (9 marks)**

| Anomaly | Explanation | Example |
|---|---|---|
| **Update** | Changing a redundant fact requires updating multiple rows; a missed update creates inconsistency | In a denormalized `STUDENT_COURSE` table, changing a professor's name requires updating every row where that professor teaches; missing one row leaves an inconsistency |
| **Insertion** | Adding a new record is impossible without attaching it to another unrelated record | A new course cannot be added to the database until at least one student enrols, because the primary key includes `StudentID` |
| **Deletion** | Deleting a record unintentionally removes other facts that were stored alongside it | Deleting the last enrolment record for a particular course removes the course's name and description from the database |

**c) Suggest how database design can minimize these anomalies. (4 marks)**

Normalization — decomposing large, denormalized tables into smaller, well-structured relations — is the primary technique. Each table should represent a single entity or relationship, with a clearly defined primary key and all non-key attributes fully functionally dependent on that key. Properly normalized schemas eliminate the redundancy that causes update, insertion, and deletion anomalies.

---

### Question 7

**a) Describe the Conceptual, Logical, and Physical Data Models. (9 marks)**

| Model | Level | Description | Audience |
|---|---|---|---|
| **Conceptual** | Highest | Represents what data exists and how entities relate, using Entity-Relationship (ER) diagrams. Independent of any database system. | Business stakeholders, analysts |
| **Logical** | Middle | Maps the conceptual model to a specific data paradigm (e.g., relational). Defines tables, columns, keys, and constraints without storage details. | Database designers, developers |
| **Physical** | Lowest | Describes how data is actually stored — file organization, indexes, partitions, compression, and access paths. | Database administrators |

**b) Explain why data modeling skills are important during database development. (4 marks)**

Data modeling provides a blueprint that bridges business requirements and technical implementation. A well-constructed model captures user needs, identifies data dependencies, and highlights design issues early — before any code is written. Poor modeling at the conceptual or logical stage leads to costly schema redesigns when the system reaches production. Moreover, a clear data model serves as documentation that stakeholders from different backgrounds can review and validate.

---

### Question 8

**a) Identify the five major components of a database system. (5 marks)**

1. Hardware
2. Software (DBMS, operating system, utilities)
3. Data
4. People (end users, database administrators, application developers)
5. Procedures (instructions, policies, standards)

**b) Explain the role of each component in a university database system. (10 marks)**

- **Hardware:** Servers housed in the university's data center store the database files and run the DBMS software. Workstations in administrative offices connect to these servers over the campus network.
- **Software:** The DBMS (e.g., Oracle or MySQL) manages data storage, retrieval, and security. The operating system provides the environment in which the DBMS runs; utilities (e.g., backup scripts, monitoring tools) support routine maintenance.
- **Data:** The university's data includes student records, course catalogs, enrolment registrations, grade transcripts, faculty profiles, and financial aid information. This is the core asset the system protects and serves.
- **People:** **End users** include registrars entering enrollment data, students checking grades, and faculty submitting final marks. **Database administrators** manage schema changes, performance tuning, and backups. **Application developers** build the portals and interfaces that connect users to the database.
- **Procedures:** Standard operating procedures govern how registrars enter new student data, how semester rollover is performed, how backup schedules operate, and how disaster recovery is executed.

---

### Question 9

**a) Explain the purpose of a data dictionary in a DBMS. (4 marks)**

A data dictionary (or system catalog) is a centralized metadata repository that stores descriptions of all database objects — table definitions, column names, data types, constraints, indexes, views, user permissions, and relationships. When a query is submitted, the DBMS consults the dictionary to verify object existence, parse column references, check access rights, and retrieve storage statistics for optimization.

**b) Describe any four DBMS functions. (8 marks)**

1. **Data Definition:** The DBMS provides a Data Definition Language (DDL) — typically SQL's CREATE, ALTER, DROP — that allows users to define and modify the database schema.
2. **Data Manipulation:** The DBMS supports a Data Manipulation Language (DML) — SELECT, INSERT, UPDATE, DELETE — for querying and modifying data.
3. **Security Management:** The DBMS enforces user authentication, role-based access control, and encryption to protect data from unauthorized access.
4. **Integrity Enforcement:** The DBMS checks constraints (PRIMARY KEY, FOREIGN KEY, CHECK, UNIQUE, NOT NULL) automatically on every insert or update, preventing invalid data from entering the database.

**c) Why are backup and recovery functions critical in modern organizations? (3 marks)**

Hardware failures, software bugs, human errors (accidental deletion), and natural disasters can corrupt or destroy data. Without reliable backup and recovery procedures, organizations face permanent data loss, regulatory penalties, legal liability, and extended business downtime. Recovery mechanisms such as transaction logs, point-in-time recovery, and replication ensure that data can be restored to a consistent state after a failure.

---

### Question 10

**a) Identify and explain THREE (3) problems caused by a file-based system. (6 marks)**

1. **Data Redundancy and Inconsistency:** The same data is duplicated across disparate files, leading to conflicting values when updates are applied unevenly.
2. **Program-Data Dependence:** File structure definitions are hard-coded into application programs, so any schema change requires modifying and recompiling every affected program.
3. **Limited Data Sharing:** Each application operates on its own set of files. Sharing data across applications requires manual export/import procedures, which are error-prone and inefficient.

**b) Recommend a database solution. (2 marks)**

Implement a relational Database Management System (DBMS) such as MySQL, PostgreSQL, or Oracle. The relational model provides a standardized schema, supports SQL for ad-hoc queries, and centralizes security and integrity enforcement.

**c) Explain how a DBMS improves data sharing, integrity, and security. (9 marks)**

| Requirement | DBMS Solution |
|---|---|
| **Data Sharing** | Multiple users and applications access the same data simultaneously through controlled interfaces (views, stored procedures). The DBMS manages concurrent access via locking or MVCC. |
| **Data Integrity** | The DBMS enforces domain, entity, and referential integrity constraints automatically. Transactions follow ACID properties — atomicity (all-or-nothing), consistency (valid state before and after), isolation (concurrent transactions are invisible to each other), and durability (committed changes survive failures). |
| **Data Security** | The DBMS provides user authentication, role-based privileges (GRANT/REVOKE), column-level encryption, and audit trails. Access is denied by default and granted explicitly to authorized roles. |

**d) Discuss ONE (1) disadvantage of implementing a database system and how it can be addressed. (3 marks)**

*Disadvantage:* **High initial cost.** A full-scale DBMS deployment requires investment in server hardware, software licenses (e.g., Oracle Enterprise Edition), specialized personnel (database administrators), and training for end users.

*Addressing the disadvantage:* Organizations may adopt open-source DBMS solutions such as PostgreSQL or MariaDB, which eliminate licensing fees. Cloud-based database services (e.g., Amazon RDS, Google Cloud SQL) reduce hardware and maintenance costs by shifting infrastructure management to the provider. Phased implementation — starting with critical modules and expanding — spreads the investment over time.

---

### References

Codd, E. F. (1970). A relational model of data for large shared data banks. *Communications of the ACM*, 13(6), 377–387. https://doi.org/10.1145/362384.362685

Elmasri, R., & Navathe, S. B. (2016). *Fundamentals of Database Systems* (7th ed.). Pearson.

Coronel, C., & Morris, S. (2019). *Database Systems: Design, Implementation, & Management* (13th ed.). Cengage Learning.
