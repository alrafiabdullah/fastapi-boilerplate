# FastAPI Boilerplate

##

## Requirements

- Create and activate a virtual environment
- Run `pip3 install -r requirements.txt`
- Create a `.env` file in the root directory of the project and copy the following:

```
PG_USER=
PG_PASSWORD=
PG_HOST=
PG_PORT=
PG_NAME=
```

- Run `uvicorn main:app --reload`
- The swagger schema will be available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Features

- [x] User CRUD
- [x] User authentication
- [x] User password hashing
- [x] User password change

##
