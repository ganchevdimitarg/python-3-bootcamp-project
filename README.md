# Create a env
```sh
pip install fastapi 
pip install "uvicorn[standard]"
fastapienv\Scripts\activate.bat
```
# Start the server uvicorn
```sh
uvicorn books:app --reload 
```
or
for production 
```sh
fastapi run books.py
```
or
for dev 
```sh
fastapi dev books.py
```
# for data parsing and validation
```python
from pydantic import BaseModel
```

# data mapper
```python
new_object = CustomObject(**request_body.model_dump())
```

# for optional data
```python
id: Optional[int] = None
```

# for Path and Query parameters validation; HTTPException
```python
from fastapi import FastAPI, Path, Query, HTTPException
```

# for custom status code
```python
from starlette import status
@app.get("/v2/books", status_code=status.HTTP_200_OK)
```

# SQL ORM
```python
pip install sqlalchemy
```

# for Bcrypt
```sh
pip install passlib bcrypt==4.0.1
```

# to submit forms to the app
```sh
pip install python-multipart
```

# for more secure form use 
```python
from fastapi.security import OAuth2PasswordRequestForm
```

# to use JWT token 
```sh
pip install "python-jose[cryptography]"
```

# for using psql
```sh
pip install psycopg2-binary
```

# for using mysql
```sh
pip install pymysql
```

# for migration and modification of existing database schemas
```sh
pip install alembic
```

| Alembic Command                     | Details                                      |
|-------------------------------------|----------------------------------------------|
| `alembic init <folder name>`        | Initializes a new, generic environment       |
| `alembic revision -m <message>`     | Creates a new revision of the environment    |
| `alembic upgrade <revision #>`      | Run our upgrade migration to our database    |
| `alembic downgrade -1`              | Run our downgrade migration to our database  |

# to set up the alembic, should change this line of code in alembic.init file:
# sqlalchemy.url = '' with the url that connects to the database 
# and also have to change a couple of lines in alembic/env file
```python
import models

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
# if config.config_file_name is not None:
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = models.Base.metadata
```

# testing tool pytest
```sh
pip install pytest
pip install httpx
```