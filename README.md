# configator



## Development

### Prerequisites

Start a redis instance:

```shell
docker run --name redis-server -d redis redis-server --appendonly yes
```

### Unit tests

Clone the source code from the github repository:

```shell
git clone https://github.com/skelethon/configator.git
```

Change the project home to the working directory:

```shell
cd configator
```

Create a virtual environment:

```shell
python3 -m venv .env
```

Activate the virtual environment:

```shell
source ./.env/bin/activate
```

Upgrade python tools:

```shell
python3 -m pip install --upgrade pip setuptools wheel
```

Install requirements:

```shell
python3 -m pip install -r requirements.txt
```

Run the unittests:

```shell
python3 tests/units
```

### Examples

Start the subscriber:

```shell
python3 tests/examples/subscriber.py
```

Run the publisher:

```shell
python3 tests/examples/publisher.py
```
