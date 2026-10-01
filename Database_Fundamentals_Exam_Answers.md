# Database Fundamentals (BCL1223) Final Exam Answers

## Question 1: SQL Creation and Queries

### a) Write a creation script for all THREE (3) tables.

```sql
CREATE TABLE SALESPERSON (
    SalespersonNo CHAR(4) PRIMARY KEY,
    SalespersonName VARCHAR(15),
    Commission NUMBER,
    hireDate DATE
);

CREATE TABLE PRODUCT (
    productNo CHAR(6) PRIMARY KEY,
    productName VARCHAR(20),
    unitPrice NUMBER(8,2)
);

CREATE TABLE SALES (
    salespPersonNo CHAR(4),
    productNo CHAR(6),
    quantity NUMBER,
    PRIMARY KEY (salespPersonNo, productNo),
    FOREIGN KEY (salespPersonNo) REFERENCES SALESPERSON(SalespersonNo),
    FOREIGN KEY (productNo) REFERENCES PRODUCT(productNo)
);
```

### b) Write a SQL statement to display all salespersons sorted by hire date.

```sql
SELECT * FROM SALESPERSON ORDER BY hireDate;
```

### c) Write a SQL statement to display all salespersons with a commission more than 10%.

```sql
SELECT * FROM SALESPERSON WHERE Commission > 10;
```

### d) Write a SQL command to display all salespersons, product number and quantity for products wrench or hammer, sort the result by salesperson.

```sql
SELECT s.SalespersonName, sa.productNo, sa.quantity
FROM SALESPERSON s
JOIN SALES sa ON s.SalespersonNo = sa.salespPersonNo
JOIN PRODUCT p ON sa.productNo = p.productNo
WHERE p.productName IN ('wrench', 'hammer')
ORDER BY s.SalespersonName;
```

### e) Write a SQL command to display salesperson number, salesperson name, product number and quantity sold.

```sql
SELECT s.SalespersonNo, s.SalespersonName, sa.productNo, sa.quantity
FROM SALESPERSON s
JOIN SALES sa ON s.SalespersonNo = sa.salespPersonNo;
```

---

## Question 2: Database Design and Concepts

### a) Describe any THREE (3) basic features of a relational database.

1.  **Data is organized into tables (relations):** Data is stored in two-dimensional tables consisting of rows (tuples) and columns (attributes).
2.  **Primary Keys:** Each table has a primary key that uniquely identifies each record (row) in the table, ensuring data integrity and uniqueness.
3.  **Foreign Keys and Relationships:** Tables can be linked to one another using foreign keys, which establish relationships between different data entities and help maintain referential integrity.

### b) Create an Entity Relationship Diagram (ERD) for the given scenario.

**Entities and Attributes:**
-   `STUDENT` (StudentID (PK), StudentName, Address)
-   `COURSE` (CourseID (PK), CourseName, Credit)
-   `LECTURER` (LecturerID (PK), LecturerName, Phone)

**Relationships and Cardinalities:**
-   A `LECTURER` teaches one or many `COURSE`s (1:M).
-   A `STUDENT` enrolls in one or many `COURSE`s, and a `COURSE` can have many `STUDENT`s (M:N).

**Junction Table:**
-   `ENROLLMENT` (StudentID (FK), CourseID (FK), Grade) — with a composite primary key of (StudentID, CourseID).

*(Note: As a text-based AI, I have provided the textual description required to draw the ERD using any diagramming tool).*

---

## Question 3: Normalization and Anomalies

### a) Normalize the Production Request Form from Unnormalized Form (UNF) to Third Normal Form (3NF).

Let's assume the UNF attributes are: `RequestNo`, `RequestDate`, `StaffNo`, `StaffName`, `ProductNo`, `ProductName`, `QuantityRequired`.

**First Normal Form (1NF):**
Remove repeating groups (assuming a single request can contain multiple products). We introduce a composite key `(RequestNo, ProductNo)`.
`ProductionRequest (RequestNo, RequestDate, StaffNo, StaffName, ProductNo, ProductName, QuantityRequired)`
*(All attributes are now atomic and the primary key is (RequestNo, ProductNo))*

**Second Normal Form (2NF):**
Remove partial dependencies.
-   `StaffName` depends only on `StaffNo`.
-   `ProductName` depends only on `ProductNo`.
-   `RequestDate` depends only on `RequestNo`.

Tables in 2NF:
1.  `STAFF (StaffNo, StaffName)`
2.  `PRODUCT (ProductNo, ProductName)`
3.  `REQUEST (RequestNo, RequestDate, StaffNo)` — StaffNo is a FK to STAFF.
4.  `REQUEST_DETAILS (RequestNo, ProductNo, QuantityRequired)` — RequestNo and ProductNo are composite FKs.

**Third Normal Form (3NF):**
Remove transitive dependencies. In this scenario, there are no apparent transitive dependencies remaining after reaching 2NF, so the design remains the same.
1.  `STAFF (StaffNo (PK), StaffName)`
2.  `PRODUCT (ProductNo (PK), ProductName)`
3.  `REQUEST (RequestNo (PK), RequestDate, StaffNo (FK))`
4.  `REQUEST_DETAILS (RequestNo (PK/FK), ProductNo (PK/FK), QuantityRequired)`

### b) Describe THREE (3) database anomalies and provide examples for each.

1.  **Insertion Anomaly:** Occurs when certain data cannot be inserted into the database without the presence of other data.
    *Example:* In a poorly designed student-course table, you cannot add a new course until at least one student enrolls in it.
2.  **Update Anomaly:** Occurs when redundant data requires updating in multiple places, and failing to update all instances leads to inconsistency.
    *Example:* If a lecturer's phone number is stored in every course record they teach, changing the phone number requires updating multiple records. If only one is updated, the database contains conflicting information.
3.  **Deletion Anomaly:** Occurs when the deletion of a piece of data inadvertently causes the loss of other unrelated data.
    *Example:* If you delete the only student enrolled in a specific course from a combined table, you might lose the information about the course itself (like its credit hours) if it's not stored elsewhere.
