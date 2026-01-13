# LECTURE SHEET 01: Introduction & Architecture

**Course:** CSE 3523 – Database Management Systems  
**Module:** 1 (The Foundation)  
**Duration:** 1 Hour 20 Minutes  

**Primary Reference:**  
Silberschatz, Korth, & Sudarshan, *Database System Concepts* (7th Edition), Chapter 1  

**Secondary Reference:**  
Dimitri Fontaine, *The Art of PostgreSQL*

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
- Store data as relations (tables)  
- Describe data logically, not physically  
- Access data using declarative queries instead of navigation paths  

**Why This Mattered:**  
This separated logical data design from physical storage, and applications from data structure.

[ADDED – academic clarification]  
This separation introduced the concept of **data independence**, a foundational principle of database systems that allows optimization and evolution without breaking applications.

---

### 1974–1979: From Theory to Practice  
#### System R and SQL

**Milestone:**  
IBM built System R, the first working prototype of a relational database management system (RDBMS).

**Language Innovation:**  
IBM researchers developed SEQUEL (Structured English Query Language), later renamed SQL. It introduced SELECT, INSERT, UPDATE, DELETE and set-based operations.

**Commercialization:**  
While IBM moved cautiously, Oracle (founded by Larry Ellison) released the first commercially successful SQL-based relational database in 1979, beating IBM to market.

---

### 1980s–1990s: The Relational Era

Relational databases became the backbone of enterprise computing (Banking, Airlines, Government). Vendors focused on ACID transactions, data integrity, and vertical scaling.

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

A Database-Management System (DBMS) is a collection of interrelated data and a set of programs to access those data. The collection of data, usually referred to as the database, contains information relevant to an enterprise. The primary goal of a DBMS is to provide a way to store and retrieve database information that is both convenient and efficient.

### Key Components

- **The Database:**  
  The physical collection of data (e.g., SmartCampus student records and transcripts).

- **The DBMS Software:**  
  The system that manages access, locking, and crash recovery (e.g., PostgreSQL, Oracle).

---

## 3. Disadvantages of File-Processing Systems  
**(Ref: [S] Section 1.2)**

To understand the value of a DBMS, it is useful to first examine why traditional file-processing systems fail.

---

### 3.1 Data Redundancy and Inconsistency

In file-processing systems, data files and application programs are often created independently by different programmers over time. As a result, the same data item may be stored in multiple files (data redundancy). When one copy is updated and others are not, the system suffers from data inconsistency.

#### Live Demo: The "Address Update" Failure

**Scenario:**  
We maintain two separate files for students:
- `library.csv` for the Library System  
- `fees.csv` for the Bursar/Accounts Office  

Both files store the student's address. A student moves to a new dorm. The change is applied to the Library file but forgotten in the Fees file.

**A. File-Processing Approach (Problematic)**

    import pandas as pd

    library_df = pd.read_csv("library.csv")
    fees_df = pd.read_csv("fees.csv")

    def update_student_address(student_id, new_address):
        library_df.loc[library_df['id'] == student_id, 'address'] = new_address
        library_df.to_csv("library.csv", index=False)
        print("Library records updated.")

**What Goes Wrong**
- Address duplicated across files  
- Update logic embedded in application code  
- Missing one update causes inconsistency  

---

**B. DBMS Solution: Normalization and Single Source of Truth**

    UPDATE students
    SET address = '123 New Dorm Hall'
    WHERE student_id = 'S-101';

    SELECT address FROM students WHERE student_id = 'S-101';

**Why This Works:**  
No data duplication. One update automatically affects all users of the data. Consistency is enforced by design.

---

### 3.2 Atomicity Problems

**Formal Definition:**  
A logical unit of work (a transaction) must be atomic—it must happen in its entirety or not at all.

#### Live Demo: The "Lost Tuition" Crash

**Scenario:**  
A student pays 50,000 BDT tuition to the university.

**A. File-Processing Approach**

    def pay_tuition_unsafe():
        student_bal = read_balance_from_file("student_bank.txt")
        write_balance_to_file("student_bank.txt", student_bal - 50000)
        raise Exception("CRASH!")
        univ_bal = read_balance_from_file("university_ledger.txt")
        write_balance_to_file("university_ledger.txt", univ_bal + 50000)

**Result:**  
Student lost 50,000. University received 0.

---

**B. DBMS Solution (ACID Transactions)**

    BEGIN;
    UPDATE students SET bank_balance = bank_balance - 50000 WHERE id = 101;
    UPDATE university_ledger SET balance = balance + 50000;
    COMMIT;

If a crash occurs before COMMIT, PostgreSQL automatically rolls back the transaction.

---

### 3.3 Concurrent Access Anomalies

**Scenario:**  
CSE 3523 has 50 seats. 49 are taken. Two students click "Register" at the same millisecond.

File system result:  
Both read 49. Both write 50. 51 students enrolled.

**DBMS Solution: Locking**

    SELECT * FROM courses
    WHERE course_id='CSE3523'
    FOR UPDATE;

---

## 4. Data Abstraction  
**(Ref: [S] Section 1.3)**

Databases provide an abstract view of data by hiding storage details.

### 4.1 Three Levels of Abstraction

![Three Levels of Abstraction](figures/three-levels-abstraction.png)

- **Physical Level:** How data is stored  
- **Logical Level:** What data is stored and relationships  
- **View Level:** What each user sees  

### 4.2 Physical Data Independence

Ability to modify the physical schema without changing application programs.

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

## Industry Incidents: Why This Matters

**Knight Capital (2012):**  
Lost $440 million in 45 minutes due to faulty deployment.  
https://en.wikipedia.org/wiki/Knight_Capital_Group

**GitHub Outage (2018):**  
MySQL replication failure caused data inconsistency.  
https://github.blog/2018-10-30-oct21-post-incident-analysis/

---

## Closing Thought

Databases are not buckets where data is dumped.  
They are engines that preserve correctness under failure, concurrency, and scale.

This course studies how those engines work.
