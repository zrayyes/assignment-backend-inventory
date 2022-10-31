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

Visit `http://localhost:8000/health_check`

## Usage

---

### Create Storage Space

POST -> `/storage/space`  
JSON body:

- name (str): Name of storage space.
- capacity (int): Maximum capacity of storage space.
- is_refrigerated (bool): Is this storage space refrigerated.

```bash
curl -X 'POST' 'http://localhost:8000/storage/space' -H 'Content-Type: application/json' -d '{"name":"small storage space", "capacity":15, "is_refrigerated": true}'
```

### Rename Storage Space

PATCH -> `/storage/space/<storage_id>`  
JSON body:

- name (str): The new name for storage space.

```bash
curl -X 'PATCH' 'http://localhost:8000/storage/space/1' -H 'Content-Type: application/json' -d '{"name":"my new space"}'
```

### Delete Storage Space

DELETE -> `/storage/space/<storage_id>`  
Fails if items attached.

```bash
curl -X 'DELETE' 'http://localhost:8000/storage/space/1'
```

### Get all items for Storage Space

GET -> `/storage/space/<storage_id>?sort=[ASC,DESC]&count=1&offset=0`  
Optional Parameters:

- sort (ASC|DESC): Sort items by expiry date, either ascending or descending.
- count (int): Number of items to return
- offset (int): Number of items to skip

```bash
curl -X 'GET' 'http://localhost:8000/storage/space/1?sort=ASC&count=1&offset=0'
```

### Create Item Type

POST -> `/storage/item_type`  
JSON body:

- name (str): Name of item type. Cannot be duplicate of existing item type.
- needs_fridge (bool): Does this item type need a refrigerated storage space.

```bash
curl -X 'POST' 'http://localhost:8000/storage/item_type' -H 'Content-Type: application/json' -d '{"name":"Frozen Pizza", "needs_fridge": true}'
```

### Rename Item Type

PATCH -> `/storage/item_type/<item_type_id>`  
JSON body:

- name (str): The new name of item type. Cannot be duplicate of existing item type.

```bash
curl -X 'PATCH' 'http://localhost:8000/storage/item_type/1' -H 'Content-Type: application/json' -d '{"name":"Better Frozen Pizza"}'
```

### Delete Item Type

DELETE -> `/storage/item_type/<item_type_id>`  
Fails if items attached.

```bash
curl -X 'DELETE' 'http://localhost:8000/storage/item_type/1'
```

### Create Item

POST -> `/storage/item`  
JSON body:

- expiry_date (str): Expiration date formatted as dd/mm/yyyy. Has to be in the future.
- storage_space_id (int): ID of storage space to add this item to.
- item_type_id (int): ID of item type this item belongs to.

```bash
curl -X 'POST' 'http://localhost:8000/storage/item' -H 'Content-Type: application/json' -d '{"expiry_date":"21/10/2040", "storage_space_id":1, "item_type_id": 1}'
```

### Move Item to new Storage Space

PATCH -> `/storage/item/<item_id>`  
JSON body:

- storage_space_id (id): The ID of the storage space to be moved to. Fails if storage space incompatible.

```bash
curl -X 'PATCH' 'http://localhost:8000/storage/item/1' -H 'Content-Type: application/json' -d '{"storage_space_id":2}'
```

### Delete Item

DELETE -> `/storage/item/<item_id>`  

```bash
curl -X 'DELETE' 'http://localhost:8000/storage/item/1'
```

## Design?

### Models
