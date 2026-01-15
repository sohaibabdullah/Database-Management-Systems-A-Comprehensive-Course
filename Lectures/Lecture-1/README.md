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

    -- DBMS APPROACH (CORRECT)
    
    -- Update the single source of truth
    UPDATE students
    SET address = '123 New Dorm Hall'
    WHERE student_id = 'S-101';
    
    -- Both Library and Fees now read the same data:
    -- Used by Library
    SELECT address FROM students WHERE student_id = 'S-101';
    
    -- Used by Fees/Bursar
    SELECT address FROM students WHERE student_id = 'S-101';
    
### 3.2 Atomicity Problems
**Formal Definition:**
A logical unit of work (a Transaction) must be atomic—it must happen in its entirety or not at all. Computer systems are subject to failure (power loss, crash). If a failure occurs during a complex update, the data must be restored to the consistent state that existed prior to the failure.

**[Live Demo]: The "Lost Tuition" Crash**

Scenario: A Student (ID 101) pays 50,000 BDT tuition to the University.

**A. The Flawed Python/CSV Approach:**

    # FILE SYSTEM CRASH SIMULATION
    def pay_tuition_unsafe():
        # 1. Read Student Bank Balance
        student_bal = read_balance_from_file("student_bank.txt") # 100,000
        
        # 2. Deduct Money from Student
        write_balance_to_file("student_bank.txt", student_bal - 50000) # Writes 50,000
        
        print("Money deducted. Writing to University Ledger...")
        
        # --- SIMULATED POWER FAILURE ---
        raise Exception("CRASH! Server Power Lost.") 
        
        # 3. Credit University (This line never runs)
        univ_bal = read_balance_from_file("university_ledger.txt")
        write_balance_to_file("university_ledger.txt", univ_bal + 50000)

    # RESULT: Student has lost 50,000. The university received 0. Money vanished.

**B. The DBMS Solution (ACID [(Atomicity, Consistency, Isolation, Durability)] Transactions):**
ACID transactions are database protocols that ensure reliability through four properties: Atomicity (all-or-nothing), Consistency (valid state transitions), Isolation (independent execution), and Durability (permanent changes). ACID transactions guarantee reliable, fault-tolerant data processing, with Write-Ahead Logging (WAL) being a core mechanism, especially for Durability and Consistency.

PostgreSQL uses Write-Ahead Logging (WAL). If a crash happens before COMMIT, the database automatically "Rolls Back" the changes upon restart.

    # POSTGRESQL APPROACH (SAFE)
    import psycopg2
    
    conn = psycopg2.connect("dbname=smartcampus")
    cur = conn.cursor()
    
    try:
        # Start Transaction
        cur.execute("BEGIN;") 
        
        # Step 1: Deduct from Student
        cur.execute("UPDATE students SET bank_balance = bank_balance - 50000 WHERE id = 101;")
        
        # --- IF CRASH HAPPENS HERE, POSTGRES AUTO-ROLLBACKS ---
        # The 'BEGIN' block is not saved to disk until 'COMMIT' is received.
        
        # Step 2: Credit University
        cur.execute("UPDATE university_ledger SET balance = balance + 50000;")
        
        # Save Changes
        cur.execute("COMMIT;") 
        print("Transaction Successful.")
        
    except Exception as e:
        cur.execute("ROLLBACK;") # Explicit undo if code errors
        print("Error detected. No money changed hands.")
###3.3 Concurrent Access Anomalies
Formal Definition:
For performance, systems allow multiple users to update data simultaneously. Without supervision, this leads to inconsistency.

**[Scenario]: The Race Condition (Enrollment Day)**
-Case: Course CSE 3523 has 50 seats. Currently, 49 are taken. Two students click "Register" at the exact same millisecond.
-File System: Both Python scripts read the file: "Seats Taken = 49". Both scripts decide "Space Available!" Both overwrite the file with "Seats Taken = 50".
-Result: 51 students are enrolled in a 50-seat room. The file is corrupted.
-DBMS Solution: Locking.

    SELECT * FROM courses WHERE course_id='CSE3523' FOR UPDATE;
    
    This SQL command tells the database: "Lock this row. Nobody else can touch it until I am done." The       second student's query will wait (block) until the first one finishes.
---

## 4. Data Abstraction  
**(Ref: [S] Section 1.3)**

A major purpose of a database system is to provide users with an abstract view of the data.  
That is, the system hides certain details of how the data are stored and maintained.

### 4.1 The Three Levels of Abstraction

![Three Levels of Data Abstraction](figures/three-levels-abstraction.png)

1. **Physical Level (The "How"):**
    *   **Definition:** Describes complex low-level data structures.
    *   **Example:** "The Student record is stored in Block #4096 on the SSD using a Heap File structure. The index is a B-Tree located in Block #5000."
    *   **User:** Database Administrator (DBA).

2.  **Logical Level (The "What"):**
    *   **Definition:** Describes what data are stored in the database and what relationships exist among those data.
    *   **Example:** `type Student = record (name: string, dept: string, credits: integer)`.
    *   **User:** YOU (Backend Application Developer).

3.  **View Level (The "Perspective"):**
    *   **Definition:** Describes only part of the entire database.
    *   **Example:** The "Student Portal" view shows grades but hides "Faculty Salaries".
    *   **User:** End-user applications.

### 4.2 Physical Data Independence

The ability to modify the physical schema without causing application programs to be rewritten.

**Example**
**Industry Scenario:**
-Day 1: Your SmartCampus system uses a cheap standard Hard Drive (HDD).
--Day 100: You have 50,000 students. The HDD is too slow during enrollment.
Action: You migrate the data to a high-performance NVMe SSD array and introduce "Partitioning" (splitting data across disks).
-Result: The Logical Schema (Table definitions) remains unchanged. The Python code (SELECT * FROM students) remains unchanged. The DBMS handles the physical mapping.


---

## 5. Database Architecture  
**(Ref: [S] Section 1.4)**

A DBMS consists of modular components.

### Query Processor
-DDL Interpreter: Interprets schema definitions (CREATE TABLE).
-DML Compiler: Translates query language statements (SELECT) into an evaluation plan.
-Query Evaluation Engine: Executes the low-level instructions generated by the compiler.

### Storage Manager
- Buffer Manager (Critical): Manages the partitioning of main memory (RAM) to cache data blocks. Databases try to avoid Disk I/O at all costs.
-Transaction Manager: Ensures the ACID properties (Atomicity, Consistency, Isolation, Durability).
- File Manager

Databases aggressively cache data in memory to minimize disk I/O.

---

## Closing Thought

Databases are not buckets where data is dumped.  
They are engines that preserve correctness under hardware failure, software crashes, and massive concurrency.

This course studies how those engines work.
