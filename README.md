# About projects
Admin panel for managing a private clinic and tracking financial indicators. This is practical work at the university.


## Stack used
- backend
  + Python
  + FastAPI
  + SQLAlchemy
  + Pytest
- frontend
    + Kotlin mutliplatform
    + Kotlin/JS 
    + Ktor client
    + Kvision (*web framework for Kotlin/JS*)


## Run project
0. Install docker and docker compose

2. Create file `db_password.txt` with password from postgresql db in root dir

3. Run:
```
docker compose up
```


### links to view the project
+ frontend: &nbsp; &nbsp; &nbsp; &nbsp; http://localhost:8000
  <br/> </br>
+ API docs
  - Swager: &nbsp; &nbsp; &nbsp; http://localhost:8080/docs
  - Redoc: &nbsp; &nbsp; &nbsp; &nbsp; http://localhost:8080/redoc
