# LECTURE SHEET 02: Data Models and the Relational Model: Relations, Tuples, Keys, Schema vs Instance

**Course:** CSE 3523 – Database Management Systems  
**Module:** 1 (The Foundation)  
**Duration:** 1 Hour 20 Minutes  

**Primary Reference:**  
[S] Silberschatz, Korth, & Sudarshan, *Database System Concepts* (7th Edition), Chapter 1  

**Secondary References:**  
[K] Kleppmann, Riccomini – Designing Data-Intensive Applications, 2nd Edition
[AP] Dimitri Fontaine, *The Art of PostgreSQL*

---

# Data Models

**(Ref: [S] Section 1.3)**

Underlying the structure of a database is the data model: a collection of conceptual tools for describing data, relationships, semantics, and consistency constraints.

Data models can be classified into four categories:
1. Relational Model
2. Entity-Relationship Model
3. Semi-structured Data Model
4. Object-Based Data Model

* **Relational Model:** The relational model for database management was introduced by Edgar F. Codd (E.F. Codd), a British computer scientist working for IBM, in 1970 when he published his groundbreaking paper titled ["A Relational Model of Data for Large Shared Data Banks,"](https://www.seas.upenn.edu/~zives/03f/cis550/codd.pdf) in the ACM journal.

    The relational model uses a collection of **tables** to represent data and relationships. Each table has multiple **columns**(also called **field** or **attribute**) with unique names. Tables are also known as **relations**. Each row represents one piece of information known as **record**. 

    It is a record-based model where the database is structured in fixed-format records. Each record type defines a fixed number of attributes. 

    The relational model is the most widely used data model.

    Example tables/relations:
        * **Instructor**: shows instructor details such as ID, name, department, and salary.
        * **Department**: shows department details such as department name, building and budget.
    ![](./instructor.png)
    ![](./department.png)

    A **query** is a statement requesting the retrieval of information. When the relational model was introduced, it included a new way of querying data: **SQL**. SQL stands for **Structured Query Language**; the term defines a declarative programming language. 

    In a **declarative query language**, like SQL or relational algebra, we just specify the
    pattern of the data we want — **what** conditions the results must meet, and how we want it to be transformed (e.g. sorted, grouped and aggregated), but **not how** to achieve that goal. For example:
    ```
    SELECT * FROM student WHERE location = 'Mirpur';
    ```
    Databases change over time. The collection of information stored in the database at a particular moment is called an **instance** of the database. The overall design of the database is called the **schema**.

    A database system provides a **data-definition language (DDL)** to specify the database schema and a **data-manipulation language (DML)** to express database queries and updates. In practice, the data-definition and data-manipulation languages are not two separate languages; instead they simply form parts of a single database language, such as the SQL language. Example of DDL:
    ```
    create table department
    (dept name char (20),
    building char (15),
    budget numeric (12,2));
    ```

* **Entity-Relationship Model:**  The entity-relationship (E-R) data model uses a collection of basic objects, called entities,and relationships among these objects. An entity is a “thing” or “object” in the real world that is distinguishable from other
objects. The entity-relationship model is widely used in database design.
![](./ERDiagram.png)

* **Semi-structured Data Model:** Traditional models assume a closed-world, schema-first universe. Semi-structured data models assume an open-world, schema-later universe. It permits the specification of data where individual data items of the same type may have different sets of attributes. This is in contrast to the data models mentioned earlier, where every data item of a particular type must have the same set of attributes. JSON and Extensible Markup Language (XML) are widely used semi-structured data represen tations. 
Following is the JSON and XML examples respectively:
    
    JSON:
    ```
    {
        "students": [
            {
            "id": "101",
            "name": "Alice Johnson",
            "location": "New York"
            },
            {
            "id": "102",
            "name": "Bob Smith",
            "location": "London"
            }
        ]
    }

    ```
    XML:
    ```
    <?xml version="1.0" encoding="UTF-8"?>
    <institute>
        <student>
            <id>101</id>
            <name>Alice Johnson</name>
            <location>New York</location>
        </student>
        <student>
            <id>102</id>
            <name>Bob Smith</name>
            <location>London</location>
        </student>
    </institute>
    ```

* **Object-Based Data Model:**  Object-oriented programming (e.g., python, Java, C++, or C#) has become the dominant software-development methodology. This led initially to the development of a distinct object-oriented data model, but today the concept of objects is well integrated into relational databases. Standards exist to store objects in relational tables. Database systems allow procedures to be stored in the database system and executed by the database system.
    
    **Example**
    In Python, a Student is naturally modeled as an object:
    ```
    class Student:
        def __init__(self, name, marks):
            self.name = name
            self.marks = marks

        def get_grade(self):
            if self.marks >= 80:
                return "A"
            elif self.marks >=60:
                return "B"
            else:
                return "C"
    s = Student("Rahim", 85)
    print(s.get_grade())
    ```
    Here,

    name, marks → Data

    get_grade() → procedures/functions/methods

    Object-Based Model = Database + procedure

    But, A relational database stores only data.
    | name | marks |
    | Rahim| 85 |

    Some DBs (e.g., PostgreSQL) actually support object features:

    1. Create Table for Students
    ```
    CREATE TABLE Student(
    name TEXT,
    marks INT
    );

    INSERT INTO Student VALUES
    ('Rahim', 85),
    ('Karim', 72),
    ('Sumi', 90);
    ```

    2. Create Function to Calculate Grade
    ```
    CREATE FUNCTION get_grade(marks INT)
    RETURNS TEXT AS $$
    BEGIN
        IF marks >= 80 THEN
            RETURN 'A';
        ELSIF marks >= 60 THEN
            RETURN 'B';
        ELSE
            RETURN 'C';
        END IF;
    END;
    $$ LANGUAGE plpgsql;
    ```

    3. Test the Function
    ```
    SELECT name, marks, get_grade(marks) AS grade
    FROM Student;
    ```


    Python Demo with psycopg2
    ```
    import psycopg2

    conn = psycopg2.connect("dbname=yourdb user=postgres password=pass123 host=localhost")
    cur = conn.cursor()

    cur.execute("SELECT name, marks, get_grade(marks) FROM Student;")
    for row in cur.fetchall():
        print(row)

    conn.close()
    ```

