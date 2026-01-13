# Lecture 01: Introduction & Database Architecture

**Course:** CSE 3523 – Database Management Systems  
**Module:** 1 (The Foundation)  
**Duration:** 1 Hour 20 Minutes  

**Primary Reference:**  
Silberschatz, Korth, Sudarshan – Database System Concepts (7th Edition), Chapter 1  

**Secondary Reference:**  
Dimitri Fontaine – The Art of PostgreSQL  

---

## Learning Objectives

By the end of this lecture, students will be able to:

- Explain the historical evolution of database systems
- Define what a DBMS is and what problems it solves
- Identify limitations of file-processing systems
- Understand atomicity, concurrency, and data abstraction
- Describe the high-level architecture of a modern DBMS
- View databases as correctness-preserving engines rather than simple storage

---

## 1. History & Evolution of Data Systems

Before defining what a database is, we must understand how we got here.  
The evolution of data storage parallels the evolution of computing itself.

---

### 1.1 1960s: The Dawn of Databases and the Space Age

#### Hierarchical Data Model

**Context**
- Large mainframe computers
- Magnetic tape and early disk drives
- Programs and data tightly coupled
- Performance mattered more than flexibility

**Milestone**
- IBM developed IMS (Information Management System) in the late 1960s
- Used by NASA during the Apollo Program to manage bills of materials for the Saturn V rocket

**Structure**
- Strict hierarchical (tree-like) structure
- Each record has exactly one parent

**Example Navigation Path**

    Rocket → Stage 1 → Engine → Pump → Bolt

To find a “Bolt,” the system must traverse the entire hierarchy from the root.

**Limitations**
- Extremely rigid structure
- Access paths hard-coded into applications
- Structural changes require rewriting application logic

---

### 1.2 1970: The Relational Model

**Event**
- Edgar F. Codd published  
  “A Relational Model of Data for Large Shared Data Banks” (1970)

**Core Ideas**
- Store data as relations (tables)
- Describe data logically, not physically
- Access data using declarative queries

**Why This Mattered**
- Logical data independence
- Separation of applications from storage
- Foundation of modern databases

---

### 1.3 System R and SQL (1974–1979)

- IBM built System R, the first relational DBMS prototype
- SQL (originally SEQUEL) introduced declarative querying
- Oracle released the first commercial SQL database in 1979

---

### 1.4 Relational Era (1980s–1990s)

Relational databases dominated:
- Banking
- Airlines
- Government systems

Engineering focus:
- ACID properties
- Data integrity
- Vertical scaling

---

### 1.5 Web Scale, NoSQL, and Convergence (2008–Present)

- Massive data and global systems
- NoSQL prioritized scalability and availability
- Modern SQL systems now support JSON
- NewSQL preserves ACID while scaling horizontally

---

## 2. Definition & Purpose of a DBMS

**Reference:** Database System Concepts, Section 1.1

A DBMS is a collection of interrelated data and programs that provide efficient, reliable, and safe access to data relevant to an enterprise.

---

## 3. Disadvantages of File-Processing Systems

**Reference:** Database System Concepts, Section 1.2

---

### 3.1 Data Redundancy and Inconsistency

**Scenario**
- `library.csv` and `fees.csv` both store student addresses
- One update is forgotten

**File-Based Example**

    import pandas as pd

    library_df = pd.read_csv("library.csv")
    fees_df = pd.read_csv("fees.csv")

    def update_student_address(student_id, new_address):
        library_df.loc[library_df['id'] == student_id, 'address'] = new_address
        library_df.to_csv("library.csv", index=False)

**What Goes Wrong**
- Address duplicated across files
- Update logic embedded in application code
- Missing one update causes inconsistency

**DBMS Solution**

    UPDATE students
    SET address = '123 New Dorm Hall'
    WHERE student_id = 'S-101';

---

### 3.2 Atomicity Problems

**File-Based Failure**

    def pay_tuition_unsafe():
        write_balance("student.txt", 50000)
        raise Exception("CRASH!")
        write_balance("university.txt", 50000)

**DBMS Transaction**

    BEGIN;
    UPDATE students SET balance = balance - 50000 WHERE id = 101;
    UPDATE university_ledger SET balance = balance + 50000;
    COMMIT;

---

### 3.3 Concurrent Access Anomalies

**Race Condition Example**
- Two students register simultaneously
- 51 students enrolled in a 50-seat course

**DBMS Locking**

    SELECT *
    FROM courses
    WHERE course_id = 'CSE3523'
    FOR UPDATE;

---

## 4. Data Abstraction

**Reference:** Database System Concepts, Section 1.3

### Three Levels of Abstraction

![Three Levels of Data Abstraction](figures/three-levels-abstraction.png)

- Physical level
- Logical level
- View level

### Physical Data Independence

- Storage can change
- Applications remain unchanged

---

## 5. Database Architecture

**Reference:** Database System Concepts, Section 1.4

### Query Processor
- DDL Interpreter
- DML Compiler
- Query Evaluation Engine

### Storage Manager
- Buffer Manager
- File Manager
- Transaction Manager

---

## Industry Incidents

**Knight Capital (2012)**  
Lost $440 million in 45 minutes  
https://en.wikipedia.org/wiki/Knight_Capital_Group

**GitHub Outage (2018)**  
Replication failure caused inconsistency  
https://github.blog/2018-10-30-oct21-post-incident-analysis/

---

## Closing Thought

Databases are not buckets.  
They are engines that preserve correctness under failure, concurrency, and scale.
