# About projects
Admin panel for managing a private clinic and tracking financial indicators. It is planned to add access control for various categories of users.


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
- backend:
1. [Create virtual environment](https://docs.python.org/3/library/venv.html#creating-virtual-environments)
```
python -m venv ./backend/venv
```
2. [Activate virtual environment](https://docs.python.org/3/library/venv.html#how-venvs-work)
  ```
  source ./backend/venv/bin/activate
```
3. Install python package
```
python -m pip install -r ./backend/requirements.txt
```
4. Create secret key for encode and decode JWT token
```
openssl rand -hex 32 > .backend/app/security/secret_key.txt
```
5. Run uvicorn server
```
python ./backend/run_uvicorn.py
```
- frontend:
1. Change directory to `client/`
```
cd client/
```
2. Run frontend app 
  ```
  ./gradlew jsRun
```


### links to view the project
+ frontend: &nbsp; &nbsp; &nbsp; &nbsp; http://localhost:8000
  <br/> </br>
+ API docs
  - Swager: &nbsp; &nbsp; &nbsp; http://localhost:8080/docs
  - Redoc: &nbsp; &nbsp; &nbsp; &nbsp; http://localhost:8080/redoc
