# configator

## Development guide

### Prerequisites

Start a redis instance:

```shell
docker run -d \
-p 6379:6379 \
--name redis-server \
redis \
redis-server --appendonly yes
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

| Tables   |      Are      |  Cool |
|----------|:-------------:|------:|
| col 1 is |  left-aligned | $1600 |
| col 2 is |    centered   |   $12 |
| col 3 is | right-aligned |    $1 |



 First Header  | Second Header
  ------------- | -------------
  Content Cell  | Content Cell
  Content Cell  | Content Cell


|   |   |   |   |   |
|---|---|---|---|---|
|   |   |   |   |   |
|   |   |   |   |   |




[![IMAGE ALT TEXT HERE](https://www.google.com/url?sa=i&url=https%3A%2F%2Fvi.cleanpng.com%2Fkisspng-grmw6p%2F&psig=AOvVaw0tR6eKPRwHxUIQ3Wn7aHXx&ust=1617685084899000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCLjr9dio5u8CFQAAAAAdAAAAABAI)](https://www.youtube.com/watch?v=pfU0QORkRpY)



