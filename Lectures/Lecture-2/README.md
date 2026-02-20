# LECTURE SHEET 02: Data Models and the Relational Model. Relations, Tuples, Keys, Schema vs Instance

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

Underlying the structure of a database is the data model: a collection of conceptual tools for describing data, relationships, semantics, and consistency constraints.

Data models can be classified into four categories:

* **Relational Model.** The relational model uses a collection of tables to represent data and relationships. Each table has multiple columns (also called field or attribute) with unique names. Tables are also known as relations. Each row represents one piece of information known as record. It is a record-based model where the database is structured in fixed-format records. Each record type defines a fixed number of attributes. The relational model is the most widely used data model.
Example tables:
    * **Instructor**: shows instructor details such as ID, name, department, and salary.
    * **Department**: shows department details such as department name, building and budget.
 ![](./instructor.png)
 ![](./department.png)

* **Entity-Relationship Model.**  The entity-relationship (E-R) data model uses a collection of basic objects, called entities,and relationships among these objects. An entity is a “thing” or “object” in the real world that is distinguishable from other
objects. The entity-relationship model is widely used in database design.
![](./ERDiagram.png)

* **Semi-structured Data Model.** Traditional models assume a closed-world, schema-first universe. Semi-structured data models assume an open-world, schema-later universe. It permits the specification of data where individual data items of the same type may have different sets of attributes. This is in contrast to the data models mentioned earlier, where
every data item of a particular type must have the same set of attributes. JSON and Extensible Markup Language (XML) are widely used semi-structured data represen tations. 
Following is the JSON and XML examples respectively:
    
    JSON:
    ```
    {
    "student": {
        "student_id": "S101",
        "name": "Rahim Uddin",
        "email": "rahim@example.com",
        "date_of_birth": "2005-03-15",
        }
    }
    ```
    XML:
    ```
    <student>
        <student_id>S101</student_id>
        <name>Rahim Uddin</name>
        <email>rahim@example.com</email>
        <date_of_birth>2005-03-15</date_of_birth>
    </student>
    ```

* **Object-Based Data Model.**  Object-oriented programming (especially in python, Java, C++, or C#) has become the dominant software-development methodology. This led initially to the development of a distinct object-oriented data model, but today the
concept of objects is well integrated into relational databases. Standards exist to store objects in relational tables. Database systems allow procedures to be stored in the database system and executed by the database system.
    
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

## Instances and Schemas

Databases change over time. The collection of information stored in the database at a particular moment is called an **instance** of the database. The overall design of the database is called the **schema**.

Database systems have multiple schemas:

* **Physical schema** – describes design at the physical level.
* **Logical schema** – describes design at the logical level.
* **View schema (subschema)** – describes different user views.

The logical schema is most important for applications. The physical schema can be changed without affecting applications (physical data independence).

Poor schema design may cause duplicated information. For example, storing department budget in instructor records would require updating many records when the budget changes.

## Database Languages
A database system provides a data-definition language (DDL) to specify the database schema and a data-manipulation language (DML) to express database queries and up dates. In practice, the data-definition and data-manipulation languages are not two sep
arate languages; instead they simply form parts of a single database language, such as the SQL language. Almost all relational database systems employ the SQL language.

### Data-Definition Language
We specify a database schema by a set of definitions expressed by a special language called a data-definition language (DDL). The DDL is also used to specify additional properties of the data.
SQL provides a rich DDL that allows one to define tables with data types and integrity constraints. For instance, the following SQL DDL statement defines the department table:
<code>create table department
(dept name char (20),
building char (15),
budget numeric (12,2));
</code>
Execution of the preceding DDL statement creates the department table with three columns: dept name, building, and budget, each of which has a specific data type asso ciated with it. 

### Data-Manipulation Language
Adata-manipulation language (DML) is a language that enables users to access or manipulate data as organized by the appropriate data model. The types of access are:
* Retrieval of information stored in the database.
* Insertion of new information into the database. 
* Deletion of information from the database.
* Modification of information stored in the database.

There are basically two types of data-manipulation language:
* Procedural DMLs require a user to specify what data are needed and how to get those data.
* Declarative DMLs (also referred to as nonprocedural DMLs)requireausertospecify what data are needed without specifying how to get those data.
Declarative DMLs are usually easier to learn and use than are procedural DMLs.
However, since a user does not have to specify how to get the data, the database system
has to figure out an efficient means of accessing data.
A query is a statement requesting the retrieval of information. The portion of a
DMLthatinvolvesinformationretrievaliscalledaquerylanguage.Althoughtechnically
incorrect, it is common practice to use the terms query language and data-manipulation
language synonymously.
There are a number of database query languages in use, either commercially or
experimentally.