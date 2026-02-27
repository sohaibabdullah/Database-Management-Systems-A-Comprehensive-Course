# Lab 01: Exploring file-processing systems, Environment Setup & Starting with SQL

**Course:** CSE 3523S - Database Management Systems (Lab)  
**Instructor:** Sohaib Abdullah  
**Duration:** 2 Hours 20 Minutes  

---

## 1. Introduction
Welcome to the Database Lab! Today, we are going to complete three tasks:
1. Exploring file-processing systems
2. Setting-up Docker and PostgreSQL
3. Exploring the notion of integration of Object-based data model into relational database (PostgreSQL)

### Task-1: Exploring file-processing systems
In this task we will do the following:
1. Create a text file and write into it. [Text file writer](https://github.com/sohaibabdullah/Database-Management-Systems-A-Comprehensive-Course/blob/main/Sessionals/Lab-1/Task-1/filewrite.py) 
2. Open a text file or CSV file in read mode and read from it. [Text file reader](https://github.com/sohaibabdullah/Database-Management-Systems-A-Comprehensive-Course/blob/main/Sessionals/Lab-1/Task-1/filereader.py) [CSV file reader](https://github.com/sohaibabdullah/Database-Management-Systems-A-Comprehensive-Course/blob/main/Sessionals/Lab-1/Task-1/filereaderCSV.py)
3. Use python Pandas package to change a particular piece of data. [Text changer](https://github.com/sohaibabdullah/Database-Management-Systems-A-Comprehensive-Course/blob/main/Sessionals/Lab-1/Task-1/fileRWpandas.py) 

### Task-2: Environment Setup
#### 1. Install Docker Desktop (Windows): 
Docker is an open-source platform used to build, share, and run applications in isolated, standardized units called containers. Usually, to install PostgreSQL, you have to download a 200MB installer, click "Next" 10 times, and mess with Windows Registry. If you get a new laptop, you have to do it all over again.

**Infrastructure as Code (IaC)** means we write a small text file that *describes* the software we want. We give this file to Docker, and Docker automatically downloads and installs everything for us.

To install docker go to following [link](https://www.docker.com/products/docker-desktop/) and click the button "Download Docker Desktop"

