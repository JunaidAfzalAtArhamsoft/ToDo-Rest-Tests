# ToDo App With Test Cases
## About
This app contains apis for following: 
- Create
- Update
- Retrive
- Delete
- SoftDelete
- Register User
- Forgot_password
- Show Currently login user profile

## Note:
Every Api required JWT Authentication and IsAuthenticated except following:
- Login
- Register
- Forgot Password

# Setup

## Database
This project used postgres database. 

### Database setup
To install and connecting database with django follow the following steps:
#### Install Postgres
**Create the file repository configuration**:


```sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'```

**Import the repository signing key:**


```wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -```

**Update the package lists:**

```sudo apt-get update```

**Install the latest version of PostgreSQL.**

```sudo apt-get -y install postgresql```

**If you want a specific version, use:

 ```sudo apt-get -y install postgresql-12```
 
 **Install client**
 
 ``` sudo apt-get install postgresql-client ```
 
 **additional supplied modules (part of the postgresql-xx package in version 10 and later)**
 
 ``` sudo apt-get install postgresql-contrib-9.x	``` 
 
 **libraries and headers for C language frontend development**

``` sudo apt-get install libpq-dev ```

**libraries and headers for C language backend development**

``` sudo apt-get install postgresql-server-dev```

## install pgadmin4 
- ``` curl https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo apt-key add - ```
- ``` sudo sh -c 'echo "deb https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/focal pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list' ```
- ``` sudo apt update ```
- ``` sudo apt install pgadmin4 ```

# Instructions

**Clone Project Using:**

``` git clone https://github.com/JunaidAfzalAtArhamsoft/ToDo-Rest-Tests.git ```

**Install Required Libraries**

``` pip3 install -r requirements.txt ```

**Create Migrations**

``` python3 manage.py makemigrations ```

**Migrate**

``` python3 manage.py migrate ```

**Run server**

 ``` python3 manage.py runserver ```
 
 # Results
 
 ## Results of test cases
 
  ``` python3 manage.py test ```
 
 ![test_cases_result](https://user-images.githubusercontent.com/93306663/143041681-d3a39382-c68f-4ecb-930b-d0eb7ec246f9.png)
 
**result = all test passed**
 
 ## Results of pylint
 
 
 ``` pylint to_do_api ```

 
 ![pylint_result](https://user-images.githubusercontent.com/93306663/143041863-bed9a774-f458-4fa5-8489-6b3367609207.png)
 
 
**result = 9.61 / 10**
