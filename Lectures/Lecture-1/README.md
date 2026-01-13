# LECTURE SHEET 01: Introduction & Architecture

Here is Lecture Sheet 01 with the SmartCampus (University Management System) capstone integration.  
I have kept the text, structure, and academic rigor exactly as provided, only swapping the specific "UrbanLogistics/Ride-Sharing" examples for "SmartCampus/University" examples where applicable.

**Course:** CSE 3523 – Database Management Systems  
**Module:** 1 (The Foundation)  
**Duration:** 1 Hour 20 Minutes  

**Primary Reference:**  
[S] Silberschatz, Korth, & Sudarshan, *Database System Concepts* (7th Edition), Chapter 1  

**Secondary Reference:**  
[AP] Dimitri Fontaine, *The Art of PostgreSQL*

---

## 1. History & Evolution of Data Systems

Before defining what a database is, we must understand how we got here.  
The evolution of data storage parallels the evolution of computing itself.

---

### 1960s: The Dawn of Databases and the Space Age  
#### Hierarchical Data Model

**Context:**  
Computers were large mainframes. Storage relied on magnetic tape and early disk drives. Programs and data were tightly coupled, and performance mattered more than flexibility.

**Milestone:**  
IBM developed IBM IMS (Information Management System) in the late 1960s. It was famously used by NASA during the Apollo Program to manage vast bills of materials for the Saturn V rocket.

**Structure:**  
Data followed a strict hierarchical, tree-like structure. Each record had exactly one parent.

**Example logic:**  

    Rocket -> Stage 1 -> Engine -> Pump -> Bolt

To find a "Bolt," the system had to navigate the full path from the root.

**Limitations:**  
Extremely rigid structure. Data access paths were hard-coded into applications. Any structural change required rewriting application logic. IMS was fast and reliable, but tightly locked to its data model.

---

### 1970: The Mathematical Breakthrough  
#### The Relational Model

**Event:**  
In 1970, Edgar F. Codd, a researcher at IBM, published the landmark paper  
“A Relational Model of Data for Large Shared Data Banks.”

**The Shift:**  
Codd proposed a radical idea:
- Store data as relations (tables)
- Describe data logically, not physically
- Access data using declarative queries instead of navigation paths

**Why This Mattered:**  
This separated logical data design from physical storage, and applications from data structure.

---

### 1974–1979: From Theory to Practice  
#### System R and SQL

**Milestone:**  
IBM built System R, the first working prototype of a relational database management system (RDBMS).

**Language Innovation:**  
IBM researchers developed SEQUEL (Structured English Query Language), later renamed SQL.  
It introduced SELECT, INSERT, UPDATE, DELETE and set-based operations.

**Commercialization:**  
While IBM moved cautiously, Oracle (founded by Larry Ellison) released the first commercially successful SQL-based relational database in 1979, beating IBM to market.

---

### 1980s–1990s: The Relational Era

Relational databases became the backbone of enterprise computing (Banking, Airlines, Government).  
Vendors focused on ACID transactions, data integrity, and vertical scaling.

---

### 2008–Present: Web Scale, NoSQL, and NewSQL

**Context:**  
The rise of Google, Amazon, and Facebook created new challenges (massive data, global distribution).

**The Shift (NoSQL):**  
Databases like DynamoDB and MongoDB emerged to prioritize scalability and availability, often relaxing strict consistency.

**The Current Trend:**  
Convergence. Modern SQL engines (like PostgreSQL) now support JSON and semi-structured data, while NewSQL systems aim to preserve ACID guarantees while scaling horizontally.

---

### Why This History Matters

Every database model emerged to solve a real problem of its time.  
Understanding this evolution helps students see databases not as static tools, but as engineering responses to changing constraints.

---

## 2. Definition & Purpose of a DBMS  
**(Ref: [S] Section 1.1)**

### Academic Definition

A Database-Management System (DBMS) is a collection of interrelated data and a set of programs to access those data.  
The collection of data, usually referred to as the database, contains information relevant to an enterprise.  
The primary goal of a DBMS is to provide a way to store and retrieve database information that is both convenient and efficient.

### Key Components

- **The Database:**  
  The physical collection of data (e.g., the SmartCampus student records and transcripts).

- **The DBMS Software:**  
  The system that manages access, locking, and crash recovery (e.g., PostgreSQL, Oracle).

---

## 3. Disadvantages of File-Processing Systems  
**(Ref: [S] Section 1.2)**

To understand the value of a DBMS, it is useful to first examine why traditional file-processing systems fail.  
Here, “file-processing” refers to applications that store and manage data directly in flat files such as CSV or text files using programming logic (for example, Python scripts).

---

### 3.1 Data Redundancy and Inconsistency

In file-processing systems, data files and application programs are often created independently by different programmers over time.  
As a result, the same data item may be stored in multiple files (data redundancy).  
When one copy is updated and others are not, the system suffers from data inconsistency, where multiple versions of the same data no longer agree.

#### [Live Demo]: The "Address Update" Failure

**Scenario:**  
We maintain two separate files for students:
- `library.csv` for the Library System (book loans)
- `fees.csv` for the Bursar/Accounts Office (tuition billing)

Both files store the student's address.  
A student moves to a new dorm.  
The change is applied to the Library file but forgotten in the Fees file.

**A. File-Processing Approach (Problematic)**

    import pandas as pd

    library_df = pd.read_csv("library.csv")  # Contains address
    fees_df = pd.read_csv("fees.csv")        # Also contains address

    def update_student_address(student_id, new_address):
        library_df.loc[library_df['id'] == student_id, 'address'] = new_address
        library_df.to_csv("library.csv", index=False)
        print("Library records updated.")

        # Fees/Bursar file is NOT updated
        # RESULT: Data inconsistency (tuition bill goes to wrong house)

**What Goes Wrong**
- The address exists in more than one file
- The update logic is embedded in application code
- Forgetting one update leads to inconsistent data

**B. DBMS Solution: Normalization and Single Source of Truth**

In a relational DBMS, data is normalized so that each fact is stored in exactly one place.  
The student's address is stored once, in a central table (`students`).  
Library and Fees modules do not maintain their own copies of the address; they query the same underlying data.

    UPDATE students
    SET address = '123 New Dorm Hall'
    WHERE student_id = 'S-101';

    SELECT address FROM students WHERE student_id = 'S-101';

---

## 4. Data Abstraction  
**(Ref: [S] Section 1.3)**

A major purpose of a database system is to provide users with an abstract view of the data.  
That is, the system hides certain details of how the data are stored and maintained.

### 4.1 The Three Levels of Abstraction

![Three Levels of Data Abstraction](figures/three-levels-abstraction.png)

- **Physical Level:** How data is stored
- **Logical Level:** What data is stored and relationships exist
- **View Level:** What each user or application sees

### 4.2 Physical Data Independence

The ability to modify the physical schema without causing application programs to be rewritten.

**Example**
- Migrating from HDD to NVMe SSD
- Introducing partitioning
- Application queries remain unchanged

---

## 5. Database Architecture  
**(Ref: [S] Section 1.4)**

A DBMS consists of modular components.

### Query Processor
- DDL Interpreter
- DML Compiler
- Query Evaluation Engine

### Storage Manager
- Buffer Manager
- File Manager
- Transaction Manager

Databases aggressively cache data in memory to minimize disk I/O.

---

## Closing Thought

Databases are not buckets where data is dumped.  
They are engines that preserve correctness under hardware failure, software crashes, and massive concurrency.

This course studies how those engines work.
