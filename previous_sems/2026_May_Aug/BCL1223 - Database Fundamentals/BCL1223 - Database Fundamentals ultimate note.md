# BCL1223 - Database Fundamentals - Ultimate Note

---

## Chapter1-IntroductiontoDatabase.pdf

### Page 1

SEG education group
Bachelor of Information Technology
Database Systems
BIT1223/BTL1223/BCL1223
Lecture 01 –Introduction to Database

### Page 2

SEG education group
Objectives
• The difference between data and information
• What a database is, what the different types of
databases are, and why they are valuable assets
for decision making
• The importance of database design
• How modern databases evolved from file systems
• About flaws in file system data management
• What the database system’s main components are
and how a database system differs from a file
system
• The main functions of a database management
system (DBMS)
5/18/2026
TSE1044 Database Management Systems

### Page 3

SEG education group
Data vs. Information
• Data:
• Raw facts; building blocks of information
• Unprocessed information
• Information:
• Data processed to reveal meaning
• Data with context
• Accurate, relevant, and timely information is
key to good decision making
• Good decision making is the key to survival in
a global environment

### Page 4

SEG education group
Example
5/18/2026
TSE1044 Database Management Systems
DATA
PROCESSING
INFORMATION
DATA
DATA
44, 70, 55, 87, 69
Ahmad’s score for 6
modules in ICT

### Page 5

SEG education group
Example
5/18/2026
TSE1044 Database Management Systems
DATA
PROCESSING
INFORMATION
DATA
DATA
Selangor, 1234, Siti,
Jalan 7,Ampang,
0155532111, 43000,
Ahmad
Siti Ahmad
1234 , Jalan 7
43000 Ampang, Selangor
015-5532111

### Page 6

SEG education group
Data vs Information
Parameters
Data
Information
Format
Data is in the form of numbers, letters
or a set of characters. Raw data.
Ideas and inferences. Data with
context.
Represented in
It can be structured, tabular data,
graph, data tree, etc.
Language, ideas, and thought
based on the given data
Meaning
Data does not have any specific
purpose
It carries meaning that has been
assigned by interpreting data
Contains
Unprocessed raw factors
Processed in a meaningful way
Dependency
Data depends upon the sources for
collecting data
Information depends upon data
Example
Ticket sales in a band on tour
Sales report by region and venue. It
gives information which venue is
profitable for the business.
5/18/2026
TSE1044 Database Management Systems

### Page 7

SEG education group
What Data to Store
• Type of Data
• Raw data
• Pre-processed
• Compressed
• Frequency of Data Storage for Sensor Data
• Trade off between precision and quantity
• Database — shared, integrated computer
structure that stores:
• End user data (raw facts)
• Metadata (data about data)

### Page 8

SEG education group
Historical Roots: Files and File
Systems
• Managing data with file systems is obsolete
• Understanding file system characteristics makes
database design easier to understand
• Awareness of problems with file systems helps
prevent similar problems in DBMS
• Knowledge of file systems is helpful if you plan to
convert an obsolete file system to a DBMS

### Page 9

SEG education group
Historical Roots: Files and File
Systems
Manual File systems:
• Collection of file folders kept in file cabinet
• Organization within folders based on data’s
expected use (ideally logically related)
• System adequate for small amounts of data with
few reporting requirements
• Finding and using data in growing collections
of file folders became time-consuming and
cumbersome

### Page 10

SEG education group
Historical Roots: Files and File
Systems
Conversion from manual to computer system:
• Could be technically complex, requiring hiring
of data processing (DP) specialists
• Resulted in numerous “home-grown” systems being
created
• Initially, computer files were similar in
design to manual files

### Page 11

Historical Roots: Files and File
Systems

### Page 12

Historical Roots: Files and File
Systems

### Page 13

SEG education group
Historical Roots: Files and File
Systems
• DP specialist wrote programs for reports:
• Monthly summaries of types and amounts of insurance
sold by agents
• Monthly reports about which customers should be
contacted for renewal
• Reports that analyzed ratios of insurance types sold
by agent
• Customer contact letters summarizing coverage

### Page 14

SEG education group
Historical Roots: Files and File
Systems
• Other departments requested databases be
written for them
• SALES database created for sales department
• AGENT database created for personnel department
• As number of databases increased, small file
system evolved
• Each file used its own application programs
• Each file was owned by individual or department
who commissioned its creation

### Page 15

Historical Roots: Files and File
Systems

### Page 16

SEG education group
Example of Early Database Design
(continued)
• As system grew, demand for DP ’ s programming
skills grew
• Additional programmers hired
• DP
specialist
evolved
into
manager,
supervising a DP department
• Primary activity of department (and DP manager)
remained programming

### Page 17

SEG education group
Problems with File System
Data Management
• Every task requires extensive programming in a
third-generation language (3GL)
• Programmer must specify task and how it must be done
• Modern
databases
fourth-generation
languages (4GL)
• Allow users to specify what must be done without
specifying how it is to be done
• Example: DO Loop VS. Select Statement

### Page 18

SEG education group
Problems with File System
Data Management
• Time-consuming, high-level activity
• As
number
files
expands,
system
administration becomes difficult
• Making changes in existing file structure is
difficult
• File structure changes require modifications in
all programs that use data in that file
• Modifications are likely to produce errors,
requiring additional time to “debug” the program
• Security features hard to program and therefore
often omitted

### Page 19

SEG education group
Structural and Data Dependence
• Structural dependence
• Access to a file depends on its structure
• Data dependence
• Changes in the data storage characteristics without
affecting the application program’s ability to access
the data
• Logical data format
• How the human being views the data
• Physical data format
• How the computer “sees” the data

### Page 20

SEG education group
Field Definitions and Naming
Conventions
• Flexible record definition anticipates
reporting requirements by breaking up fields
into their component parts
• Example:
Cutomer Last Name …. Cus-LName

### Page 21

SEG education group
Data Redundancy
• Data redundancy results in data inconsistency
• Different and conflicting versions of the same
data appear in different places
• Errors more likely to occur when complex entries
are made in several different files and/or recur
frequently in one or more files
• Data anomalies develop when required changes in
redundant data are not made successfully

### Page 22

SEG education group
Data Redundancy
Types of data anomalies:
• Update anomalies
• Occur when changes must be made to existing records
• Insertion anomalies
• Occur when entering new records
• Deletion anomalies
• Occur when deleting records

### Page 23

SEG education group
Database Systems
• Problems inherent in file systems make using a
database system desirable
• File system
• Many separate and unrelated files
• Database
• Logically related data stored in a single logical
data repository

### Page 24

Database Systems

### Page 25

SEG education group
The Database System
Environment
• Database system is composed of five main
parts:
• Hardware
• Software
• Operating system software
• DBMS software
• Application programs and utility software
• People
• Procedures
• Data

### Page 26

The Database System Environment

### Page 27

SEG education group
Introduction to Database
Systems
• DBMS (database management system):
• Collection of programs that manages database
structure and controls access to data
• Possible
share
data
among
multiple
applications or users
• Makes data management more efficient and
effective

### Page 28

SEG education group
Basic components of a database
system
In order to convert data into useful information a set of software tools are need, SQL,
Form, etc..

### Page 29

SEG education group
Role and Advantages of the
DBMS
• End users have better access to more and
better-managed data
• Promotes integrated view of organization’s
operations
• Probability of data inconsistency is greatly
reduced
• Possible to produce quick answers to ad hoc
queries

### Page 30

Role and Advantages of the DBMS

### Page 31

SEG education group
Why Database Design is
Important
• Defines the database’s expected use
• Different approach needed for different types
of databases
• Avoid redundant data
• Poorly designed database generates errors
→ leads to bad decisions
→ can lead to failure of organization

### Page 32

SEG education group
DBMS Functions
• DBMS
performs
functions
that
guarantee
integrity and consistency of data
1. Data dictionary management
• defines data elements and their relationships
2. Data storage management
• stores data and related data entry forms, report
definitions, etc.
3. Data transformation and presentation
• translates logical requests into commands to
physically locate and retrieve the requested data
4. Security management
• enforces user security and data privacy within
database

### Page 33

SEG education group
DBMS Functions
5.Multiuser access control
• uses sophisticated algorithms to ensure multiple
users can access the database concurrently without
compromising the integrity of the database
6.Backup and recovery management
• provides backup and data recovery procedures
7.Data integrity management
• promotes and enforces integrity rules
8.Database access languages and application
programming interfaces
• provide data access through a query language
9.Database communication interfaces
• allow database to accept end-user requests via
multiple, different network environments

### Page 34

DBMS Functions

### Page 35

SEG education group
File based Vs Database
File based
Database
1. The data is distributed in
different files and cannot be
shared
1. The data is stored at one place and
can be shared easily
2. The data integrity checks are
difficult to apply on files
2. It provide constraints for data
integrity
3. It provide poor security as data is
widely spread
3. It provide data security
4. It is less complex system
4. It is very complex system
5. The cost is very less than dbms
5. It is costly system and more chance
of failure

### Page 36

SEG education group
Summary
• Data are raw facts. Information is the result
of processing data to reveal its meaning.
• To implement and manage a database, use a
DBMS.
• Database design defines the database
structure.
• A well-designed database facilitates data
management and generates accurate and valuable
information.
• A poorly designed database can lead to bad
decision making, and bad decision making can
lead to the failure of an organization.

### Page 37

SEG education group
Summary (continued)
• Databases were preceded by file systems.
• Limitations of file system data management:
• requires extensive programming
• system administration complex and difficult
• making changes to existing structures is difficult
• security features are likely to be inadequate
• independent files tend to contain redundant data
• DBMS’s were developed to address file systems’
inherent weaknesses

### Page 38

THANK YOU
ANY QUESTIONS?

---

## Chapter2-RelationalModel.pdf

### Page 1

The Relational Model
Chapter Two
DAVID M. KROENKE and DAVID J. AUER
DATABASE CONCEPTS, 7th Edition

### Page 2

Chapter Objectives
• Learn the conceptual foundation of the relational
model
• Understand how relations differ from nonrelational
tables
• Learn basic relational terminology
• Learn the meaning and importance of keys, foreign
keys, and related terminology
• Understand how foreign keys represent
relationships
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall

### Page 3

Relational Data Structure
• Relation – a relation is a table with columns and
rows
• Attribute – an attribute is a named column and rows
• Domain – a domain is the s et of allowable values
for one or more attributes
• Tuple – a tuple is a row of a relation
• Degree – the degree of a relation is the number of
attributes it contains
• Cardinality – the cardinality of a relation is the
number of tuples it contains
• Relational Database - collection of normalized
relations with distinct relation names.

### Page 4

Example of a Relation

### Page 5

Characteristics of a Relation
Rows contain data about an entity.
Columns contain data about attributes of the entity.
Cells of the table hold a single value.
All entries in a column are of the same kind.
Each column has a unique name.
The order of the columns is unimportant.
The order of the rows is unimportant.
No two rows may be identical.
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
EmployeeNumber
FirstName
LastName
Mary
Abernathy
Jerry
Cadley
Alex
Copley
Megan
Jackson

### Page 6

A Nonrelation Example
EmployeeNumber
Phone
LastName
335-6421,
454-9744
Abernathy
215-7789
Cadley
610-9850
Copley
299-9090
Jackson
Cells of the table hold multiple values
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall

### Page 7

Example of a Nonrelational
Table
EmployeeNumber
Phone
LastName
335-6421
Abernathy
215-7789
Cadley
610-9850
Copley
335-6421
Abernathy
299-9090
Jackson
No two rows may be identical
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall

### Page 8

Terminology
Table
Column
File
Record
Field
Relation
Tuple
Attribute
Synonyms…
Figure 2-6:  Equivalent Sets of Terms
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall

### Page 9

Composite Attributes

### Page 10

E-R Diagrams
Rectangles represent entity sets.
Diamonds represent relationship sets.
Lines link attributes to entity sets and entity sets to relationship sets.
Ellipses represent attributes
Double ellipses represent multivalued attributes.
Dashed ellipses denote derived attributes.
Underline indicates primary key attributes (will study later)

### Page 11

E-R Diagram With Composite, Multivalued, and
Derived Attributes

### Page 12

E-R Diagram With Composite, Multivalued, and
Derived Attributes

### Page 13

E-R Diagram With Composite, Multivalued, and
Derived Attributes

### Page 14

A Key
• A key is one (or more) column(s) of a
relation that is (are) used to identify a
row.
2-14
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall

### Page 15

Uniqueness of Keys
2-15
Unique Key
Nonunique Key
Data value is unique
for each row.
Consequently, the
key will uniquely
identify a row.
Data value may be
shared among
several rows.
Consequently, the
key will identify a set
of rows.
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall

### Page 16

A Composite Key
• A composite key is a key that
contains two or more attributes.
• For a key to be unique, it must often
become a composite key.
2-16
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall

### Page 17

Composite Key
Characteristics
• To identify a family member, you
need to know a FamilyID, a
FirstName, and a Suffix (e.g., Jr.).
• The composite key is:
(FamilyID, FirstName, Suffix).
• One needs to know the value of all
three columns to uniquely identify an
individual.
2-17
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall

### Page 18

A Candidate Key
• A candidate key is called “candidate”
because it is a candidate to become
the primary key.
• A candidate key is a unique key.
2-18
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall

### Page 19

A Primary Key
• A primary key is a candidate key
chosen to be the main key for the
relation.
• If you know the value of the primary
key, you will be able to uniquely
identify a single row.
2-19
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall

### Page 20

Relationships Between Tables
• A table may be related to other tables.
• For example
– An Employee works in a Department
– A Manager controls a Project
2-20
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall

### Page 21

A Foreign Key
• To preserve relationships, you may
need to create a foreign key.
• A foreign key is a primary key from
one table placed into another table.
• The key is called a foreign key in the
table that received the key.
2-21
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall

### Page 22

Foreign Key Example I
2-22
Project
ProjID
ProjName
MgrID
Manager
MgrID
MgrName
Foreign Key
Primary Key
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall

### Page 23

Foreign Key Example II
22/9
2-23
Department
DeptID
DeptName
Location
Employee
EmpID
DeptID
EmpName
Foreign Key
Primary Key
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall

### Page 24

Referential Integrity
• Referential integrity states that every
value of a foreign key must match a value
of an existing primary key.
• Example (see previous slide):
– If EmpID = 4 in EMPLOYEE has a DeptID
= 7  (a foreign key), a Department with
DeptID = 7 must exist in DEPARTMENT.
– The primary key value must exist before
the foreign key value is entered.
2-24
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall

### Page 25

Referential Integrity (Cont’d)
• Another perspective…
The value of the Foreign Key EmployeeID
in EQUIPMENT
must exist in
The values of the Primary Key EmployeeID
in EMPLOYEE
2-25
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall

### Page 26

The Null Value
• A Null value means that no data
was entered.
• This is different from a zero, space
character, or tab character.
2-26
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall

### Page 27

The Problem of Null Values
• A Null is often ambiguous.  It could
mean…
– The column value is not appropriate for
the specific row.
– The column value is not decided.
– The column value is unknown.
• Each may have entirely different
implications.
2-27
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall

### Page 28

Functional Dependency
• Functional Dependency—A
relationship between attributes in
which one attribute (or group of
attributes) determines the value of
another attribute in the same table
• Illustration…
– The price of one cookie can determine
the price of a box of 12 cookies.
2-28
(CookiePrice, Qty)
BoxPrice
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall

### Page 29

Determinants
• The attribute (or attributes) that we
use as the starting point (the variable
on the left side of the equation) is
called a determinant.
2-29
(CookiePrice, Qty)
BoxPrice
Determinant
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall

### Page 30

Candidate/Primary Keys
and Functional Dependency
• By definition…
A candidate key of a relation will
functionally determine all other
attributes in the row.
• Likewise, by definition…
A primary key of a relation will
functionally determine all other
attributes in the row.
2-30
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall

### Page 31

Primary Key and Functional
Dependency Example
2-31
(EmployeeID)
(EmpLastName,
EmpPhone)
(ProjectID)
(ProjectName,
StartDate)
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall

### Page 32

END OF CHAPTER 2
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
2-32

---

## Chapter2_1-ERD.pdf

### Page 1

CONCEPTUAL DATA MODELING:
ENTITY RELATIONSHIP DIAGRAM
(ERD)

### Page 2

Entity Relationship Modelling
In This Lecture
• Entity/Relationship models
– Entities and Attributes
– Relationships
– Attributes
– E/R Diagrams

### Page 3

Approaches for data model development
• Top-down Approach
– 3 steps
• identify data entities
• determine attributes of the entities
• determine the nature of the relationships
– usually results in a data model that is well organized but
details can be easily overlooked.
• Bottom-up Approach
• gather information on data used by the organization by...
• group into entities of which these data are attributes
• determine the nature of the relationships
– insures that no important data is overlooked but overall
organization may not be so apparent.

### Page 4

LEVELS IN DATA MODEL

### Page 5

Entity-Relationship Diagrams
• What Is an ERD?
– A picture showing the information created, stored,
and used by a business system.
– ERD is network model that describes stored data
of a system at a high level of abstraction.
– Entities generally represent similar kinds of
information
– Lines drawn between entities show relationships
among the data
– High level business rules are also shown

### Page 6

Entity
• Entities represent objects or
things of interest
– Physical things like students,
lecturers, employees,
products
– More abstract things like
modules, orders, courses,
projects
– noun
• Entities represent objects or
things of interest
– Physical things like students,
lecturers, employees,
products
– More abstract things like
modules, orders, courses,
projects
– noun
PART-TIME
EMPLOYEE
CUSTOMER

### Page 7

Diagramming Entities
• In an E/R Diagram, an
entity is usually drawn as
a box with rounded
corners
• The box is labelled with
the name of the class of
objects represented by
that entity
Student
Lecturer
Module
Tutors
Studies
Course
Name

### Page 8

Entity Relationship Modelling
Attributes
• Attributes are facts, aspects,
properties, or details about
an entity
– Students have IDs, names,
courses, addresses, …
– Modules have codes, titles,
credit weights, levels, …
• Attributes have
– A name
– An associated entity
– Domains of possible values
– Values from the domain for
each instance of the entity
they are belong to

### Page 9

Entity Relationship Modelling
Diagramming Attributes
• In an E/R Diagram attributes
may be drawn as ovals
• Each attribute is linked to its
entity by a line
• The name of the attribute is
written in the oval
Student
Lecturer
Module
Tutors
Studies
Course
Name

### Page 10

Types of Attributes
• Simple:
• Each entity has a single atomic value for the attribute, for example SSN,
CourseNo.
• Composite:
•  The attribute may be composed of several components
• Multivalued:
•  An entity may have multiple values for that attribute; for example Color
of a Car or PreviousDegrees of a Student
• Derived:
•  The domain value of attribute can be determined from one or more other
attributes.

### Page 11

Nested attribute
In general, composite and multiple-valued attributes may
be nested arbitrarily to any number of levels although
this is rare.
Address
Street
Address
City
Post Code
District
Number
Street
House
Number

### Page 12

Entity Relationship Modelling
Relationships
• Relationships are an
association between two or
more entities
– Each Student takes several
Modules
– Each Module is taught by a
Lecturer
– Each Employee works for a
single Department
• Relationships have
– A name
– A set of entities that
participate in them
– A degree - the number of
entities that participate (most
have degree 2)
– A cardinality ratio

### Page 13

Unary or Recursive Relationships
PERSON
Married
EMPLOYEE
Manages
1-TO-1
1-TO-MANY
A relationship where the same entity
participates more than once in a different
roles.
Staff
Supervises
Supervisee
Supervisor

### Page 14

Ternary Relationships
VENDOR
WAREHOUSE
Ships
PART

### Page 15

Relationship
• A Relationship Type is a relevant business association
between two Entity Types.
• A Relationship is an occurrence of a relationship type.
Finance
Marketing
Ahmad Al ghoul
Osama Mlkawi
Yosef Ali
employs
employs
employs
DEPT
EMPLOYEE
employs
employs

### Page 16

Entity Relationship Modelling
Cardinality Ratios
• Each entity in a relationship
can participate in zero, one,
or more than one instances
of that relationship
• This leads to 3 types of
relationship…
• One to one (1:1)
– Each lecturer has a unique office
• One to many (1:M)
– A lecturer may tutor many
students, but each student has
just one tutor
• Many to many (M:M)
– Each student takes several
modules, and each module is
taken by several students

### Page 17

Cardinality
EMPLOYEE
PARKING
SPOT
given
PRODUCT
LINE
PRODUCT
Contains
STUDENT
COURSE
Enrol
1-TO-1
1-TO-MANY
MANY-TO-MANY

### Page 18

Entity Relationship Modelling
Diagramming Relationships
• Relationships are links
between two entities
• The name is given in a
diamond box
• The ends of the link show
cardinality
Student
Lecturer
Module
Tutors
Studies
Course
Name
Many

### Page 19

Cardinality: Example

### Page 20

Entity Relationship Modelling
Removing M:M Relationships
• Many to many relationships
are difficult to represent
• We can split a many to
many relationship into two
one to many relationships
• An entity represents the
M:M relationship
Student
Module
Studies
Enrolment
Student
Module

### Page 21

Removing M:M Relationships

### Page 22

ERD: Crow’s Foot
Crow's foot notation is a common method of indicating cardinality. The
four examples show how you can use various symbols to describe the
relationships between entities.

### Page 23

ERD: Chen Notation

### Page 24

Entity Relationship Modelling
Making E/R Models
• To make an E/R model you
need to identify
– Enitities
– Attributes
– Relationships
– Cardinality ratios
• from a description
• General guidelines
– Since entities are things or
objects they are often nouns
in the description
– Attributes are facts or
properties, and so are often
nouns also
– Verbs often describe
relationships between
entities

### Page 25

Entity Relationship Modelling
Example
A university consists of a number of departments. Each
department offers several courses. A number of modules
make up each course. Students enrol in a particular course
and take modules towards the completion of that course.
Each module is taught by a lecturer from the appropriate
department, and each lecturer tutors a group of students

### Page 26

Entity Relationship Modelling
Example - Entities
A university consists of a number of departments. Each
department offers several courses. A number of modules
make up each course. Students enrol in a particular course
and take modules towards the completion of that course.
Each module is taught by a lecturer from the appropriate
department, and each lecturer tutors a group of students

### Page 27

Entity Relationship Modelling
Example - Relationships
•  A university consists of a number of departments. Each
department offers several courses. A number of modules
make up each course. Students enrol in a particular course
and take modules towards the completion of that course.
Each module is taught by a lecturer from the appropriate
department, and each lecturer tutors a group of students

### Page 28

Entity Relationship Modelling
Example - E/R Diagram
Module
Course
Department
Student
Lecturer
Entities: Department, Course, Module, Lecturer, Student

### Page 29

Entity Relationship Modelling
Example - E/R Diagram
Module
Course
Department
Student
Lecturer
Offers
Each department offers several courses

### Page 30

Entity Relationship Modelling
Example - E/R Diagram
Module
Course
Department
Student
Lecturer
Includes
Offers
A number of modules make up each courses

### Page 31

Entity Relationship Modelling
Example - E/R Diagram
Module
Course
Department
Student
Lecturer
Includes
Offers
Enrols In
Students enrol in a particular course

### Page 32

Entity Relationship Modelling
Example - E/R Diagram
Module
Course
Department
Student
Lecturer
Includes
Offers
Enrols In
Takes
Students … take modules

### Page 33

Entity Relationship Modelling
Example - E/R Diagram
Module
Course
Department
Student
Lecturer
Includes
Offers
Enrols In
Takes
Teaches
Each module is taught by a lecturer

### Page 34

Entity Relationship Modelling
Example - E/R Diagram
Module
Course
Department
Student
Lecturer
Includes
Offers
Enrols In
Takes
Employs
Teaches
a lecturer from the appropriate department

### Page 35

Entity Relationship Modelling
Example - E/R Diagram
Module
Course
Department
Student
Lecturer
Includes
Offers
Tutors
Enrols In
Takes
Employs
Teaches
each lecturer tutors a group of students

### Page 36

Entity Relationship Modelling
Example - E/R Diagram
Module
Course
Department
Student
Lecturer
Includes
Offers
Tutors
Enrols In
Takes
Employs
Teaches

### Page 37

Entity-Relationship Diagrams
In the first example of cardinality notation,
one and only one CUSTOMER can place
anywhere from zero to many of the ORDER
entity.
In the second example, one and only one
ORDER can include one ITEM ORDERED or
many.
In the third example, one and only one
EMPLOYEE can have one SPOUSE or none.
In the fourth example, one EMPLOYEE, or
many employees, or none, can be assigned
to one PROJECT, or many projects, or
none.

### Page 38

Example ERD

### Page 39

Entity Relationship Modelling
ERD EXERCISE 1
A university consists of a number of
departments. Each department offers several
courses. A number of modules make up each
course. Students enrol in a particular course
and take modules towards the completion of
that course. Each module is taught by a
lecturer from the appropriate department, and
each lecturer tutors a group of students
(erd2)

### Page 40

ERD EXERCISE 2
Prepare an ERD for a real estate firm that lists property for sale. The following
describes this organization:
The firm has a number of sales offices in several states. Attributes of sales office
include Office_Number(identifier) and Location
Each sales office is assigned one or more employees. Attributes of employee
include Employee_ID(identifier) and Employee_Name. An employee must be
assigned to only one sales office.
For each sales office, there is always one employee assigned to manage that office.
An employee may manage only the sales office to which he/she is assigned.
The firm lists property for sale. Attributes of property include
Property_ID(identifier) and Location. Components of Location include Address,
City, State and Zip_Code.
Each unit of property must be listed with one (and only one) of the sales offices. A
sales office may have any number of properties listed, or may have no properties
listed.
Each unit of property has one or more owners. Attributes of owners are
Owner_ID(identifier) and Owner_Name. An owner may own one or more units of
property. An attribute of the relationship between property and owner is
Percent_Owned.

### Page 42

Exercise 3
Pick and Shovel Construction Company is a
multi-state building contractor specializing in
medium-priced town homes. Assume that Pick
and Shovel’s main entities are its customers,
employees, projects and equipment. A customer
can hire the company for more than one project,
and employees sometimes work on more than
one project at a time. Equipment, however, is
assigned to only one project at a time. Draw a
complete ERD showing those entities.

---

## Chapter3-DatabaseDesign.pdf

### Page 1

DATABASE SYSTEM

### Page 2

CHAPTER 3 & 4
DATABASE DESIGN
Data and Entity-Relationship Model (ER
MODEL)

### Page 3

Entity-Relationship Model
• Entity Sets √
• Relationship Sets
• Design Issues
• Mapping Constraints
• Keys
• E-R Diagram
• Extended E-R Features
• Design of an E-R Database Schema
• Reduction of an E-R Schema to Tables

### Page 4

Entity Sets
• A database can be modeled as:
• a collection of entities,
• relationship among entities.
• An entity is an object that exists and is distinguishable
from other objects.
• Example:  specific person, company, event, plant
• Entities have attributes
• Example: people have names and addresses
• An entity set is a set of entities of the same type that
share the same properties.
• Example: set of all persons, companies, trees, holidays

### Page 5

Entity Sets customer and loan
customer-id   customer-  customer-  customer-           loan-
amount
name     street         city                    number

### Page 6

Attributes
• An entity is represented by a set of attributes, that is
descriptive properties possessed by all members of an
entity set.
• Domain – the set of permitted values for each attribute
• Attribute types:
• Simple and composite attributes.
• Single-valued and multi-valued attributes
• E.g. multivalued attribute: phone-numbers
• Derived attributes
• Can be computed from other attributes
• E.g.  age, given date of birth
Example:
customer = (customer-id, customer-name,
customer-street, customer-city)
loan = (loan-number, amount)

### Page 7

Composite Attributes

### Page 8

Relationship Sets
• A relationship is an association among several entities
Example:
Hayes
depositor
A-102
customer entityrelationship setaccount entity
• A relationship set is a mathematical relation among n 
2 entities, each taken from entity sets
{(e1, e2, … en) | e1   E1, e2   E2, …, en 
where (e1, e2, …, en) is a relationship
• Example:
(Hayes, A-102)  depositor

### Page 9

Relationship Set borrower

### Page 10

Relationship Sets (Cont.)
• An attribute can also be property of a relationship set.
• For instance, the depositor relationship set between entity sets
customer and account may have the attribute access-date

### Page 11

Degree of a Relationship Set
• Refers to number of entity sets that participate in a
relationship set.
• Relationship sets that involve two entity sets are binary
(or degree two).  Generally, most relationship sets in a
database system are binary.
• Relationship sets may involve more than two entity sets.
• Relationships between more than two entity sets are
rare.  Most relationships are binary. (More on this later.)
HE.g.  Suppose employees of a bank may have jobs
(responsibilities) at multiple branches, with different jobs at
different branches.  Then there is a ternary relationship set
between entity sets employee,  job and branch

### Page 12

Mapping Cardinalities
• Express the number of entities to which another
entity can be associated via a relationship set.
• Most useful in describing binary relationship sets.
• For a binary relationship set the mapping cardinality
must be one of the following types:
• One to one
• One to many
• Many to one
• Many to many

### Page 13

Mapping Cardinalities
One to one
One to many
Note: Some elements in A and B may not be mapped to any
elements in the other set

### Page 14

Mapping Cardinalities
Many to one
Many to many
Note: Some elements in A and B may not be mapped to any
elements in the other set

### Page 15

Mapping Cardinalities affect ER Design
Can make access-date an attribute of account, instead of a
relationship attribute, if each account can have only one customer
n I.e., the relationship from account to customer is many to one,
or equivalently, customer to account is one to many

### Page 16

E-R Diagrams
Rectangles represent entity sets.
Diamonds represent relationship sets.
Lines link attributes to entity sets and entity sets to relationship sets.
Ellipses represent attributes
n Double ellipses represent multivalued attributes.
n Dashed ellipses denote derived attributes.
Underline indicates primary key attributes (will study later)

### Page 17

E-R Diagram With Composite, Multivalued, and Derived
Attributes

### Page 18

Relationship Sets with Attributes

### Page 19

Roles
• Entity sets of a relationship need not be distinct
• The labels “manager” and “worker” are called roles; they specify how
employee entities interact via the works-for relationship set.
• Roles are indicated in E-R diagrams by labeling the lines that connect
diamonds to rectangles.
• Role labels are optional, and are used to clarify semantics of the
relationship

### Page 20

Cardinality Constraints
• We express cardinality constraints by drawing either a
directed line (→), signifying “one,” or an undirected line (—
), signifying “many,” between the relationship set and the
entity set.
• E.g.: One-to-one relationship:
• A customer is associated with at most one loan via the relationship
borrower
• A loan is associated with at most one customer via borrower

### Page 21

One-To-Many Relationship
• In the one-to-many relationship a loan is associated
with at most one customer via borrower, a customer is
associated with several (including 0) loans via borrower

### Page 22

Many-To-One Relationships
• In a many-to-one relationship a loan is associated with
several (including 0) customers via borrower, a
customer is associated with at most one loan via
borrower

### Page 23

Many-To-Many Relationship
• A customer is associated with several (possibly
0) loans via borrower
• A loan is associated with several (possibly 0)
customers via borrower

### Page 24

Participation of an Entity Set in a Relationship Set
Total participation (indicated by double line):  every entity in the entity
set participates in at least one relationship in the relationship set
n E.g. participation of loan in borrower is total
n  every loan must have a customer associated to it via borrower
Partial participation:  some entities may not participate in any
relationship in the relationship set
n E.g. participation of customer in borrower is partial

### Page 25

Alternative Notation for Cardinality Limits
Cardinality limits can also express participation constraints

### Page 26

Keys
• A super key of an entity set is a set of one or more
attributes whose values uniquely determine each
entity.
• A candidate key of an entity set is a minimal super
• Customer-id is candidate key of customer
• account-number is candidate key of account
• Although several candidate keys may exist, one of
the candidate keys is selected to be the primary
key.

### Page 27

Keys for Relationship Sets
• The combination of primary keys of the participating entity
sets forms a super key of a relationship set.
• (customer-id, account-number) is the super key of depositor
• NOTE:  this means a pair of entity sets can have at most one
relationship in a particular relationship set.
• E.g. if we wish to track all access-dates to each account by each
customer, we cannot assume a relationship for each access.  We can
use a multivalued attribute though
• Must consider the mapping cardinality of the relationship
set when deciding the what are the candidate keys
• Need to consider semantics of relationship set in selecting
the primary key  in case of more than one candidate key

### Page 28

E-R Diagram with a Ternary Relationship

### Page 29

EXERCISE
Create an ER diagram for each of the following descriptions:
a) Each company operates four departments, and each
department belongs to one company.
b) Each department in part (a) employs one or more
employees, and each employee works for one
department.
c) Each of the employees in part (b) may or may not have
one or more dependants, and each dependant belongs to
one employee.
d) Each employee in part (c) may or may not have an
employment history.
e) Represent all the ER diagrams described in (a), (b), (c),
and (d) as a single ER diagram.

### Page 30

Cardinality Constraints on Ternary
Relationship
• We allow at most one arrow out of a ternary (or greater
degree) relationship to indicate a cardinality constraint
• E.g. an arrow from works-on to job indicates each
employee works on at most one job at any branch.
• If there is more than one arrow, there are two ways of
defining the meaning.
• E.g a ternary relationship R between A, B and C with arrows to B
and C could mean
• 1.  each A entity is associated with a unique entity from B and C or
• 2.  each pair of entities from (A, B) is associated with a unique C
entity,
and each pair (A, C) is associated with a unique B
• Each alternative has been used in different formalisms
• To avoid confusion we outlaw more than one arrow

### Page 31

Binary Vs. Non-Binary Relationships
• Some relationships that appear to be non-binary may be
better represented using binary relationships
• E.g.  A ternary relationship parents, relating a child to his/her father
and mother, is best replaced by two binary relationships,  father
and mother
• Using two binary relationships allows partial information (e.g. only
mother being know)
• But there are some relationships that are naturally non-binary
• E.g. works-on

### Page 32

Converting Non-Binary Relationships to Binary Form
• In general, any non-binary relationship can be represented using binary
relationships by creating an artificial entity set.
• Replace R between entity sets A, B and C by an entity set E, and three relationship
sets:
1. RA, relating E and A
2.RB, relating E and B
3. RC, relating E and C
• Create a special identifying attribute for E
• Add any attributes of R to E
• For each relationship (ai , bi , ci) in R, create
1. a new entity ei in the entity set E       2. add (ei , ai ) to RA
3. add (ei , bi ) to RB
4. add (ei , ci ) to RC

### Page 33

Converting Non-Binary Relationships
(Cont.)
• Also need to translate constraints
• Translating all constraints may not be possible
• There may be instances in the translated schema that
cannot correspond to any instance of R
• Exercise:  add constraints to the relationships RA, RB and RC to ensure
that a newly created entity corresponds to exactly one entity in each of
entity sets A, B and C
• We can avoid creating an identifying attribute by making E a weak
entity set (described shortly) identified by the three relationship
sets

### Page 34

STUDENT
SUBJECT
enrol
studentID
Name
gender
subjectCode
Name
Credit
STUDENT
SUBJECT
ENROLLMENT
studentID
Name
gender
subjectCode
Name
Credit
studentID
subjectCode
Marks
grade

### Page 35

Design Issues
• Use of entity sets vs. attributes
Choice mainly depends on the structure of the enterprise
being modeled, and on the semantics associated with the
attribute in question.
• Use of entity sets vs. relationship sets
Possible guideline is to designate a relationship set to
describe an action that occurs between entities
• Binary versus n-ary relationship sets
Although it is possible to replace any nonbinary (n-ary, for n >
2) relationship set by a number of distinct binary relationship
sets, a n-ary relationship set shows more clearly that several
entities participate in a single relationship.
• Placement of relationship attributes

### Page 36

Weak Entity Sets
• An entity set that does not have a primary key is referred
to as a weak entity set.
• The existence of a weak entity set depends on the
existence of a identifying entity set
•  it must relate to the identifying entity set via a total, one-to-many
relationship set from the identifying to the weak entity set
• Identifying relationship depicted using a double diamond
• The discriminator (or partial key) of a weak entity set is
the set of attributes that distinguishes among all the
entities of a weak entity set.
• The primary key of a weak entity set is formed by the
primary key of the strong entity set on which the weak
entity set is existence dependent, plus the weak entity
set’s discriminator.

### Page 37

Weak Entity Sets (Cont.)
• We depict a weak entity set by double rectangles.
• We underline the discriminator of a weak entity set  with a
dashed line.
• payment-number – discriminator of the payment entity set
• Primary key for payment – (loan-number, payment-number)

### Page 38

Weak Entity Sets (Cont.)
• Note: the primary key of the strong entity set is not
explicitly stored with the weak entity set, since it is
implicit in the identifying relationship.
• If loan-number were explicitly stored, payment could be
made a strong entity, but then the relationship between
payment and loan would be duplicated by an implicit
relationship defined by the attribute loan-number
common to payment and loan

### Page 39

More Weak Entity Set Examples
• In a university, a course is a strong entity and a course-
offering can be modeled as a weak entity
• The discriminator of course-offering would be semester
(including year) and section-number (if there is more than one
section)
• If we model course-offering as a strong entity we would
model course-number as an attribute.
Then the relationship with course would be implicit in the
course-number attribute

### Page 40

Specialization
• Top-down design process; we designate subgroupings
within an entity set that are distinctive from other entities
in the set.
• These subgroupings become lower-level entity sets that
have attributes or participate in relationships that do not
apply to the higher-level entity set.
• Depicted by a triangle component labeled ISA (E.g.
customer “is a” person).
• Attribute inheritance – a lower-level entity set inherits
all the attributes and relationship participation of the
higher-level entity set to which it is linked.

### Page 41

Specialization Example

### Page 42

Generalization
• A bottom-up design process – combine a number of entity
sets that share the same features into a higher-level entity
set.
• Specialization and generalization are simple inversions of
each other; they are represented in an E-R diagram in the
same way.
• The terms specialization and generalization are used
interchangeably.

### Page 43

Specialization and Generalization
(Contd.)
• Can have multiple specializations of an entity set based
on different features.
• E.g. permanent-employee vs. temporary-employee, in
addition to officer vs. secretary vs. teller
• Each particular employee would be
• a member of one of permanent-employee or temporary-
employee,
• and also a member of one of officer, secretary, or teller
• The ISA relationship also referred to as superclass -
subclass relationship

### Page 44

Design Constraints on a
Specialization/Generalization
• Constraint on which entities can be members of a
given lower-level entity set.
• condition-defined
• E.g. all customers over 65 years are members of senior-citizen
entity set; senior-citizen ISA  person.
• user-defined
• Constraint on whether or not entities may belong to
more than one lower-level entity set within a single
generalization.
• Disjoint
• an entity can belong to only one lower-level entity set
• Noted in E-R diagram by writing disjoint next to the ISA triangle
• Overlapping
• an entity can belong to more than one lower-level entity set

### Page 45

Design Constraints on a
Specialization/Generalization (Contd.)
• Completeness constraint -- specifies whether or not an
entity in the higher-level entity set must belong to at
least one of the lower-level entity sets within a
generalization.
• total : an entity must belong to one of the lower-level entity sets
• partial: an entity need not belong to one of the lower-level entity
sets

### Page 46

Aggregation
n Consider the ternary relationship works-on, which we saw earlier
n Suppose we want to record managers for tasks performed by an
employee at a branch

### Page 47

Aggregation (Cont.)
• Relationship sets works-on and manages represent
overlapping information
• Every manages relationship corresponds to a works-on relationship
• However, some works-on relationships may not correspond to any
manages relationships
• So we can’t discard the works-on relationship
• Eliminate this redundancy via aggregation
• Treat relationship as an abstract entity
• Allows relationships between relationships
• Abstraction of relationship into new entity
• Without introducing redundancy, the following diagram
represents:
• An employee works on a particular job at a particular branch
• An employee, branch, job combination may have an associated
manager

### Page 48

E-R Diagram With Aggregation

### Page 49

E-R Design Decisions
• The use of an attribute or entity set to represent an object.
• Whether a real-world concept is best expressed by an
entity set or a relationship set.
• The use of a ternary relationship versus a pair of binary
relationships.
• The use of a strong or weak entity set.
• The use of specialization/generalization – contributes to
modularity in the design.
• The use of aggregation – can treat the aggregate entity
set as a single unit without concern for the details of its
internal structure.

### Page 50

E-R Diagram for a Banking Enterprise

### Page 51

Summary of Symbols Used in E-R
Notation

### Page 52

Summary of Symbols (Cont.)

### Page 53

Alternative E-R Notations

### Page 54

Representing Entity Sets as Tables
• A strong entity set reduces to a table with the same
attributes.

### Page 55

Composite and Multivalued Attributes
• Composite attributes are flattened out by creating a
separate attribute for each component attribute
• E.g. given entity set customer with composite attribute name with
component attributes first-name and last-name the table
corresponding to the entity set has two attributes
name.first-name  and name.last-name
• A multivalued attribute M of an entity E is represented by a
separate table EM
• Table EM has attributes corresponding to the primary key of E and
an attribute corresponding to multivalued attribute M
• E.g.  Multivalued attribute dependent-names of employee is
represented by a table
employee-dependent-names( employee-id, dname)
• Each value of the multivalued attribute maps to a separate row of
the table EM
• E.g.,  an employee entity with primary key  John and
dependents  Johnson and Johndotir maps to two rows:
(John, Johnson) and (John, Johndotir)

### Page 56

Representing Weak Entity Sets
A weak entity set becomes a table that includes a column for
the primary key of the identifying strong entity set

### Page 57

Representing Relationship Sets as
Tables
• A many-to-many relationship set is represented as a table with
columns for the primary keys of the two participating entity sets,
and any descriptive attributes of the relationship set.
• E.g.: table for relationship set borrower

### Page 58

Redundancy of Tables
Many-to-one and one-to-many relationship sets that are total
on the many-side can be represented by adding an extra
attribute to the many side, containing the primary key of the
one side
E.g.: Instead of creating a table for relationship account-
branch, add an attribute branch to the entity set account

### Page 59

Redundancy of Tables (Cont.)
• For one-to-one relationship sets, either side can be
chosen to act as the “many” side
• That is, extra attribute can be added to either of the tables
corresponding to the two entity sets
• If participation is partial on the many side, replacing a
table by an extra attribute in the relation corresponding to
the “many” side could result in null values
• The table corresponding to a relationship set linking a
weak entity set to its identifying strong entity set is
redundant.
• E.g. The payment table already contains the information that would
appear in the loan-payment table (i.e., the columns loan-number
and payment-number).

### Page 60

Representing Specialization as Tables
• Method 1:
• Form a table for the higher level entity
• Form a table for each lower level entity set, include primary key of
higher level entity set and local attributes
table    table attributes
personname, street, city
customer
name, credit-rating
employee
name, salary
• Drawback:  getting information about, e.g., employee requires
accessing two tables

### Page 61

Representing Specialization as Tables
(Cont.)
• Method 2:
• Form a table for each entity set with all local and inherited attributes
table
table attributes
personname, street, city
customer
name, street, city, credit-rating
employee
name, street, city, salary
• If specialization is total, table for generalized entity (person) not
required to store information
• Can be defined as a “view” relation containing union of
specialization tables
• But explicit table may still be needed for foreign key constraints
• Drawback:  street and city may be stored redundantly for persons
who are both customers and employees

### Page 62

Relations Corresponding to
Aggregation
n To represent aggregation, create a table containing
n  primary key of the aggregated relationship,
n the primary key of the associated entity set
n Any descriptive attributes

### Page 63

Relations Corresponding to
Aggregation (Cont.)
n E.g. to represent aggregation manages between relationship
works-on and entity set manager, create a table
manages(employee-id, branch-name, title, manager-name)
n Table works-on is redundant provided we are willing to store
null values for attribute manager-name in table manages

---

## Chapter4-DataModelingandEntity-RelationshipModel.pdf

### Page 1

Data Modeling and the
Entity-Relationship Model
Chapter Four
DAVID M. KROENKE and DAVID J. AUER
DATABASE CONCEPTS, 6th Edition

### Page 2

Chapter Objectives
• Learn the basic stages of database development
• Understand the purpose and role of a data model
• Know the principal components of the E-R data
model
• Understand how to interpret traditional E-R
diagrams
• Understand how to interpret the Information
Engineering (IE) model’s Crow’s Foot E-R
diagrams
• Learn to construct E-R diagrams
• Know how to represent 1:1, 1:N, N:M, and binary
relationships with the E-R model
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 3

Chapter Objectives
(Cont’d)
• Understand two types of weak entities and know
how to use them
• Understand nonidentifying and identifying
relationships and know how to use them
• Know how to represent subtype entities with the
E-R model
• Know how to represent recursive relationships
with the E-R model
• Learn how to create an E-R diagram from source
documents
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 4

Three Stages of
Database Development
• The three stages of database development
are:
– Requirements Analysis Stage
– Component Design Stage
– Implementation Stage
• These three stages are part of the five
stage Systems Development Life Cycle
(SDLC) model
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 5

The Requirements Analysis Stage
• Sources of requirements
– User Interviews
– Forms
– Reports
– Queries
– Use Cases
– Business Rules
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 6

Requirements Become the
E-R Data Model
• After the requirements have been
gathered, they are transformed into
an Entity Relationship (E-R) Data
Model.
• The most important elements of E-R
Models are:
– Entities
– Attributes
– Identifiers
– Relationships
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 7

Entity Class versus Entity Instance
• An entity class is a description of
the structure and format of the
occurrences of the entity.
• An entity instance is a specific
occurrence of an entity within an
entity class.
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 8

Entity Class and Entity Instance
Figure 4-2: The ITEM Entity and Two Entity Instances
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 9

Attributes
• Entities have attributes that
describe the entity’s characteristics:
– ProjectName
– StartDate
– ProjectType
– ProjectDescription
• Attributes have a data type and
properties.
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 10

Identifiers
• Entity instances have identifiers.
• An identifier will identify a particular
instance in the entity class:
– SocialSecurityNumber
– StudentID
– EmployeeID
4-10
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 11

Identifier Types
• Uniqueness
– Identifiers may be unique or nonunique.
– If the identifier is unique, the data value for the
identifier must be unique for all instances.
• Composite
– A composite identifier consists of two or
more attributes.
• E.g., OrderNumber & LineItemNumber are both
required.
4-11
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 12

Levels of Entity Attribute Display
4-12
Figure  4-3: Levels of Entity Attribute Display
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 13

Relationships
• Entities can be associated with one
another in relationships.
• Relationship degree defines the
number of entity classes participating
in the relationship:
– Degree 2 is a binary relationship.
– Degree 3 is a ternary relationship.
4-13
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 14

Degree 2 Relationship:
Binary
4-14
Figure 4-4: Example Relationships
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 15

Degree 3 Relationship:
Ternary
4-15
Figure 4-4:  Example Relationships
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 16

One-to-One Binary Relationship
• 1:1 (one-to-one)
– A single entity instance in one entity class is
related to a single entity instance in another
entity class.
• An employee may have no more than one locker;
• A locker may only be accessible by one employee
4-16
(a) One-to-One Relationship
Figure 4-5:  Three Types of  Binary Relationships
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 17

One-to-Many Binary Relationship
• 1:N (one-to-many)
– A single entity instance in one entity class is
related to many entity instances in another
entity class.
• A quotation is associated with only one item; and
• An item may have several quotations
4-17
(b) One-to-Many Relationship
Figure 4-4: Three Types of  Binary Relationships
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 18

Many-to-Many Binary Relationship
• N:M (many-to-many)
– Many entity instances in one entity class is
related to many entity instances in another
entity class:
• a supplier may supply several items; and
• a particular item may be supplied by several
suppliers.
4-18
(c) Many-to-Many Relationship
Figure 4-5:  Three Types of Binary Relationships
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 19

Maximum Cardinality
• Relationships are named and classified by
their cardinality, which is a word that
means count.
• Each of the three types of binary
relationships shown above have different
maximum cardinalities.
• Maximum cardinality is the maximum
number of entity instances that may
participate in a relationship instance—
one, many, or some other fixed number.
4-19
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 20

Minimum Cardinality
• Minimum cardinality is the
minimum number of entity instances
that must participate in a relationship
instance.
• These values typically assume a
value of zero (optional) or one
(mandatory).
4-20
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 21

Cardinality Example
• Maximum cardinality is many for both ITEM and
SUPPLIER.
• Minimum cardinality is zero (optional) for ITEM
and one (mandatory) SUPPLIER.
– A SUPPLIER does not have to supply an ITEM.
– An ITEM must have a SUPPLIER.
4-21
Figure 4-6:  A Relationship with Minimum Cardinalities
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 22

Entity-Relationship Diagrams
• The diagrams in previous slides are called
entity-relationship diagrams.
– Entity classes are shown by rectangles.
– Relationships are shown by diamonds.
– The maximum cardinality of the relationship is
shown inside the diamond.
– The minimum cardinality is shown by the oval
or hash mark next to the entity.
– The name of the entity is shown inside the
rectangle.
– The name of the relationship is shown near
the diamond.
4-22
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 23

HAS-A Relationships
• The relationships in the previous
slides are called HAS-A
relationships.
• The term is used because each
entity instance has a relationship to a
second entity instance:
– An employee has a badge.
– A badge has an employee.
4-23
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 24

Types of
Entity-Relationship Diagrams
• Information Engineering (IE) [James Martin
1990]—Uses “crow’s feet” to show the many sides
of a relationship, and it is sometimes called the
crow’s foot model.
• Integrated Definition 1, Extended 3 (IDEF1X) is
a version of the E-R model that is a national
standard.
• Unified Modeling Language (UML) is a set of
structures and techniques for modeling and
designing object-oriented programs (OOP) and
applications
4-24
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 25

Crow’s Foot Example:
One-to-Many Relationship
4-25
Figure 4-7:  Two Versions of a 1:N Relationship
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 26

Crow’s Foot Symbols
4-26
Figure 4-8:  Crow’s Foot Notation
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 27

Crow’s Foot Example:
Many-to-Many Relationship
4-27
Figure 4-9:  Two Versions of an N:M Relationship
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 28

Weak Entity
• A weak entity is an entity that cannot
exist in the database without the existence
of another entity.
• Any entity that is not a weak entity is
called a strong entity.
4-28
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 29

ID-Dependent Weak Entities
• An ID-Dependent weak entity is a
weak entity that cannot exist without
its parent entity.
• An ID-dependent weak entity has a
composite identifier.
– The first part of the identifier is the
identifier for the strong entity.
– The second part of the identifier is the
identifier for the weak entity itself.
4-29
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 30

ID-Dependent Weak Entity
Examples
4-30
Figure 4-10:  Example ID-Dependent Entities
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 31

Weak Entity Relationships
• The relationship between a strong and
weak entity is termed an identifying
relationship if the weak entity is ID-
dependent.
– Represented by a solid line
• The relationship between a strong and
weak entity is termed a nonidentifying
relationship if the weak entity is non-ID-
dependent.
– Represented by a dashed line
– Also used between strong entities
4-31
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 32

Weak Entity Identifier:
Non-ID-dependent
• All ID-dependent entities are weak
entities, but there are other entities
that are weak but not ID-dependent.
• A non-ID-dependent weak entity may
have a single or composite identifier,
but the identifier of the parent entity
will be a foreign key.
4-32
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 33

Non-ID-Dependent Weak Entity
Examples
4-33
Figure 4-11:  Weak Entity Examples
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 34

Strong and Weak Entity Examples
4-34
Figure 4-12:  Examples of Required Entities
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 35

Associative Entities
• An associative entity (also called an
association entity) is used when there are
attributes that are associated with the relationship
between two entities rather than with either of the
two entities themselves.
• A new entity is then created to:
– Link the two original entities
– Hold the attributes
4-35
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 36

Associative Entities (Cont’d)
4-36
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
Figure 4-13:  The Associative Entity

### Page 37

Subtype Entities
• A subtype entity is a special case of another
entity called supertype.
• An attribute of the supertype may be included
that indicates which of the subtypes is
appropriate for a given instance; this attribute is
called a discriminator.
• Subtypes can be exclusive or inclusive.
– If exclusive, the supertype relates to at most one
subtype.
– If inclusive, the supertype can relate to one or
more subtypes.
4-37
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 38

Subtype Entity Identifiers
• The relationships that connect supertypes
and subtypes are called IS-A
relationships because a subtype is the
same entity as the supertype.
• The identifier of a supertype and all of its
subtypes is the same attribute.
4-38
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 39

Subtype Entity Examples
4-39
Figure 4-14:  Example Subtype Entities
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 40

Recursive Relationships
• It is possible for an entity to have a
relationship to itself—this is called a
recursive relationship.
4-40
Figure 4-15:
Example Recursive Relationship
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 41

Developing an E-R Diagram
• Heather Sweeney Designs will be used as
an ongoing example throughout Chapters
4, 5, 6 and 7.
– Heather Sweeney is an interior designer who
specializes in home kitchen design.
– She offers a variety of free seminars at home
shows, kitchen and appliance stores and other
public locations.
– She earns revenue by selling books and
videos that instruct people on kitchen design.
– She also offers custom-design consulting
services.
4-41
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 42

Heather Sweeney Designs:
The Seminar Customer List
4-42
Figure 4-16:  Example Seminar Customer List
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 43

Heather Sweeney Designs:
Initial E-R Diagram I
4-43
Figure 4-17:  Initial E-R Diagram for Heather Sweeney Designs
(a) First Version of the SEMINAR and CUSTOMER E-R Diagram
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 44

Heather Sweeney Designs:
Initial E-R Diagram II
4-44
Figure 4-17:  Initial E-R Diagram for Heather Sweeney Designs
(b) Second Version of the SEMINAR and CUSTOMER E-R Diagram
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 45

Heather Sweeney Designs:
Initial E-R Diagram III
4-45
(c) Third Version of the SEMINAR and CUSTOMER E-R Diagram
Figure 4-17:  Initial E-R Diagram for Heather Sweeney Designs
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 46

Heather Sweeney Designs:
The Customer Form Letter
4-46
Figure 4-18:
Heather Sweeney Designs
Customer Form Letter
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 47

Heather Sweeney Designs:
Data Model with CONTACT
4-47
Figure 4-19:  Heather Sweeney Designs Data Model with CONTACT
(a) First Version with CONTACT
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 48

Heather Sweeney Designs:
Data Model with CONTACT as Weak Entity
4-48
(b) Second Version with CONTACT as a Weak Entity
Figure 4-19:  Heather Sweeney Designs Data Model with CONTACT
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 49

Heather Sweeney Designs:
Data Model with Modified CUSTOMER
4-49
(c) Third Version with Modified CUSTOMER
Figure 4-19:  Heather Sweeney Designs Data Model with CONTACT
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 50

Heather Sweeney Designs:
Sales Invoice
4-50
Figure 4-20: Heather
Sweeney Designs
Sales Invoice
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 51

Heather Sweeney Designs:
Data Model with INVOICE
4-51
(a) Version with INVOICE
Figure 4-21:  The Final Data Model for Heather Sweeney Designs
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 52

Heather Sweeney Designs:
Data Model with LINE_ITEM
4-52
(b) Version with LINE_ITEM
Figure 4-21: The Final Data Model for Heather Sweeney Designs
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 53

Heather Sweeney Designs:
Final Data Model
4-53
(c) The Finished Data Model
Figure 4-21:  The Final Data Model for Heather Sweeney Designs
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 54

Heather Sweeney Designs:
Business Rules and Model Validation
• Business rules may constrain the
model and need to be recorded.
– Heather Sweeney Designs has a
business rule that no more than one
form letter or email per day is to be sent
to a customer.
• After the data model has been
completed, it needs to be validated.
– Prototyping is commonly used to
validate forms and reports.
4-54
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 55

All rights reserved. No part of this publication may be reproduced,
stored in a retrieval system, or transmitted, in any form or by any
means, electronic, mechanical, photocopying, recording, or otherwise,
without the prior written permission of the publisher. Printed in the
United States of America.
Copyright © 2015 Pearson Education, Inc.
Publishing as Prentice Hall
DAVID M. KROENKE and DAVID J. AUER
DATABASE CONCEPTS, 7th Edition

### Page 56

Data Modeling and the
Entity-Relationship Model
End of Presentation on Chapter Four
DAVID M. KROENKE and DAVID J. AUER
DATABASE CONCEPTS, 7th Edition

---

## Chapter5-Normalization.pdf

### Page 1

Normalization
Chapter Five
DAVID M. KROENKE and DAVID J. AUER
DATABASE CONCEPTS, 7th Edition

### Page 2

Chapter Objectives
• Learn how to transform E-R data models into
relational designs
• Practice applying the normalization process
• Understand the need for denormalization
• Learn how to represent weak entities with the
relational model
• Know how to represent 1:1, 1:N, and N:M binary
relationships
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 3

Chapter Objectives (Cont’d)
• Know how to represent 1:1, 1:N, and N:M
recursive relationships
• Learn SQL statements for creating joins over
binary and recursive relationships
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 4

Transforming a Data Model into a
Relational Design
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 5

Representing Entities with the
Relational Model
• Create a relation for each entity.
– A relation has a descriptive name and a set of attributes
that describe the entity.
• Specify a primary key.
• Specify column properties:
– Data type
– Null status
– Default values (if any)
– Data constraints (if any)
• The relation is then analyzed using the
normalization rules.
• As normalization issues arise, the initial relation
design may need to change.
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 6

Representing an Entity as a Table
ITEM (ItemNumber, Description, Cost, ListPrice, QuantityOnHand)
Figure 5-2:  The ITEM Entity and Table
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 7

The Entity Table
with Column Characteristics
ITEM (ItemNumber, Description, Cost, ListPrice, QuantityOnHand)
Figure 5-3:  The Final ITEM Table
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 8

Normalization Review:
Modification Problems
• Tables that are not normalized will
experience issues known as
modification problems.
– Insertion problems
• Difficulties inserting data into a relation
– Modification problems
• Difficulties modifying data into a relation
– Deletion problems
• Difficulties deleting data from a relation
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 9

Normalization Review:
Solving Modification Problems
• Most modification problems are
solved by breaking an existing table
into two or more tables through a
process known as normalization.
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 10

Normalization Review:
Definition Review
• Functional dependency
– The relationship (within the relation)
that describes how the value of one
attribute may be used to find the value
of another attribute.
• Determinant
– The attribute that can be used to find
the value of another attribute in the
relation
– The right-hand side of a functional
dependency
5-10
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 11

Normalization Review:
Definition Review II
• Candidate key
– The value of a candidate key can be
used to find the value of every other
attribute in the table.
– A simple candidate key consists of
only one attribute.
– A composite candidate key consists of
more than one attribute.
5-11
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 12

Normalization Review:
Normal Forms
• There are many defined normal
forms:
– First Normal Form (1NF)
– Second Normal Form (2NF)
– Third Normal Form (3NF)
– Boyce-Codd Normal Form (BCNF)
– Fourth Normal Form (4NF)
– Fifth Normal Form (5NF)
– Domain/Key Normal Form (DK/NF)
5-12
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 13

Normalization Review:
Normalization
• For our purposes, a relation is
considered normalized when:
Every determinant is a candidate key.
[Technically, this is Boyce-Codd Normal Form (BCNF)]
5-13
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 14

The CUSTOMER Table
CUSTOMER (CustomerNumber, CustomerName, StreetAddress,
City, State, ZIP, ContactName, Phone)
5-14
ZIP→(City, State)
ContactName→Phone
Figure 5-4:  The CUSTOMER Entity and Table
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 15

The CUSTOMER Entity:
The Normalized Set of Tables
CUSTOMER (CustomerNumber, CustomerName, StreetAddress,
ZIP, ContactName)
ZIP (ZIP, City, State)
CONTACT (ContactName, Phone)
5-15
Figure 5-5:  The Normalized CUSTOMER and Associated Tables
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 16

Denormalization
• Normalizing relations (or breaking
them apart into many component
relations) may significantly increase
the complexity of the data structure.
• The question is one of balance.
– Trading complexity for modification
problems
• There are situations where
denormalized relations are preferred.
5-16
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 17

The CUSTOMER Entity:
The Denormalized Set of Tables
CUSTOMER (CustomerNumber, CustomerName, StreetAddress,
City, State, ZIP, ContactName)
CONTACT (ContactName, Phone)
5-17
Figure 5-6: The Denormalized CUSTOMER and Associated CONTACT Tables
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 18

Representing Weak Entities
• If not ID-dependent, use the same
techniques as for strong entities.
• If ID-dependent, then must add
primary key of the parent entity.
5-18
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 19

Representing Weak Entities
Example
5-19
Figure 5-9:  Relational Representation of a Weak Entity
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 20

Representing Relationships
1:1 Relationships
• The maximum cardinality determines
how a relationship is represented.
• 1:1 relationship
– The key from one relation is placed in
the other as a foreign key.
– It does not matter which table receives
the foreign key.
5-20
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 21

Representing Relationships
1:1 Relationship Example
5-21
Figure 5-10:  1:1 Strong Entity Relationships
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 22

Representing Relationships
SQL for 1:1 Relationships
5-22
SELECT
FROM
LOCKER, EMPLOYEE
WHERE
LOCKER.LockerNumber =
EMPLOYEE.LockerNumber;
SELECT
FROM
LOCKER, EMPLOYEE
WHERE
LOCKER.EmployeeNumber =
EMPLOYEE.EmployeeNumber;
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 23

Representing Relationships
1:N Relationships
• Like a 1:1 relationship, a 1:N
relationship is saved by placing the
key from one table into another as a
foreign key.
• However, in a 1:N the foreign key
always goes into the many-side of
the relationship.
– The 1 side is called the parent.
– The N side is called the child.
5-23
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 24

Representing Relationships
1:N Relationship Example
5-24
Figure 5-12:  1:N Strong Entity Relationships
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 25

Representing Relationships
SQL for 1:N Relationships
5-25
SELECT
FROM
ITEM, QUOTATION
WHERE
ITEM.ItemNumber =
QUOTATION.ItemNumber;
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 26

Representing Relationships
N:M Relationships
• To create an N:M relationship, a new
table is created.  This table is called
an intersection table.
• An intersection table has a composite
key consisting of the keys from each
of the tables that it connects.
5-26
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 27

Representing Relationships
N:M Relationship – Data Model
5-27
Figure 5-13:  N:M Strong Entity Relationships
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 28

Representing Relationships
N:M Relationship – Database Design
5-28
Figure 5-15:  Representing an N:M Strong Entity Relationship
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 29

Representing Relationships
SQL for N:M Relationships
5-29
SELECT
FROM
STUDENT, CLASS, STUDENT_CLASS
WHERE
STUDENT.SID = STUDENT_CLASS.SID
STUDENT_CLASS.ClassNumber =
CLASS.ClassNumber;
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 30

Representing Relationships
Association Relationships
• When an intersection table has columns beyond
those in the primary key, the relationship is called
an association relationship.
5-30
Figure 5-18:  The Association Relationship
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 31

Representing Relationships
Supertype/Subtype Relationships
• The identifier of the supertype becomes the
primary key and the foreign key of each subtype.
5-31
Figure 5-20:  Representing Subtypes
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 32

Representing Relationships
Recursive Relationships
• A recursive relationship is a relationship
that a relation has with itself.
• Recursive relationships adhere to the
same rules as binary relationships.
– 1:1 and 1:M relationships are saved using
foreign keys.
– M:N relationships are saved by creating an
intersecting relation.
5-32
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 33

Representing Relationships
Recursive Relationships—Examples
5-33
Figure 5-21:  Example Recursive Relationships
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 34

Representing Relationships
1:1 Recursive Relationship Examples
5-34
SELECT  *
FROM    PERSON1 AS A, PERSON1 AS B
WHERE   A.Person = B.PersonSponsored;
SELECT  *
FROM    PERSON2 AS C, PERSON2 AS D
WHERE   C.Person = D.PersonSponsoredBy;
Figure 5-22:  Example 1:1 Recursive Relationships
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 35

Representing Relationships
1:N Recursive Relationship Example
5-35
SELECT  *
FROM    CUSTOMER AS A, CUSTOMER AS B
WHERE   A.CustomerNumber = B.ReferredBy;
Figure 5-23:  Example 1:N Recursive Relationship
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 36

Representing Relationships
N:M Recursive Relationship Example
5-36
Figure 5-24:  Example of an N:M Recursive Relationship
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 37

SQL for
N:M Recursive Relationships
5-37
SELECT *
FROM   DOCTOR AS A,
DOCTOR AS B,
TREATMENT-INTERSECTION
WHERE  A.Name = TREATMENT-INTERSECTION.Physician
AND TREATMENT-INTERSECTION.Patient = B.Name;
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 38

Heather Sweeney Designs:
Developing a Database Design
• Heather Sweeney Designs will be used as
on ongoing example throughout Chapters
4, 5, 6, 7, and 8.
– Heather Sweeney is an interior designer who
specializes in home kitchen design.
– She offers a variety of free seminars at home
shows, kitchen and appliance stores, and
other public locations.
– She earns revenue by selling books and
videos that instruct people on kitchen design.
– She also offers custom-design consulting
services.
5-38
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 39

Heather Sweeney Designs:
Final Data Model
5-39
Figure 5-25:  The Final Data Model for Heather Sweeney Designs
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 40

Specifying Column Properties
• Column properties must be specified for each
table.
• The finalized column properties for the HSD
tables are on the next set of slides-these are the
column characteristics after additional needed
foreign keys (shown in bold) have been added.
This includes any new intersection tables.
4-40
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 41

HSD Column Property Specifications
SEMINAR
5-41
SEMINAR
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
Figures 5-26 & 5-28: Heather Sweeney Designs Column Specifications

### Page 42

HSD Column Property Specifications
SEMINAR_CUSTOMER
5-42
SEMINAR_CUSTOMER
Figures 5-26 & 5-28: Heather Sweeney Designs Column Specifications
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 43

HSD Column Property Specifications
CUSTOMER
5-43
CUSTOMER
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
Figures 5-26 & 5-28: Heather Sweeney Designs Column Specifications

### Page 44

HSD Column Property Specifications
CONTACT
5-44
CONTACT
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
Figures 5-26 & 5-28: Heather Sweeney Designs Column Specifications

### Page 45

HSD Column Property Specifications
INVOICE
5-45
INVOICE
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
Figures 5-26 & 5-28: Heather Sweeney Designs Column Specifications

### Page 46

HSD Column Property Specifications
LINE_ITEM
5-46
LINE_ITEM
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
Figures 5-26 & 5-28: Heather Sweeney Designs Column Specifications

### Page 47

HSD Column Property Specifications
PRODUCT
5-47
PRODUCT
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
Figures 5-26 & 5-28: Heather Sweeney Designs Column Specifications

### Page 48

Heather Sweeney Designs:
Database Design
5-48
Figure 5-27:  Database Design for Heather Sweeney Designs
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 49

Heather Sweeney Designs:
Database Design Schema
5-49
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 50

Heather Sweeney Designs:
Referential Integrity Constraints
5-50
Figure 5-29: Referential Integrity Constraint Enforcement for Heather Sweeney Designs
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

---

## Chapter5-Normalizationnotes.pdf

### Page 1

SEG education group
Bachelor of Information Technology
Database Systems
BIT1223/BTL1223/BCL1223
Chapter 5 Normalization

### Page 2

SEG education group
In this chapter, you will learn:
• What normalization is and what role it plays in the database
design process
• About the normal forms 1NF, 2NF, 3NF
• How normal forms can be transformed from lower normal
forms to higher normal forms
• That normalization and ER modeling are used concurrently to
produce a good database design
• That some situations require denormalization to generate
information efficiently

### Page 3

SEG education group
• An anomaly is an error or inconsistency that may occur
when we try to update a table that contains redundant
data.
• Types of data anomalies:
• Update anomalies
• Occur when changes must be made to existing records
• Insertion anomalies
• Occur when entering new records
• Deletion anomalies
• Occur when deleting records
Data Anomalies
* recall from chapter 1

### Page 4

EmpDept (EmpID, DeptID, EmpName, DeptName, Location)
• Figure 1 shows a poorly-designed relation EmpDept which stores data of employees as
well as data of departments they work in.
• Its primary key (PK) is EmpID.
EmpID
DeptID
EmpName
DeptName
Location
Jane
Training
Blk 31
Training
Blk 31
Peter
Training
Blk 31
Mark
Human
Resources
Blk 1
Peter
Human
Resources
Blk 1
Finance
Blk 1
Figure 1
Update Anomalies

### Page 5

SEG education group
1. Insertion Anomaly
• There are two types of insertion anomaly which will be
illustrated with two different scenarios.
• 1) First Type of Insertion Anomaly
• To insert the details of new employee into EmpDept relation,
the details of the department which the employee is working
must also be included.
An insertion anomaly occurs when extra data
besides the required data for insertion must be
added to the database.

### Page 6

SEG education group
Relation: EmpDept
EmpID
DeptID
EmpName
DeptName
Location
Jane
Training
Blk 31
Training
Blk 31
Peter
Training
Blk 31
Mark
Human Resources
Blk 1
Peter
Human Resources
Blk 1
Finance
Blk 1
Department
details
must
consistent with existing records.
New Employee: Mary
Mary
Training
Blk 31
Figure 2 First type of Insertion Anomaly

### Page 7

SEG education group
• 2) 2nd Type of Insertion Anomaly
• To insert the details of a new department that has no
employees into EmpDept relation, it is necessary to provide a
value for EmpID, the primary key (PK).
• A null value for the primary key is not allowed as it
violates entity integrity.

### Page 8

SEG education group
Relation: EmpDept
EmpID
DeptI
EmpNam
DeptName
Locatio
Jane
Training
Blk 31
Training
Blk 31
Peter
Training
Blk 31
Mark
Human
Resources
Blk 1
Peter
Human
Resources
Blk 1
Finance
Blk 1
New Department details cannot be
inserted until an employee joins the
department.
New Department: Sales
Sales
Blk 8
Figure 3 First type of Insertion Anomaly

### Page 9

SEG education group
2. Deletion Anomaly
• If we delete a tuple that represents the last employee working at
a department from EmpDept relation, the details of the
department will also disappear from the database.
• As shown in Figure 4, employee with EmpNo 6 is the last
employee of Finance department.
A deletion anomaly occurs when deleting a row
causes other data to be deleted.

### Page 10

SEG education group
Relation: EmpDept
EmpID
DeptID
EmpName
DeptName
Location
Jane
Training
Blk 31
Training
Blk 31
Peter
Training
Blk 31
Mark
Human Resources
Blk 1
Peter
Human Resources
Blk 1
Finance
Blk 1
When the last employee of
Finance department is deleted,
details of Finance department are
also deleted.
Figure 4 Deletion Anomaly

### Page 11

SEG education group
3. Modification Anomaly
• If the value of any attributes of a department
changes, the tuples of all employees working in that
department must be updated.
• This situation of making multiple updates to ensure
data consistency in the database can give rise to the
problem of modification anomalies.
A modification anomaly occurs when it is necessary to
change multiple rows to modify a single fact.

### Page 12

SEG education group
If Training department changes its location from
‘Blk 31’ to ‘Blk 27’, then three tuples containing
information of that department must be updated.
Relation: EmpDept
EmpID
DeptID
EmpName
DeptName
Location
Jane
Training
Blk 31
Training
Blk 31
Peter
Training
Blk 31
Mark
Human Resources
Blk 1
Peter
Human Resources
Blk 1
Finance
Blk 1
Figure 5 Modification Anomaly

### Page 13

SEG education group
Database Tables and Normalization
• Normalization
• Process for evaluating and correcting table structures to minimize data
redundancies
• Reduces data anomalies
• Works through a series of stages called normal forms:
• First normal form (1NF)
• Second normal form (2NF)
• Third normal form (3NF)
• 2NF is better than 1NF; 3NF is better than 2NF
• For most business database design purposes, 3NF is as high as we need
to go in normalization process
• Highest level of normalization is not always most desirable

### Page 14

SEG education group
The Need for Normalization
• Example: Company that manages building projects
• Charges its clients by billing hours spent on each contract
• Hourly billing rate is dependent on employee’s position
• Periodically, report is generated that contains information displayed below:

### Page 15

SEG education group
The Need for Normalization (continued)
• Structure of data set in Table 5.1 does not handle data very
well
• The table structure appears to work; report generated with
ease
• Unfortunately, report may yield different results depending on
what data anomaly has occurred
• Each table represents a single subject
• No data item will be unnecessarily stored in more than one
table
• All attributes in a table are dependent on the primary key

### Page 16

SEG education group
The Normalization Process
• Each table represents a single subject
• No data item will be unnecessarily stored in more than one
table
• All attributes in a table are dependent on the primary key

### Page 17

SEG education group
Conversion to First Normal Form
• Repeating group
• Derives its name from the fact that a group of multiple entries of
same type can exist for any single key attribute occurrence
• Relational table must not contain repeating groups
• Normalizing table structure will reduce data redundancies
• Normalization is three-step procedure
• Step 1: Eliminate the Repeating Groups
• Present data in tabular format, where each cell has single value and
there are no repeating groups
• Eliminate repeating groups, eliminate nulls by making sure that each
repeating group attribute contains an appropriate data value

### Page 18

Conversion to First Normal Form
(continued)

### Page 19

SEG education group
Conversion to First Normal Form (continued)
• Step 2: Identify the Primary Key
• Primary key must uniquely identify attribute value
• New key must be composed
• Step 3: Identify All Dependencies
– Dependencies can be depicted with help of a diagram
– Dependency diagram:
• Depicts all dependencies found within given table
structure
• Helpful in getting bird’s-eye view of all relationships
among table’s attributes
• Makes it less likely that will overlook an important
dependency

### Page 20

Conversion to First Normal Form (continued)
• Some tables contain partial dependencies
• Dependencies based on only part of the primary key
• Sometimes used for performance reasons, but should be used
with caution
• Still subject to data redundancies

### Page 21

SEG education group
Conversion to Second Normal Form
• Relational database design can be improved by converting the
database into second normal form (2NF)
• Two steps
Step 1: Write Each Key Component on a Separate Line
– Write each key component on separate line, then write original
(composite) key on last line
– Each component will become key in new table
Step 2: Assign Corresponding Dependent Attributes
– Determine those attributes that are dependent on other attributes
– At this point, most anomalies have been eliminated

### Page 22

Conversion to Second Normal Form
(continued)
• Table is in second
normal form (2NF)
when:
• It is in 1NF and
• It includes no
partial
dependencies:
• No attribute is
dependent on
only portion of
primary key

### Page 23

SEG education group
Conversion to Third Normal Form
• Data anomalies created are easily eliminated by completing
three steps
• Step 1: Identify Each New Determinant
• For every transitive dependency, write its determinant as PK for new
table
• Determinant
• Any attribute whose value determines other values within a row
Step 2: Identify the Dependent Attributes
– Identify attributes dependent on each determinant identified in
Step 1 and identify dependency
– Name table to reflect its contents and function

### Page 24

SEG education group
Conversion to Third Normal Form
(continued)
• Step 3: Remove the Dependent Attributes from Transitive Dependencies
• Eliminate all dependent attributes in transitive relationship(s) from
each of the tables that have such a transitive relationship
• Draw new dependency diagram to show all tables defined in Steps 1–3
• Check new tables as well as tables modified in Step 3 to make sure that
each table has determinant and that no table contains inappropriate
dependencies

### Page 25

Conversion to Third Normal Form (cont)
• A table is in third normal form (3NF) when both of the following are true:
• It is in 2NF
• It contains no transitive dependencies

### Page 26

SEG education group
Improving the Design
• Table structures are cleaned up to eliminate troublesome initial partial and
transitive dependencies
• Normalization cannot, by itself, be relied on to make good designs
• It is valuable because its use helps eliminate data redundancies
• Issues to address in order to produce a good normalized set of tables:
• Evaluate PK Assignments
• Evaluate Naming Conventions
• Refine Attribute Atomicity
• Identify New Attributes
• Identify New Relationships
• Refine Primary Keys as Required for Data Granularity
• Maintain Historical Accuracy
• Evaluate Using Derived Attributes

### Page 27

Improving the Design (continued)

### Page 28

SEG education group
Normalization and Database Design
• Normalization should be part of design process
• Make sure that proposed entities meet required normal form before table
structures are created
• Many real-world databases have been improperly designed or burdened
with anomalies if improperly modified during course of time
• You may be asked to redesign and modify existing databases
• ER diagram
• Provides big picture, or macro view, of an organization’s data
requirements and operations
• Created through an iterative process
• Identifying relevant entities, their attributes and their relationship
• Use results to identify additional entities and attributes

### Page 29

SEG education group
Normalization and Database Design (continued)
• Normalization procedures
• Focus on characteristics of specific
entities
• Represents micro view of entities
within ER diagram
• Difficult to separate normalization
process from ER modeling process
• Two techniques should be used
concurrently

### Page 30

Normalization and Database Design (continued)

### Page 31

SEG education group
Denormalization
• Creation of normalized relations is important database design goal
• Processing requirements should also be a goal
• If tables decomposed to conform to normalization requirements:
• Number of database tables expands
• Joining the larger number of tables takes additional input/output (I/O)
operations and processing logic, thereby reducing system speed
• Conflicts between design efficiency, information requirements, and
processing speed are often resolved through compromises that may
include denormalization

### Page 32

SEG education group
Denormalization (continued)
• Unnormalized tables in production database tend to suffer from these
defects:
• Data updates are less efficient because programs that read and
update tables must deal with larger tables
• Indexing is more cumbersome
• Unnormalized tables yield no simple strategies for creating virtual
tables known as views
• Use denormalization cautiously
• Understand why—under some circumstances—unnormalized tables are
better choice

---

## Chapter6-SQL.pdf

### Page 1

Structured Query Language
Chapter Six
DAVID M. KROENKE and DAVID J. AUER
DATABASE CONCEPTS, 7th Edition

### Page 2

Chapter Objectives
• Learn basic SQL statements for creating
database structures
• Learn basic SQL statements for adding data to a
database
• Learn basic SQL SELECT statements and
options for processing a single table
• Learn basic SQL SELECT statements for
processing multiple tables with subqueries
• Learn basic SQL SELECT statements for
processing multiple tables with joins
• Learn basic SQL statements for modifying and
deleting data from a database
• Learn basic SQL statements for modifying and
deleting database tables and constraints
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 3

Structured Query Language
• Structured Query Language
– Acronym: SQL
– Pronounced as “S-Q-L” [“Ess-Que-El”]
– Originally developed by IBM as the
SEQUEL language in the 1970s
– SQL-92 is an ANSI national standard
adopted in 1992.
– SQL:2011 is current standard.
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 4

SQL Defined
• SQL is not a programming language, but rather a
data sublanguage.
• SQL is comprised of
– Data definition language (DDL)
• Used to define database structures
– Data manipulation language (DML)
• Data definition and updating
• Data retrieval (Queries)
– SQL/Persistent Stored Modules (SQL/PSM)
• Procedural programming capabilities [See Appendix E]
– Transaction control language (TCL)
• Control transaction behavior [See Chapter 6]
– Data control language (DLC)
• Grant and revoke database permissions [See Chapter 6]
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 5

SQL for Data Definition
• The SQL data definition statements
include:
– CREATE
• To create database objects
– ALTER
• To modify the structure and/or
characteristics of database objects
– DROP
• To delete database objects
– TRUNCATE
• To delete table data while keeping structure
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 6

Main Data Types
CIT4144/TCS4424 Advanced Database Systems
Keyword
Description
Sample Declaration
Sample Values
CHAR
Fixed length character string.
CHAR (4)
‘ABCD’,’   ‘,AbCd’
VARCHAR
Variable length character string
(you only specify max length).
VARCHAR (4)
‘ABCD’,’Ab’,’Add’
Fixed length bit string.
BIT (4)
‘1010’,’1111’,’0101’
BIT VARYING
Variable length bit string
BIT VARYING (4)
’01’,’1111’,’010’
NUMERIC
Decimal number.
NUMERIC (5)
NUMERIC (5,2)
12345
12345.01
DECIMAL
Higher precision decimal num.
DEC (4)
12345
INTEGER
Whole number (4 bytes).
INTEGER
12345678
SMALLINT
Whole number (2 bytes).
SMALLINT
1234
FLOAT
Floating point of at least the
stated precision.
FLOAT (4)
0.1234E+05
REAL
Floating point with
implementation-defined
precision.
REAL
0.1234E+05
DOUBLE
PRECISION
Floating point with higher
precision than REAL.
DOUBLE PRECISION
0.1234E+05
DATE
Calendar date consisting of
DAY, MONTH & YEAR
DATE
’02-MAY-05’
Modified from Howe (2001) Fig. 19.3, page 230.
Main Data Types

### Page 7

Example: CREATE TABLE with Primary Key
CIT4144/TCS4424 Advanced Database Systems
CREATE TABLE Depts
(Dept_No
SMALLINT
NOT NULL,
Dept_Name VARCHAR(15) NOT NULL,
CONSTRAINT d_pk PRIMARY KEY (Dept_No));
Table Name
Column
Name
Column
Data Type
Column
integrity rule
Table integrity rule
(enforcing entity
integrity)
Specify at table level on creation:
Name of constraint
so you can delete or
modify it later!
Example: CREATE TABLE with Primary Key

### Page 8

CIT4144/TCS4424 Advanced Database Systems
CREATE TABLE Depts
(Dept_No SMALLINT
CONSTRAINT d_pk PRIMARY KEY,
Dept_Name
VARCHAR(15) NOT NULL);
Column
integrity
rule
Specify at attribute level on creation:
Specify at table level post-hoc using ALTER TABLE:
CREATE TABLE Depts
(Dept_No
SMALLINT,
Dept_Name
VARCHAR(15) NOT NULL);
ALTER TABLE Depts
ADD CONSTRAINT d_pk PRIMARY KEY (Dept_No);
Post hoc
table
integrity
rule
Example: CREATE TABLE with Primary Key

### Page 9

SQL for Data Definition:
CREATE
• Creating database tables
– The SQL CREATE TABLE statement
CREATE TABLE EMPLOYEE(
EmpID       Integer
PRIMARY KEY,
EmpName     Char(25)
NOT NULL
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 10

SQL for Data Definition:
CREATE with CONSTRAINT I
• Creating database tables with
PRIMARY KEY constraints
– The SQL CREATE TABLE statement
– The SQL CONSTRAINT keyword
CREATE TABLE EMPLOYEE(
EmpID
Integer
NOT NULL,
EmpName
Char(25)
NOT NULL,
CONSTRAINT  Emp_PK
PRIMARY KEY(EmpID)
6-10
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 11

SQL for Data Definition:
CREATE with CONSTRAINT II
• Creating database tables with composite
primary keys using PRIMARY KEY
constraints
– The SQL CREATE TABLE statement
– The SQL CONSTRAINT keyword
CREATE TABLE EMP_SKILL(
EmpID
Integer      NOT NULL,
SkillID     Integer      NOT NULL,
SkillLevel  Integer
NULL,
CONSTRAINT  EmpSkill_PK  PRIMARY KEY
(EmpID, SkillID)
6-11
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 12

SQL for Data Definition:
CREATE with CONSTRAINT III
• Creating database tables using PRIMARY KEY
and FOREIGN KEY constraints
– The SQL CREATE TABLE statement
– The SQL CONSTRAINT keyword
CREATE TABLE EMP_SKILL(
EmpID       Integer      NOT NULL,
SkillID     Integer      NOT NULL,
SkillLevel  Integer
NULL,
CONSTRAINT  EmpSkill_PK  PRIMARY KEY
(EmpID, SkillID),
CONSTRAINT  Emp_FK
FOREIGN KEY(EmpID)
REFERENCES   EMPLOYEE(EmpID),
CONSTRAINT  Skill_FK
FOREIGN KEY(SkillID)
REFERENCES   SKILL(SkillID)
6-12
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 13

SQL for Data Definition:
CREATE with CONSTRAINT IV
Creating database tables using PRIMARY KEY and FOREIGN
KEY constraints
The SQL CREATE TABLE statement
The SQL CONSTRAINT keyword
ON UPDATE CASCADE and ON DELETE CASCADE
CREATE TABLE EMP_SKILL(
EmpID
Integer       NOT NULL,
SkillID
Integer       NOT NULL,
SkillLevel  Integer       NULL,
CONSTRAINT  EmpSkill_PK   PRIMARY KEY(EmpID, SkillID),
CONSTRAINT  Emp_FK
FOREIGN KEY(EmpID)
REFERENCES EMPLOYEE(EmpID)
ON DELETE CASCADE,
CONSTRAINT  Skill_FK
FOREIGN KEY(SkillID)
REFERENCES SKILL(SkillID)
ON UPDATE CASCADE
6-13
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 14

Process SQL CREATE TABLE Statements:
Microsoft SQL Server 2014
6-14
Table 3-8:
Processing the CREATE TABLE Statements Using SQL Server 2014
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 15

Process SQL CREATE TABLE Statements:
Oracle Database 11g Release 2
6-15
Figure 3-9: Processing the CREATE TABLE Statements
Using Oracle Database Express Edition 11g Release 2
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 16

Process SQL CREATE TABLE Statements:
MySQL 5.6
6-16
Figure 3-10:
Processing the CREATE TABLE Statements Using MySQL 5.6
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 17

Database Diagram in the
Microsoft SQL Server Management Studio
6-17
Figure 3-11:
Database Diagram in the Microsoft SQL Server Management Studio
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 18

Primary Key Constraint:
ALTER I
Adding primary key constraints to
an existing table
– The SQL ALTER statement
ALTER TABLE EMPLOYEE
ADD CONSTRAINT Emp_PK PRIMARY KEY(EmpID);
6-18
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 19

Composite Primary Key Constraints:
ALTER II
• Adding a composite primary key constraint
to an existing table
– The SQL ALTER statement
ALTER TABLE EMP_SKILL
ADD CONSTRAINT EmpSkill_PK
PRIMARY KEY(EmpID, SkillID);
6-19
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 20

Foreign Key Constraint:
ALTER III
• Adding foreign key constraints to an
existing table
– The SQL ALTER statement
ALTER TABLE EMPLOYEE ADD
CONSTRAINT  Emp_FK
FOREIGN KEY(DeptID)
REFERENCES  DEPARTMENT(DeptID);
6-20
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 21

Adding Data:
INSERT
• To add a row to an existing table,
use the INSERT statement.
• Non-numeric data must be enclosed
in straight ( ' ) single quotes.
INSERT INTO EMPLOYEE VALUES(91, 'Smither', 12);
INSERT INTO EMPLOYEE (EmpID, SalaryCode)
VALUES (62, 11);
6-21
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 22

END FOR
CREATING DATABASE &
TABLE STRUCTURE &
INSERT DATA
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
3-22

### Page 23

SQL for Data Retrieval:
Queries
• SELECT is the best known SQL
statement.
• SELECT will retrieve information
from the database that matches the
specified criteria using the
SELECT/FROM/WHERE framework.
SELECT EmpName
FROM
EMPLOYEE
WHERE
EmpID = 2010001;
6-23
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 24

SQL for Data Retrieval:
The Results of a Query Is a Relation
• A query pulls information from one or
more relations and creates
(temporarily) a new relation.
• This allows a query to:
– Create a new relation
– Feed information to another query (as a
“sub-query”)
6-24
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 25

SQL for Data Retrieval:
Displaying All Columns
• To show all of the column values for
the rows that match the specified
criteria, use an asterisk ( * ).
SELECT
FROM
EMPLOYEE;
6-25
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 26

SQL for Data Retrieval:
Showing Each Row Only Once
• The DISTINCT keyword may be
added to the SELECT statement to
inhibit duplicate rows from displaying.
SELECT  DISTINCT DeptID
FROM
EMPLOYEE;
6-26
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 27

SQL for Data Retrieval:
Specifying Search Criteria
• The WHERE clause stipulates the
matching criteria for the record that is
to be displayed.
SELECT
EmpName
FROM
EMPLOYEE
WHERE
DeptID = 15;
6-27
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 28

Processing SQL Query Statements:
Microsoft SQL Server 2014
6-28
Figure 3-13:
SQL Query Results in the Microsoft SQL Server Management Studio
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 29

Processing SQL Query Statements:
Oracle Database Express Edition 11g Release 2
6-29
Figure 3-14:  SQL Query Results in the Oracle SQL Developer
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 30

Processing SQL Query Statements:
MySQL 5.6
6-30
Figure 3-15:  SQL Query Results in the MySQL Workbench
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 31

SQL for Data Retrieval:
Match Criteria
• The WHERE clause match criteria
may include
– Equals “=”
– Not Equals “<>”
– Greater than “>”
– Less than “<”
– Greater than or Equal to “>=”
– Less than or Equal to “<=”
6-31
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 32

SQL for Data Retrieval:
Match Operators
• Multiple matching criteria may be
specified using
– AND
• Representing an intersection of the data
sets
– OR
• Representing a union of the data sets
6-32
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 33

SQL for Data Retrieval:
Operator Examples
SELECT     EmpName
FROM
EMPLOYEE
WHERE      DeptID < 7
DeptID > 12;
SELECT
EmpName
FROM
EMPLOYEE
WHERE
DeptID = 9
AND  SalaryCode <= 23;
6-33
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 34

SQL for Data Retrieval:
A List of Values
• The WHERE clause may include the IN
keyword to specify that a particular column
value must be included in a list of values.
SELECT    EmpName
FROM      EMPLOYEE
WHERE     DeptID IN (4, 8, 9);
6-34
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 35

SQL for Data Retrieval:
The Logical NOT Operator
• Any criteria statement may be
preceded by a NOT operator, which
is to say that all information will be
shown except that information
matching the specified criteria
SELECT   EmpName
FROM     EMPLOYEE
WHERE    DeptID NOT IN (4, 8, 9);
6-35
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 36

SQL for Data Retrieval:
Finding Data in a Range of Values
• SQL provides a BETWEEN keyword that
allows a user to specify a minimum and
maximum value on one line.
SELECT  EmpName
FROM    EMPLOYEE
WHERE   SalaryCode BETWEEN 10 AND 45;
6-36
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 37

SQL for Data Retrieval:
Allowing for Wildcard Searches
• The SQL LIKE keyword allows
searches on partial data values.
• LIKE can be paired with wildcards to
find rows matching a string value.
– Multiple character wildcard character is
a percent sign (%).
– Single character wildcard character is
an underscore (_).
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
6-37

### Page 38

SQL for Data Retrieval:
Wildcard Search Examples
SELECT
EmpID
FROM
EMPLOYEE
WHERE
EmpName LIKE 'Kr%';
SELECT
EmpID
FROM
EMPLOYEE
WHERE
Phone LIKE '616-___-____';
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
6-38

### Page 39

SQL for Data Retrieval:
Sorting the Results
• Query results may be sorted using
the ORDER BY clause.
SELECT
FROM
EMPLOYEE
ORDER BY
EmpName;
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
6-39

### Page 40

SQL for Data Retrieval:
Built-in SQL Functions
• SQL provides several built-in
functions:
– COUNT
• Counts the number of rows that match the
specified criteria
– MIN
• Finds the minimum value for a specific
column for those rows matching the criteria
– MAX
• Finds the maximum value for a specific
column for those rows matching the criteria
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
6-40

### Page 41

SQL for Data Retrieval:
Built-in SQL Functions (Cont’d)
• SUM
– Calculates the sum for a specific
column for those rows matching the
criteria
• AVG
– Calculates the numerical average of a
specific column for those rows
matching the criteria
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
6-41

### Page 42

SQL for Data Retrieval:
Built-in Function Examples
SELECT COUNT(DeptID)
FROM
EMPLOYEE;
SELECT MIN(Hours) AS MinimumHours,
MAX(Hours) AS MaximumHours,
AVG(Hours) AS AverageHours
FROM
PROJECT
WHERE ProjID > 7;
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
6-42

### Page 43

SQL for Data Retrieval:
Providing Subtotals: GROUP BY
• Subtotals may be calculated by using
the GROUP BY clause.
• The HAVING clause may be used to
restrict which data is displayed.
SELECT
DeptID,
COUNT(*) AS NumOfEmployees
FROM
EMPLOYEE
GROUP BY
DeptID
HAVING
COUNT(*) > 3;
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
6-43

### Page 44

SQL for Data Retrieval:
Retrieving Information from Multiple Tables
• Subqueries
– As stated earlier, the result of a query is a
relation.  As a result, a query may feed
another query.  This is called a subquery.
• Joins
– Another way of combining data is by using a
join .
• Join [also called an Inner Join]
• Left Outer Join
• Right Outer Join
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
6-44

### Page 45

SQL for Data Retrieval:
Subquery Example
SELECT EmpName
FROM
EMPLOYEE
WHERE DeptID in
(SELECT  DeptID
FROM
DEPARTMENT
WHERE
DeptName LIKE 'Account%');
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
6-45

### Page 46

SQL for Data Retrieval:
Join Example
SELECT  EmpName
FROM    EMPLOYEE AS E, DEPARTMENT AS D
WHERE   E.DeptID = D.DeptID
AND  D.DeptName LIKE 'Account%';
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
6-46

### Page 47

SQL for Data Retrieval:
JOIN…ON Example
• The JOIN…ON syntax can be used
in joins.
• It has the advantage of moving the
JOIN syntax into the FROM clause.
SELECT  EmpName
FROM    EMPLOYEE AS E JOIN DEPARTMENT AS D
ON  E.DeptID = D.DeptID
WHERE   D.DeptName LIKE 'Account%';
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
6-47

### Page 48

SQL for Data Retrieval:
OUTER JOIN I
The OUTER JOIN syntax can be used to obtain data that
exists in one table without matching data in the other
table.
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
Figure 3-17:  Types of Joins
6-48

### Page 49

SQL for Data Retrieval:
OUTER JOIN II
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
Figure 3-17:  Types of Joins
6-49

### Page 50

SQL for Data Retrieval:
OUTER JOIN III
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
Figure 3-17:  Types of Joins
6-50

### Page 51

SQL for Data Retrieval:
OUTER JOIN IV
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
Figure 3-17:  Types of Joins
6-51

### Page 52

SQL for Data Retrieval:
LEFT OUTER JOIN Example
• The OUTER JOIN syntax can be
used to obtain data that exists in
one table without matching data in
the other table.
SELECT  EmpName
FROM    EMPLOYEE AS E
LEFT JOIN DEPARTMENT AS D
ON  E.DeptID = D.DeptID
WHERE   D.DeptName LIKE 'Account%';
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
6-52

### Page 53

SQL for Data Retrieval:
RIGHT OUTER JOIN Example
• The unmatched data displayed can
be from either table, depending on
whether RIGHT JOIN or LEFT JOIN
is used.
SELECT  EmpName
FROM    EMPLOYEE AS E
RIGHT JOIN DEPARTMENT AS D
ON  E.DeptID = D.DeptID
WHERE   D.DeptName LIKE 'Account%';
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
6-53

### Page 54

Modifying Data using SQL
• Insert
– Will add a new row in a table (already
discussed above)
• Update
– Will update the data in a table that
matches the specified criteria
• Delete
– Will delete the data in a table that
matches the specified criteria
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
6-54

### Page 55

Modifying Data using SQL:
Changing Data Values: UPDATE
• To change the data values in an existing
row (or set of rows) use the Update
statement.
UPDATE    EMPLOYEE
Phone '791-555-1234'
WHERE     EmpID = 29;
UPDATE    EMPLOYEE
SET       DeptID = 44
WHERE     EmpName LIKE 'Kr%';
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
6-55

### Page 56

Modifying Data using SQL:
MERGE
• SQL:2003 introduced the MERGE
statement.
– Combines INSERT and UPDATE into one
statement
– Uses the equivalent of IF-THEN-ELSE logic to
decide whether to use INSERT or UPDATE
– An advanced feature—learn to use INSERT
and UPDATE separately first, then consult
DBMS documentation
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
6-56

### Page 57

Modifying Data using SQL:
Deleting Data: DELETE
• To delete a row or set of rows from a
table use the DELETE statement.
DELETE FROM EMPLOYEE
WHERE  EmpID = 29;
DELETE FROM EMPLOYEE
WHERE  EmpName LIKE 'Kr%';
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
6-57

### Page 58

Modifying Data using SQL:
Deleting Database Objects: DROP
• To remove unwanted database
objects from the database, use the
SQL DROP statement.
• Warning… The DROP statement will
permanently remove the object and
all data.
DROP TABLE EMPLOYEE;
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
6-58

### Page 59

Modifying Data using SQL:
Removing a Constraint: ALTER & DROP
• To change the constraints on existing
tables, you may need to remove the
existing constraints before adding
new constraints.
ALTER TABLE EMPLOYEE
DROP CONSTRAINT EmpFK;
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
6-59

### Page 60

Modifying Data Using SQL:
The CHECK Constraint
• The CHECK constraint can be used
to create sets of values to restrict the
values that can be used in a column.
ALTER TABLE PROJECT
ADD CONSTRAINT PROJECT_Check_Dates
CHECK (StartDate < EndDate);
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
6-60

### Page 61

SQL Views
• A SQL View is a virtual table created
by a DBMS-stored SELECT
statement that can combine access
to data in multiple tables and even in
other views.
• SQL views are discussed online in
Appendix E.
KROENKE and AUER - DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall
6-61

### Page 62

END OF CHAPTER 6

---

## Chapter7-DbIssues.pdf

### Page 1

Database Issues
Chapter Seven
DAVID M. KROENKE and DAVID J. AUER
DATABASE CONCEPTS, 7th Edition

### Page 2

Chapter Objectives
• Understand the need for and importance of
database administration
• Learn different ways of processing a database
• Understand the need for concurrency control,
security, and backup and recovery
• Learn about  typical problems that can occur when
multiple users process a database concurrently
• Understand the use of locking and the problem of
deadlock
• Learn the difference between optimistic and
pessimistic locking
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall

### Page 3

Chapter Objectives (Cont’d)
• Know the meaning of ACID transaction
• Learn the four 1992 ANSI standard isolation
levels
• Understand the need for security and specific
tasks for improving database security
• Know the difference between recovery via
reprocessing and recovery via
rollback/rollforward
• Understand the nature of the tasks required for
recovery using rollback/rollforward
• Know basic administrative and management DBA
functions
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall

### Page 4

Heather Sweeney Designs:
Database Design
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Education, Inc. Publishing as Prentice Hall

### Page 5

Heather Sweeney Designs:
HSD Database in Microsoft SQL Server 2014
Figure 6-1:  The HSD Database in Microsoft SQL Server 2014
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall

### Page 6

Heather Sweeney Designs:
HSD Database Diagram in SQL Server 2012
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall

### Page 7

The Database Processing
Environment
Figure 6-2:  The Database  Processing Environment
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall

### Page 8

Control, Security and Reliability
• Three necessary database
administration functions are:
– Concurrency control
– Security
– Backup and Recovery
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall

### Page 9

Concurrency Control
• Concurrency control ensures that one
user’s actions do not adversely impact
another user’s actions.
• At the core of concurrency is accessibility.
• In one extreme, data becomes
inaccessible once a user touches the
data.
– This ensures that data that is being
considered for update is not shown.
• In the other extreme, data is always
readable.
– The data is even readable when it is locked for
update.
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall

### Page 10

Concurrency Control
(continued)
• Interdependency
– Changes required by one user may impact
others.
• Concurrency
– People or applications may try to update the
same information at the same time.
• Record retention
– When information should be discarded
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-10

### Page 11

Need for Atomic
Transactions
• A database operation typically involves
several transactions.
• These transactions are atomic and are
sometimes called logical units of work
(LUW).
• Before an operation is committed to the
database, all LUWs must be successfully
completed.
– If one or more LUW is unsuccessful, a rollback
is performed and no changes are saved to the
database.
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-11

### Page 12

Transaction Example I
Figure 6-3:  Comparison of the Results of Applying Serial Actions
Versus a Multiple-Step Transaction
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-12

### Page 13

Transaction Example II
Figure 6-3: Comparison of the Results of Applying Serial Actions
Versus a Multiple-Step Transaction (Cont’d)
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-13

### Page 14

Concurrent Processing Example
Figure 6-4:  Example of Concurrent  Processing of Two Users’ Tasks
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-14

### Page 15

Lost Update Problem
• If two or more users are attempting to
update the same piece of data at the
same time, it is possible that one
update may overwrite the other
update
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-15

### Page 16

Lost Update Problem Example
Figure 6-5:  Example of the Lost Update Problem
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-16

### Page 17

Concurrency Issues
• Dirty reads
– The transaction reads a changed record that
has not been committed to the database.
• Inconsistent reads
– The transaction re-reads a data set and finds
that the data has changed.
• Phantom reads
– The transaction re-reads a data set and finds
that a new record has been added.
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-17

### Page 18

Resource Locking
• To avoid concurrency issues,
resource locking will disallow
transactions from reading, modifying
and/or writing to a data set that has
been locked.
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-18

### Page 19

Implicit versus Explicit
Resource Locking
• Implicit locks are issued
automatically by the DBMS based on
an activity.
• Explicit locks are issued by users
requesting exclusive rights to the
data.
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-19

### Page 20

Concurrent Processing with
Explicit Locking Example
Figure 6-6:  Example of Concurrent  Processing with Explicit Locks
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-20

### Page 21

Serializable Transactions
• When two or more transactions are
processed concurrently, the results in the
database should be logically consistent
with the results that would have been
achieved had the transactions been
processed in an arbitrary serial fashion.
• A scheme for processing concurrent
transactions in this way is said to be
serializable.
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-21

### Page 22

Two-Phased Locking
• One way to achieve serializable
transactions is by using two-phased
locking.
• Two-phased locking lets locks be
obtained and released as they are needed.
– A growing phase, when the transaction
continues to request additional locks
– A shrinking phase, when the transaction
begins to release the locks
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-22

### Page 23

Deadlock
• As a transaction begins to lock
resources, it may have to wait for a
particular resource to be released by
another transaction.
• On occasions, two transactions may
indefinitely wait on each another to
release resources—This condition is
known as a deadlock or the deadly
embrace.
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-23

### Page 24

Deadlock Example
Figure 6-7:  Example of Deadlock
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-24

### Page 25

Optimistic Locking versus
Pessimistic Locking
• Optimistic Locking
– Read data
– Process
transaction
– Issue update
– Look for conflict
– IF no conflict occurred
THEN commit
transaction
– ELSE rollback and
repeat transaction
• Pessimistic Locking
– Lock required
resources
– Read data
– Process
transaction
– Issue commit
– Release locks
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-25

### Page 26

Optimistic Locking Example
Figure 6-8:   Example of Optimistic Locking
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-26

### Page 27

Pessimistic Locking Example
Figure 6-9:  Example of Pessimistic Locking
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-27

### Page 28

SQL Transaction Control Language (TLC)
• The SQL BEGIN TRANSACTION statement
• The SQL COMMIT TRANSACTION statement
• The SQL ROLLBACK TRANSACTION statement
NOTE: Exact SQL syntax varies between DBMS products.
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-28

### Page 29

Marking Transaction Boundaries Example
Figure 6-10:  Example of Marking Transaction Boundaries
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-29

### Page 30

Consistent Transactions
• Consistent transactions are often
referred to by the acronym ACID.
– Atomic
– Consistent
– Isolated
– Durable
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-30

### Page 31

ACID: Atomic
• An atomic transaction is one in
which all of the database actions
occur or none of them do.
• A transaction consists of a series of
steps.  Each step must be successful
for the transaction to be saved.
• This ensures that the transaction
completes everything it intended to
do before saving the changes.
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-31

### Page 32

ACID: Consistent
• No other transactions are permitted
on the records until the current
transaction finishes.
• This ensures that the transaction
integrity has statement level
consistency among all records.
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-32

### Page 33

ACID: Isolation
• Within multiuser environments, different
transactions may be operating on the
same data.
• As such, the sequencing of uncommitted
updates, rollbacks, and commits
continuously change the data content.
• The 1992 ANSI SQL standard defines four
isolation levels that specify which of the
concurrency control problems are allowed
to occur.
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-33

### Page 34

ACID: Durable
• A durable transaction is one in which
all committed changes are
permanent.
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-34

### Page 35

Summary of Data Read Problems
Figure 6-11:  Summary of Data Read Problems
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-35

### Page 36

1992 ANSI SQL Isolation levels
Figure 6-12:  Summary of Isolation Levels
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-36

### Page 37

Cursors
• A cursor is a pointer into a set of
rows that are the result set from an
SQL SELECT statement.
• Cursors are usually defined using
SELECT statements.
DECLARE CURSOR TransCursor AS
SELECT *
FROM   SALE_TRANSACTION
WHERE  PurchasePrice > '10000';
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-37

### Page 38

Cursor Types
• Forward only or scrollable
• In SQL Server, for forward only or
scrollable cursors, there are three
types:
– Static cursor
– Keyset cursor
– Dynamic cursor
• Other DBMS products may define a
different set of cursors.
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-38

### Page 39

Summary of Cursor Types
Figure 6-13:  Summary of Cursor Types
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-39

### Page 40

A Note on Cursor Types
• Other DBMS products may define a
different set of cursors.
• In this case, the forward only cursor
is considered a separate cursor type,
and only a scrollable cursor may be
static, keyset, or dynamic.
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-40

### Page 41

Database Security
• Database Security strives to ensure
that
– Only authenticated users
– Perform authorized activities
Figure 6-14:  Database Security  Authentication and  Authorization
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-41

### Page 42

Processing Rights and
Responsibilities
• Processing rights define who is
permitted to do what and when.
• The individuals performing these
activities have full responsibility for
the implications of their actions.
• Individuals are identified by a
username and a password.
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-42

### Page 43

User Accounts in SQL Server 2014:
Server Login Account
Figure 6-15:  Creating the Database Server Login
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-43

### Page 44

A Model of DBMS Security
Figure 6-16:  A Model of DBMS Security
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-44

### Page 45

Processing Rights at
Heather Sweeney Designs
Figure 6-17:  Processing Rights at Heather Sweeney Designs
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-45

### Page 46

User Accounts in SQL Server 2014:
Database User
Figure 6-18:  Creating the Database User Name
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-46

### Page 47

Granting Permissions
• Database users are known as an
individual and as a member of one or
more roles.
• Granting access and processing
rights/privileges may be granted to an
individual and/or a role.
• Users possess the compilation of rights
granted to the individual and all the roles
for which they are members.
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-47

### Page 48

SQL Server 2014
Fixed Database Roles
Figure 6-19:  SQL Server Fixed Database Roles
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-48

### Page 49

Assigning HSD-Database-User to the
SQL Server 2014 db_datareader Role
Figure 6-20:  Assigning HSD-Database-User to the db_datareader Role
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-49

### Page 50

Database Security Guidelines
• Run the DBMS behind a firewall.
• Apply the latest operating system and
DBMS service packs and patches.
• Limit DBMS functionality to needed
features.
• Protect the computer that runs the DBMS.
• Manage accounts and passwords.
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-50

### Page 51

Database Backup and
Recovery
• Common causes of database failures
– Hardware failures
– Programming bugs
– Human errors/mistakes
– Malicious actions
• As these issues are impossible to
completely avoid, recovery procedures
are essential.
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-51

### Page 52

Recovery via Reprocessing
• In reprocessing, all activities since the
backup was performed are redone.
• This is a brunt-force technique.
• This procedure is costly in the effort
involved in re-entering the data.
• This procedure is risky in that human error
is likely and in that paper record-keeping
may not be accurate.
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-52

### Page 53

Recovery via
Rollback and Rollforward
• Most database management systems provide a
mechanism to record activities into a log file.
– To undo a transaction the log must contain a copy of
every database record before it was changed.
• Such records are called before-images.
• A transaction is undone by applying before-images of all
its changes to the database.
– To redo a transaction the log must contain a copy of
every database record (or page) after it was changed.
• These records are called after-images.
• A transaction is redone by applying after-images of all its
changes to the database.
• The log file is then used for recovery via rollback
or rollforward.
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-53

### Page 54

Rollback
• Rollback
– Log files save activities in sequence
order.
– It is possible to undo activities in
reverse order that they were originally
executed.
– This is performed to correct/undo
erroneous or malicious transaction(s)
after a database is recovered from a full
backup.
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-54

### Page 55

Rollback Example
Figure 6-22:  Undo and Redo Transactions
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-55

### Page 56

Rollforward
• Rollforward
– Activities recorded in the log files may
be replayed.
– In doing so, all activities are re-applied
to the database.
– This procedure is used to
resynchronize restored database data
by adding transactions to the last full
backup.
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-56

### Page 57

Rollforward Example
Figure 6-22:  Undo and Redo Transactions (Cont’d)
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-57

### Page 58

Example Transaction Log
Figure 6-23:  Transaction Log Example
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-58

### Page 59

Recovery Example I
Figure 6-24:  Recovery Example
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-59

### Page 60

Recovery Example I
Figure 6-24:  Recovery Example  (Cont’d)
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-60

### Page 61

Backing Up the HSD Database
Microsoft SQL Server 2014
Figure 6-25:  Backing Up the HSD Database
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-61

### Page 62

Additional DBA Responsibilities
The DBA needs to ensure that a system exists to gather
and record user reported errors and other problems.
– A means needs to be devised to prioritize those errors and
problems and to ensure that they are corrected accordingly .
The DBA needs to create and manage a process for
controlling the database configuration.
– Procedures for recording change requests
– Conducting user and developer reviews of such requests
– Creating projects and tasks
The DBA is responsible for ensuring that appropriate
documentation is maintained.
– Database structure
– Concurrency control
– Security
– Backup and recovery
– Applications used
KROENKE and AUER -  DATABASE CONCEPTS (7th Edition)
Copyright © 2015 Pearson Educations, Inc. Publishing as Prentice Hall
7-62

### Page 63

END OF CHAPTER 7

---

## Lecture1DATABASECONCEPTS.pptx

### Slide 2

Database Systems, 9th Edition

‹#›

Database Systems: Design, Implementation, and ManagementNinth Edition

Chapter 1

Database Concept

### Slide 3

OBJECTIVES

In this chapter, you will learn:

The difference between data and information

What a database is, the various types of databases, and why they are valuable assets for decision making

The importance of database design

How modern databases evolved from file systems

About flaws in file system data management

The main components of the database system

The main functions of a database management system (DBMS)

Database Systems, 9th Edition

‹#›

### Slide 4

WHY DATABASES?

Databases solve many of the problems encountered in data management

Used in almost all modern settings involving data management:

Business

Research

Administration

Important to understand how databases work and interact with other applications

Database Systems, 9th Edition

‹#›

### Slide 5

DATA VS. INFORMATION

Data are raw facts

Information is the result of processing raw data to reveal meaning

Information requires context to reveal meaning

Raw data must be formatted for storage, processing, and presentation

Data are the foundation of information, which is the bedrock of knowledge

Database Systems, 9th Edition

‹#›

### Slide 6

DATA VS. INFORMATION (CONT’D.)

Data: building blocks of information

Information produced by processing data

Information used to reveal meaning in data

Accurate, relevant, timely information is the key to good decision making

Good decision making is the key to organizational survival

Database Systems, 9th Edition

‹#›

### Slide 7

INTRODUCING THE DATABASE

Database: shared, integrated computer structure that stores a collection of:

End-user data: raw facts of interest to end user

Metadata: data about data

Provides description of data characteristics and relationships in data

Complements and expands value of data

Database management system (DBMS): collection of programs  that manages structure and controls access to data

Database Systems, 9th Edition

‹#›

### Slide 8

ROLE AND ADVANTAGES OF THE DBMS

DBMS is the intermediary between the user and the database

Database structure stored as file collection

Can only access files through the DBMS

DBMS enables data to be shared

DBMS integrates many users’ views of the data

Database Systems, 9th Edition

‹#›

### Slide 9

Database Systems, 9th Edition

‹#›

### Slide 10

ROLE AND ADVANTAGES OF THE DBMS

Advantages of a DBMS:

Improved data sharing

Improved data security

Better data integration

Minimized data inconsistency

Improved data access

Improved decision making

Increased end-user productivity

Database Systems, 9th Edition

‹#›

### Slide 11

TYPES OF DATABASES

Databases can be classified according to:

Number of users

Database location(s)

Expected type and extent of use

Single-user database supports only one user at a time

Desktop database: single-user; runs on PC

Multiuser database supports multiple users at the same time

Workgroup and enterprise databases

Database Systems, 9th Edition

‹#›

### Slide 12

TYPES OF DATABASES (CONT’D.)

Centralized database: data located at a single site

Distributed database: data distributed across several different sites

Operational database: supports a company’s day-to-day operations

Transactional or production database

Designed to allow users to easily define, modify, retrieve and manage data in real-time

Data warehouse: stores data used for tactical or strategic decisions

Database Systems, 9th Edition

‹#›

### Slide 13

Database Systems, 9th Edition

‹#›

### Slide 14

WHY DATABASE DESIGN IS IMPORTANT

Database design focuses on design of database structure used for end-user data

Designer must identify database’s expected use

Well-designed database:

Facilitates data management

Generates accurate and valuable information

Poorly designed database:

Causes difficult-to-trace errors

Database Systems, 9th Edition

‹#›

### Slide 15

EVOLUTION OF FILE SYSTEM DATA PROCESSING

Reasons for studying file systems:

Complexity of database design is easier to understand

Understanding file system problems helps to avoid problems with DBMS systems

Knowledge of file system is useful for converting file system to database system

File systems typically composed of collection of file folders, each tagged and kept in cabinet

Database Systems, 9th Edition

‹#›

### Slide 16

EVOLUTION OF FILE SYSTEM DATA PROCESSING (CONT'D.)

Contents of each file folder are logically related

Manual systems

Served as a data repository for small data collections

Cumbersome for large collections

Computerized file systems

Data processing (DP) specialist converted computer file structure from manual system

Database Systems, 9th Edition

‹#›

### Slide 17

EVOLUTION OF FILE SYSTEM DATA PROCESSING (CONT'D.)

Initially, computer file systems resembled manual systems

As number of files increased, file systems evolved

Each file used its own application program to store, retrieve, and modify data

Each file was owned by individual or department that commissioned its creation

Database Systems, 9th Edition

‹#›

### Slide 18

Database Systems, 9th Edition

‹#›

### Slide 19

Database Systems, 9th Edition

‹#›

### Slide 20

Database Systems, 9th Edition

‹#›

### Slide 21

PROBLEMS WITH FILE SYSTEM DATA PROCESSING

File systems were an improvement over manual system

File systems used for more than two decades

Understanding the shortcomings of file systems aids in development of modern databases

Many problems not unique to file systems

Even simple file system retrieval task required extensive programming

Ad hoc queries impossible

Changing existing structure difficult

Database Systems, 9th Edition

‹#›

### Slide 22

PROBLEMS WITH FILE SYSTEM DATA PROCESSING (CONT'D.)

Security features difficult to program

Often omitted in file system environments

Summary of file system limitations:

Requires extensive programming

Cannot perform ad hoc queries

System administration is complex and difficult

Difficult to make changes to existing structures

Security features are likely to be inadequate

Database Systems, 9th Edition

‹#›

### Slide 23

STRUCTURAL AND DATA DEPENDENCE

Structural dependence: access to a file is dependent on its own structure (changes will cause changing all structure)

All file system programs must be modified to conform to a new file structure

Structural independence: change file structure without affecting data access

Data dependence: data access changes when data storage characteristics change (affecting data access)

Data independence: data storage characteristics do not affect data access

Database Systems, 9th Edition

‹#›

### Slide 24

DATA REDUNDANCY

File system structure makes it difficult to combine data from multiple sources

Vulnerable to security breaches

Organizational structure promotes storage of same data in different locations

Islands of information

Data stored in different locations is unlikely to be updated consistently

Data redundancy: same data stored unnecessarily in different places

Database Systems, 9th Edition

‹#›

### Slide 25

DATA REDUNDANCY (CONT'D.)

Data inconsistency: different and conflicting versions of same data occur at different places

Data anomalies: abnormalities when all changes in redundant data are not made correctly (changes made will cause unexpected result)

Three types of anomalies:

Update anomalies

Insertion anomalies

Deletion anomalies

Database Systems, 9th Edition

‹#›

### Slide 28

LACK OF DESIGN AND DATA-MODELING SKILLS

Most users lack the skill to properly design databases, despite multiple personal productivity tools being available

Data-modeling skills are vital in the data design process

Good data modeling facilitates communication between the designer, user, and the developer

Database Systems, 9th Edition

‹#›

### Slide 29

DATABASE SYSTEMS

Database system consists of logically related data stored in a single logical data repository

May be physically distributed among multiple storage facilities

DBMS eliminates most of file system’s problems

Current generation stores data structures, relationships between structures, and access paths

Also defines, stores, and manages all access paths and components

Database Systems, 9th Edition

‹#›

### Slide 30

Database Systems, 9th Edition

‹#›

### Slide 31

Database Systems, 9th Edition

‹#›

A DBMS is a software that allows users to interact with database.

### Slide 32

THE DATABASE SYSTEM ENVIRONMENT

Database system: defines and regulates the collection, storage, management, use of data

Five major parts of a database system:

Hardware

Software

People

Procedures

Data

Database Systems, 9th Edition

‹#›

### Slide 33

Database Systems, 9th Edition

‹#›

### Slide 34

THE DATABASE SYSTEM ENVIRONMENT

Hardware: all the system’s physical devices

Software: three types of software required:

Operating system software

DBMS software

Application programs and utility software

People: all users of the database system

System and database administrators

Database designers

Systems analysts and programmers

End users

Procedures: instructions and rules that govern the design and use of the database system

Data: the collection of facts stored in the database

Database Systems, 9th Edition

‹#›

Hardware: all the system’s physical devices

Software: three types of software required:

Operating system software

DBMS software

Application programs and utility software

People: all users of the database system

System and database administrators

Database designers

Systems analysts and programmers

End users

Procedures: instructions and rules that govern the design and use of the database system

Data: the collection of facts stored in the database

### Slide 35

DBMS FUNCTIONS

Most functions are transparent to end users

Can only be achieved through the DBMS

Data dictionary management

DBMS stores definitions of data elements and relationships (metadata) in a data dictionary

DBMS looks up required data component structures and relationships

Changes automatically recorded in the dictionary

DBMS provides data abstraction and removes structural and data dependency

Database Systems, 9th Edition

‹#›

### Slide 36

Database Systems, 9th Edition

‹#›

### Slide 37

DBMS FUNCTIONS (CONT'D.)

Data storage management

DBMS creates and manages complex structures required for data storage

Also stores related data entry forms, screen definitions, report definitions, etc.

Performance tuning: activities that make the database perform more efficiently

DBMS stores the database in multiple physical data files

Database Systems, 9th Edition

‹#›

### Slide 38

DBMS FUNCTIONS (CONT'D.)

Data transformation and presentation

DBMS transforms data entered to conform to required data structures

DBMS transforms physically retrieved data to conform to user’s logical expectations

Security management

DBMS creates a security system that enforces user security and data privacy

Security rules determine which users can access the database, which items can be accessed, etc.

Multiuser access control

DBMS uses sophisticated algorithms to ensure concurrent access does not affect integrity

Backup and recovery management

DBMS provides backup and data recovery to ensure data safety and integrity

Recovery management deals with recovery of database after a failure

Database Systems, 9th Edition

‹#›

### Slide 39

DBMS FUNCTIONS (CONT'D.)

Data integrity management

DBMS promotes and enforces integrity rules

Minimizes redundancy

Maximizes consistency

Data relationships stored in data dictionary used to enforce data integrity

Integrity is especially important in transaction-oriented database systems

Database access languages and application programming interfaces

DBMS provides access through a query language

Query language is a nonprocedural language

Structured Query Language (SQL) is the de facto query language

Standard supported by majority of DBMS vendors

Database Systems, 9th Edition

‹#›

### Slide 40

MANAGING THE DATABASE SYSTEM: A SHIFT IN FOCUS

Database system provides a framework in which strict procedures and standards enforced

Role of human changes from programming to managing organization’s resources

Database system enables more sophisticated use of the data

Data structures created within the database and their relationships determine effectiveness

Database Systems, 9th Edition

‹#›

### Slide 41

MANAGING THE DATABASE SYSTEM: A SHIFT IN FOCUS (CONT'D.)

Disadvantages of database systems:

Increased costs

Management complexity

Maintaining concurrency

Vendor dependence

Frequent upgrade/replacement cycles

Database Systems, 9th Edition

‹#›

### Slide 42

SUMMARY

Data are raw facts

Information is the result of processing data to reveal its meaning

Accurate, relevant, and timely information is the key to good decision making

Data are usually stored in a database

DBMS implements a database and manages its contents

Database Systems, 9th Edition

‹#›

### Slide 43

SUMMARY (CONT'D.)

Metadata is data about data

Database design defines the database structure

Well-designed database facilitates data management and generates valuable information

Poorly designed database leads to bad decision making and organizational failure

Databases evolved from manual and computerized file systems

Database Systems, 9th Edition

‹#›

### Slide 44

SUMMARY (CONT'D.)

Database management systems were developed to address file system’s inherent weaknesses

DBMS present database to end user as single repository

Promotes data sharing

Eliminates islands of information

DBMS enforces data integrity, eliminates redundancy, and promotes security

Database Systems, 9th Edition

‹#›

### Slide 45

SUMMARY (CONT'D.)

In a file system, data stored in independent files

Each requires its own management program

Some limitations of file system data management:

Requires extensive programming

System administration is complex and difficult

Changing existing structures is difficult

Security features are likely inadequate

Independent files tend to contain redundant data

Structural and data dependency problems

Database Systems, 9th Edition

‹#›

### Slide 46

Q & A ?

---

## Lecture2-RELATIONALM0DEL.pptx

### Slide 1

Database Systems: Design, Implementation, and ManagementNinth Edition

Chapter 2

The Relational Database Model

### Slide 2

Objectives

In this chapter, students will learn:

That the relational database model offers a logical view of data

About the relational model’s basic component: relations

That relations are logical constructs composed of rows (tuples) and columns (attributes)

That relations are implemented as tables in a relational DBMS

Database Systems, 9th Edition

2

### Slide 3

Objectives (cont’d.)

About relational database operators, the data dictionary, and the system catalog

How data redundancy is handled in the relational database model

Why indexing is important

Database Systems, 9th Edition

3

### Slide 4

A Logical View of Data

Database Systems, 9th Edition

4

### Slide 5

Relational Model

A relational database collects different types of data sets that use tables, records, and columns.

It is used to create a well-defined relationship between database tables so that relational databases can be easily stored.

For example of relational databases such as Microsoft SQL Server, Oracle Database, MYSQL, etc.

There are some important parameters of the relational database:

It is based on a relational model (Data in tables).

Each row in the table with a unique id, key.

Columns of the table hold attributes of data.

### Slide 6

Tables and Their Characteristics

Database Systems, 9th Edition

6

### Slide 7

Database Systems, 9th Edition

7

### Slide 8

Database Systems, 9th Edition

8

### Slide 9

Keys

Database Systems, 9th Edition

9

### Slide 10

Keys (cont’d.)

Database Systems, 9th Edition

10

### Slide 12

Keys (cont’d.)

Nulls

No data entry

Not permitted in primary key

Should be avoided in other attributes

Can represent:

An unknown attribute value

A known, but missing, attribute value

A “not applicable” condition

Database Systems, 9th Edition

12

### Slide 13

Keys (cont’d.)

Nulls (cont’d.)

Can create problems when functions such as COUNT, AVERAGE, and SUM are used

Can create logical problems when relational tables are linked

Database Systems, 9th Edition

13

### Slide 14

Keys (cont’d.)

Controlled redundancy

Makes the relational database work

Tables within the database share common attributes

Enables tables to be linked together

Multiple occurrences of values not redundant when required to make the relationship work

Redundancy exists only when there is unnecessary duplication of attribute values

Database Systems, 9th Edition

14

### Slide 15

Database Systems, 9th Edition

15

### Slide 16

Database Systems, 9th Edition

16

### Slide 17

Keys (cont’d.)

Database Systems, 9th Edition

17

### Slide 18

Database Systems, 9th Edition

18

### Slide 19

QUICK TUTORIAL

Simplify the table below to a relational schema

Underline the Primary key and Foreign key

### Slide 20

Sample solutions- Relational Schema

### Slide 21

Integrity Rules

Database Systems, 9th Edition

21

### Slide 22

Database Systems, 9th Edition

22

### Slide 23

Database Systems, 9th Edition

23

### Slide 24

The Data Dictionary and System Catalog

Database Systems, 9th Edition

24

### Slide 25

Database Systems, 9th Edition

25

### Slide 26

Relationships within the Relational Database

1:M relationship

Relational modeling ideal

Should be the norm in any relational database design

1:1 relationship

Should be rare in any relational database design

Database Systems, 9th Edition

26

### Slide 27

Relationships within the Relational Database (cont’d.)

M:N relationships

Cannot be implemented as such in the relational model

M:N relationships can be changed into 1:M relationships

Database Systems, 9th Edition

27

### Slide 28

The 1:M Relationship

Relational database norm

Found in any database environment

Database Systems, 9th Edition

28

### Slide 29

Database Systems, 9th Edition

29

### Slide 30

The 1:1 Relationship

Database Systems, 9th Edition

30

### Slide 31

Database Systems, 9th Edition

31

### Slide 32

The M:N Relationship

Implemented by breaking it up to produce a set of 1:M relationships

Avoid problems inherent to M:N relationship by creating a composite entity

Includes as foreign keys the primary keys of tables to be linked

Database Systems, 9th Edition

32

### Slide 33

Database Systems, 9th Edition

33

### Slide 34

Database Systems, 9th Edition

34

### Slide 35

Database Systems, 9th Edition

35

### Slide 36

Database Systems, 9th Edition

36

### Slide 37

Database Systems, 9th Edition

37

### Slide 38

Data Redundancy Revisited

Data redundancy leads to data anomalies

Can destroy the effectiveness of the database

Foreign keys

Control data redundancies by using common attributes shared by tables

Crucial to exercising data redundancy control

Database Systems, 9th Edition

38

### Slide 39

Database Systems, 9th Edition

39

### Slide 40

Indexes

Orderly arrangement to logically access rows in a table

Index key

Index’s reference point

Points to data location identified by the key

Unique index

Index in which the index key can have only one pointer value (row) associated with it

Each index is associated with only one table

Database Systems, 9th Edition

40

### Slide 41

Database Systems, 9th Edition

41

### Slide 42

Relational Set Operators

Relational algebra

Defines theoretical way of manipulating table contents using relational operators

Use of relational algebra operators on existing relations produces new relations:

Database Systems, 9th Edition

42

### Slide 43

Database Systems, 9th Edition

43

The SELECT statement is used to select data from a database. The data returned is stored in a result table, called the result-set.

### Slide 44

Database Systems, 9th Edition

44

selecting the values of a few attributes, rather than selection all attributes of the Table (Relation),

### Slide 45

Database Systems, 9th Edition

45

UNION : Combine all results from two table into a single result, omitting any duplicates.

INTERSECT : Combine only those rows which the results of two table have in common, omitting any duplicates.

### Slide 46

Database Systems, 9th Edition

46

DIFFERENCE yields all rows in one table that are not found in the other table;

PRODUCT yields all possible pairs of rows from two tables—also known as the Cartesian product.

### Slide 47

Relational Set Operators (cont’d.)

Database Systems, 9th Edition

47

### Slide 50

Database Systems, 9th Edition

50

### Slide 51

Database Systems, 9th Edition

51

### Slide 52

Database Systems, 9th Edition

52

### Slide 53

Database Systems, 9th Edition

53

### Slide 54

Database Systems, 9th Edition

54

### Slide 55

Summary

Tables are basic building blocks of a relational database

Keys are central to the use of relational tables

Keys define functional dependencies

Superkey

Candidate key

Primary key

Secondary key

Foreign key

Database Systems, 9th Edition

55

### Slide 56

Summary (cont’d.)

Each table row must have a primary key that uniquely identifies all attributes

Tables are linked by common attributes

Good design begins by identifying entities, attributes, and relationships

1:1, 1:M, M:N

The relational model supports relational algebra functions

SELECT, PROJECT, JOIN, INTERSECT UNION, DIFFERENCE, PRODUCT, DIVIDE

Database Systems, 9th Edition

56

---