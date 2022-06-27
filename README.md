a PostgreSQL Database Column Encryption

## Introduction
This is the PoC for storing sensitive data in PostgreSQL datbase. Data will be encrypted transparently with help of SQLAlchemy and SQLUtils.

## Setup
```
cd pgdbencryption
python3.8 -mvenv venv
venv/bin/pip install -r requirements.txt
venv/bin/docker-compose up -d
sudo apt install postgresql-client
psql -U postgres -h localhost -d postgres
postgres=#create database pgdbencryption
postgres=#\l
postgres=#\q
flask run
```

## Test

### Using flask shell
```
flask shell
> from pgdbencryption import db
> from pgdbencryption.models import *
> ccdetails = {"name": "user1", "number": "1234-5678-9123", "cvv": "123"}}
> user1 = UserModel(name="user1", password="password1", ccdetails=ccdetails, ccdetails2=ccdetails)
> db.session.add(user1)
> db.session.commit()
> user = UserModel.query.all()[0]
> print(user.name)
print(user.password)
print(user.ccdetails["cvv"])
print(user.ccdetails2["cvv"])
```

Here in `ccdetails` column, we are storing encrypted information of credit card while `ccdetails2`, we are storing same information in plain text.
You can now visit database using psql client and verify

```
psql -U postgres -h localhost -d pgdbencryption
> \dt
> select * from users;
> \q
```

### Using curl


#### list users

```
curl -X GET http://localhost:5000/users/list -H 'Content-Type: application/json'
```

#### create users

```
curl -X POST http://localhost:5000/users/create -H 'Content-Type: application/json' -d '{"name": "user1", "password": "password1", "ccdetails": {"name": "user1", "number": "1234-5678-9123", "cvv": "123"}}'
curl -X POST http://localhost:5000/users/create -H 'Content-Type: application/json' -d '{"name": "user2", "password": "password2", "ccdetails": {"name": "user2", "number": "1234-5678-9123", "cvv": "123"}}'
curl -X POST http://localhost:5000/users/create -H 'Content-Type: application/json' -d '{"name": "user3", "password": "password3", "ccdetails": {"name": "user3", "number": "1234-5678-9123", "cvv": "123"}}'
```

#### update users

```
curl -X PUT http://localhost:5000/users/update?user=3 -H 'Content-Type: application/json' -d '{"password": "password-updated", "ccdetails": {"name": "user3", "number": "1234-5678-9123-updated", "cvv": "123-updated"}}'
```

#### delete users

```
curl -X DELETE http://localhost:5000/users/delete?user=3 -H 'Content-Type: application/json'
```
