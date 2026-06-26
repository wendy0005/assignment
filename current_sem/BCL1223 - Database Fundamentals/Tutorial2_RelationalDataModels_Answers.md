# Tutorial 2 — Relational Data Models
## BCL1223/BIT1223 Database Systems

---

### Question 1

**a) Define the relational database model. (2 marks)**

The relational database model, introduced by Codd (1970), organizes data into *relations* — two-dimensional tables composed of *tuples* (rows) and *attributes* (columns). Each relation represents an entity or relationship, with constraints such as primary keys ensuring tuple uniqueness and foreign keys enforcing referential integrity across relations. The model provides a logical abstraction that decouples data storage from data access through set-oriented operations defined in relational algebra.

**b) Explain TWO advantages of the relational database model compared to hierarchical and network database models. (4 marks)**

The first advantage is **logical simplicity and data independence**. Unlike hierarchical and network models that require programmers to navigate predefined pointer paths or parent–child structures, relational databases present all data as simple tables. Changes to physical storage structures — such as adding indexes or reorganizing files — do not alter the logical schema, shielding applications from storage-level modifications (Elmasri & Navathe, 2016).

The second advantage is **flexible ad-hoc querying** via declarative languages such as SQL. In hierarchical and network models, retrieving data requires writing procedural code that explicitly traverses record linkages. The relational model supports set-based operations (SELECT, PROJECT, JOIN) that allow users to express complex queries without specifying access paths, greatly improving productivity and reducing development time.

**c) Differentiate between logical data independence and physical data independence. (4 marks)**

| Aspect | Logical Data Independence | Physical Data Independence |
|---|---|---|
| Scope | Protects external schemas from changes to the conceptual schema | Protects the conceptual schema from changes to the internal storage |
| Examples of change | Adding a new column, splitting a table, modifying relationships | Changing file organization, adding indexes, altering storage hardware |
| Impact level | Higher-level abstraction — more difficult to achieve | Lower-level abstraction — relatively easier to implement |
| Typical difficulty | Requires view mapping and may involve restructuring applications | Handled transparently by the DBMS |

---

### Question 2

A university maintains the following table:

`STUDENT(StudentID, StudentName, Programme, CGPA)`

**a) Explain the meaning of the terms relation, tuple, and attribute using the STUDENT table above. (6 marks)**

A **relation** corresponds to the entire STUDENT table — a named set of tuples sharing the same attribute structure. It is the fundamental building block of the relational model.

A **tuple** is an individual row within the relation. For example, the row `(S12345, Ali Bin Ahmad, Computer Science, 3.72)` constitutes one tuple representing a single student entity.

An **attribute** is a named column of the relation, such as `StudentID`, `StudentName`, `Programme`, or `CGPA`. Each attribute draws values from a defined domain (e.g., `CGPA` draws from a decimal range 0.00–4.00). The number of attributes in a relation is called its *degree* (four in this case).

**b) Why is a table considered a logical representation of a relation? (4 marks)**

A table mirrors the mathematical definition of a relation — specifically, a subset of the Cartesian product of attribute domains. Each row is an ordered n-tuple of domain values, and the column headers name each dimension of the product. The table's structure (unique rows, unordered tuples, atomic attribute values) directly implements the properties of a mathematical relation, making it a natural and intuitive logical representation.

---

### Question 3

Consider the following relation:

`EMPLOYEE(EmpID, EmpName, Department, Salary)`

Given that: `EmpID → EmpName, Department, Salary`

**a) Define functional dependency. (2 marks)**

A functional dependency $X \rightarrow Y$ states that for any two tuples in the relation, if they share the same value for attribute set $X$, they must also share the same value for attribute set $Y$. In simpler terms, the value of $X$ uniquely determines the value of $Y$.

**b) Explain why EmpID functionally determines the other attributes. (4 marks)**

`EmpID` serves as the unique identifier for each employee. No two employees share the same `EmpID` value — it is assigned uniquely at record creation. Consequently, given a specific `EmpID`, the system can retrieve exactly one `EmpName`, one `Department`, and one `Salary`. This one-to-one correspondence between `EmpID` and the remaining attributes satisfies the definition of functional dependency.

**c) Determine whether EmpName can functionally determine EmpID. Justify your answer. (4 marks)**

`EmpName` cannot functionally determine `EmpID` because employee names are not guaranteed to be unique. Two different employees may share the same name — for instance, two individuals named "Ahmad Faiz" would have different `EmpID` values. Under functional dependency $EmpName \rightarrow EmpID$, every occurrence of "Ahmad Faiz" would need to map to a single `EmpID`, which is impossible when the name is shared. Therefore, the dependency does not hold.

---

### Question 4

Consider the relation:

`COURSE_REGISTRATION(StudentID, CourseID, Semester, Grade)`

**a) Define the following terms: (8 marks)**

| Term | Definition | Example |
|---|---|---|
| **Superkey** | A set of attributes that uniquely identifies every tuple in a relation | `{StudentID, CourseID, Semester}`; `{StudentID, CourseID, Semester, Grade}` |
| **Candidate Key** | A minimal superkey — no proper subset is itself a superkey | `{StudentID, CourseID, Semester}` (cannot remove any attribute without losing uniqueness) |
| **Primary Key** | The candidate key chosen by the database designer as the main identifier | `{StudentID, CourseID, Semester}` |
| **Composite Key** | A primary key consisting of two or more attributes | `(StudentID, CourseID, Semester)` — three attributes jointly form the key |

**b) Identify the most appropriate primary key for the relation and justify your answer. (4 marks)**

The most appropriate primary key is the composite key `(StudentID, CourseID, Semester)`.

*Justification:* A student can register for multiple courses, so `StudentID` alone is insufficient (one student produces many rows). A single course has many students, so `CourseID` alone is insufficient. Even the pair `(StudentID, CourseID)` is not enough because the same student may retake the same course in a different semester. Adding `Semester` resolves this ambiguity. The `Grade` attribute cannot be part of the key because it is the value being recorded, not an identifier.

---

### Question 5

Given the following tables:

`DEPARTMENT(DeptID, DeptName)`
`EMPLOYEE(EmpID, EmpName, DeptID)`

**a) Identify the primary key and foreign key in the tables above. (4 marks)**

| Table | Primary Key | Foreign Key |
|---|---|---|
| DEPARTMENT | `DeptID` | — |
| EMPLOYEE | `EmpID` | `DeptID` (references `DEPARTMENT.DeptID`) |

**b) Explain the concept of referential integrity. (3 marks)**

Referential integrity ensures that every foreign key value in a referencing table must either (i) match a primary key value in the referenced table or (ii) be NULL. This constraint guarantees that relationships between tables remain consistent — an employee cannot be assigned to a department that does not exist.

**c) Describe what would happen if an employee record contains a DeptID that does not exist in the DEPARTMENT table. (3 marks)**

Such a record would violate referential integrity and create an *orphan row* — an employee linked to a non-existent department. The DBMS enforces referential integrity at the constraint level; any `INSERT` or `UPDATE` that produces an invalid `DeptID` is rejected with an integrity constraint violation error. Some systems offer cascade options (e.g., `ON DELETE SET NULL`) to handle deletions gracefully, but by default the operation fails.

---

### Question 6

A company stores the following information:

| CustomerID | CustomerName | OrderID | OrderDate |
|---|---|---|---|
| C001 | Ali | O101 | 10-Jan-2026 |
| C002 | Siti | O102 | 12-Jan-2026 |

**a) Convert the information into relational schemas. (4 marks)**

```
CUSTOMER(**CustomerID**, CustomerName)
ORDER(**OrderID**, OrderDate, CustomerID*)
```

Primary keys are shown in **bold**; foreign keys are marked with *.

**b) Underline the primary keys and indicate foreign keys. (4 marks)**

- `CUSTOMER( **CustomerID** , CustomerName )`
- `ORDER( **OrderID** , OrderDate, CustomerID* )`

`CustomerID` is the primary key of `CUSTOMER` and a foreign key in `ORDER`.

**c) Explain the relationship between the entities identified. (2 marks)**

The relationship is **One-to-Many (1:M)** — one customer can place many orders, but each order belongs to exactly one customer. This is implemented by embedding the `CustomerID` foreign key inside the `ORDER` table.

---

### Question 7

**a) Differentiate between the following relationship types: (6 marks)**

$$
\begin{array}{|l|l|l|}
\hline
\textbf{Type} & \textbf{Definition} & \textbf{Crow's Foot Symbol} \\
\hline
\text{One-to-One (1:1)} & \text{One entity in A relates to at most one entity in B, and vice versa} & \text{---}\|\text{---}\| \\
\text{One-to-Many (1:M)} & \text{One entity in A relates to many entities in B; each B relates to one A} & \text{---}\|\text{---<} \\
\text{Many-to-Many (M:N)} & \text{One entity in A relates to many in B, and one entity in B relates to many in A} & \text{---<}\text{>---} \\
\hline
\end{array}
$$

**b) Provide ONE real-world example for each relationship type. (6 marks)**

- **1:1 — Person and Passport:** Each person holds at most one passport, and each passport belongs to exactly one person.
- **1:M — Department and Employee:** One department employs many employees; each employee works in exactly one department.
- **M:N — Student and Course:** A student enrols in multiple courses over a semester, and each course contains many enrolled students. This requires a junction table (e.g., `Enrolment`) to be resolved.

**c) Explain why M:N relationships cannot be directly implemented in a relational database. (3 marks)**

Relational tables store data as rows with fixed attribute sets. An M:N relationship implies that one row in table A can be associated with an arbitrary number of rows in table B — storing this directly would require a variable-length attribute, which violates the atomicity rule of first normal form (1NF). The standard solution is to introduce a *bridge* (junction) table that decomposes the M:N relationship into two 1:M relationships. For example, a `Student_Course` junction table with a composite primary key `(StudentID, CourseID)` resolves the M:N between `Student` and `Course`.

---

### Question 8

**a) Define a data dictionary. (3 marks)**

A data dictionary — also called a *system catalog* — is a centralized repository of metadata that describes the structure, constraints, and properties of all database objects. It stores information such as table names, column definitions, data types, primary and foreign keys, indexes, views, user permissions, and storage parameters.

**b) Explain the role of metadata in a relational database. (3 marks)**

Metadata provides the DBMS with a self-describing framework for managing data. When a query is submitted, the DBMS consults the metadata to resolve table and column names, verify access rights, check constraint compliance, and retrieve statistics for query optimization. Without metadata, the DBMS would have no knowledge of the database's own structure.

**c) Discuss THREE benefits of maintaining a system catalog. (6 marks)**

- **Data Consistency and Standardization:** The catalog enforces uniform naming conventions and data-type rules across all tables. Changes to a column definition are immediately visible to all users and applications, preventing schema drift.

- **Access Control and Security:** The catalog stores user privileges at the table, column, and operation levels. The DBMS checks these permissions on every query, ensuring that only authorized users can read or modify sensitive data.

- **Query Optimization:** The catalog maintains statistics — row counts, index selectivity, data distribution histograms — that the query optimizer uses to choose efficient execution plans (e.g., index scans versus full table scans). These statistics directly impact query performance.

---

### Question 9

Given the relation:

`STUDENT(StudentID, StudentName, Programme)`

**a) Explain the difference between the SELECT and PROJECT operations. (4 marks)**

The **SELECT** operation ($\sigma$) filters *rows* (tuples) based on a predicate condition. It reduces the cardinality (number of tuples) but retains all attributes.

The **PROJECT** operation ($\pi$) filters *columns* (attributes), retaining only those specified and eliminating duplicate tuples from the result. It reduces the degree (number of attributes) but may not reduce cardinality unless duplicates arise.

**b) Write the relational algebra expression to: (4 marks)**

- Retrieve all students from the "Computer Science" programme:

$$\sigma_{\text{Programme} = \text{"Computer Science"}}(\text{STUDENT})$$

- Display only StudentID and StudentName:

$$\pi_{\text{StudentID}, \text{StudentName}}(\sigma_{\text{Programme} = \text{"Computer Science"}}(\text{STUDENT}))$$

**c) Differentiate between UNION and INTERSECT with suitable examples. (4 marks)**

| Operation | Symbol | Result | Example |
|---|---|---|---|
| **UNION** | $R \cup S$ | All tuples that appear in $R$ or $S$ (or both), duplicates removed | $\pi_{\text{Programme}}(\text{STUDENT}) \cup \pi_{\text{Programme}}(\text{STAFF})$ returns all unique programmes across both tables |
| **INTERSECT** | $R \cap S$ | Only tuples that appear in both $R$ and $S$ | $\pi_{\text{Programme}}(\text{STUDENT}) \cap \pi_{\text{Programme}}(\text{STAFF})$ returns only programmes that exist in both tables |

Both operations require the operand relations to be *union-compatible* — same number of attributes and compatible domains.

---

### Question 10

**a) Define data redundancy. (2 marks)**

Data redundancy refers to the unnecessary duplication of data values across multiple records or tables within a database. While controlled redundancy (e.g., foreign keys) is essential for relationship representation, uncontrolled redundancy wastes storage and leads to maintenance problems.

**b) Explain TWO data anomalies that may result from excessive redundancy. (4 marks)**

- **Update Anomaly:** A change to a redundant piece of data must be applied to every occurrence. For example, if a student's address is stored in both an `ENROLMENT` table and a `STUDENT` table, changing the address requires updating potentially many rows across both tables. A missed update leaves the database in an inconsistent state.

- **Deletion Anomaly:** Deleting a row may unintentionally remove data that was the only copy of some other fact. For instance, if course details are stored redundantly within an enrolment record, deleting the last enrolment for a course also deletes the course's name and description.

**c) Describe the purpose of indexing in a relational database. (2 marks)**

An index is an auxiliary data structure (commonly a B⁺-tree) that provides fast access paths to rows based on the values of one or more columns. It sacrifices write performance and storage space to accelerate read operations.

**d) Explain how indexes improve query performance. (4 marks)**

Without an index, the DBMS must perform a *full table scan* — reading every row sequentially from disk to locate those matching a `WHERE` clause. An index allows the DBMS to navigate directly to the relevant disk pages using a balanced-tree search, reducing the search from $O(n)$ to $O(\log n)$ comparisons. For large tables, this translates to orders-of-magnitude fewer disk I/O operations. Indexes also speed up `JOIN` operations by allowing fast lookup of matching foreign keys, and they support efficient `ORDER BY` and `GROUP BY` clauses by scanning the index in sorted order rather than sorting the entire result set.

---

### References

Codd, E. F. (1970). A relational model of data for large shared data banks. *Communications of the ACM*, 13(6), 377–387. https://doi.org/10.1145/362384.362685

Elmasri, R., & Navathe, S. B. (2016). *Fundamentals of Database Systems* (7th ed.). Pearson.
