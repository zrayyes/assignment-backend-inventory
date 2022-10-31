# Notes

## How to run?

You can run this service either with Docker or a local python 3.8+ installation.

### Using Docker

With Docker (and docker-compose) installed and running, you can run either of the following commands:

#### Via docker-compose

```bash
# create container
docker-compose up --build -d
# Create database tables. Only needed to run on new container
docker-compose exec store-backend python manage.py create_db
```

#### Via makefile (shortcut for docker-compose)

```bash
# create container
make up
# Create database tables. Only needed to run on new container
make create_db
```

You can then visit `http://localhost:8000/health_check` to check that the service is running successfully.  
You can also run `make seed_db` to add some dummy data to the database.

### Using Python

Tested on python3.8 and 3.10.

#### Install requirements

```bash
# optionally, consider using a virtual environment
pip install -r requirements.txt
```

#### Create Database Tables

```bash
python manage.py create_db
```

#### Start server

```bash
sanic src.server:create_app --factory --dev
```

Visit `http://localhost:8000/health_check`.

## Usage

### Create Storage Space

POST -> /storage/space  
JSON body:

- name (str): Name of storage space.
- capacity (int): Maximum capacity of storage space.
- is_refrigerated (bool): Is this storage space refrigerated.

```bash
curl -X 'POST' 'http://localhost:8000/storage/space' -H 'Content-Type: application/json' -d '{"name":"small storage space", "capacity":15, "is_refrigerated": true}'
```

### Item Type

### Item

## Design?

### Models
