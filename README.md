# Life

## An app to organize what you need to do in life

Visit at http://54.210.101.32:8106/

## Usage

Create an account and start adding what you need to do in the future.
Each item can be a place in four categories:
- A place you want to TRAVEL to
- A PROJECT you want to execute
- Something you want to DO
- Something you want to BUY

You have controls for:
- How much effort the task will take
- Personal or professional tagging
- Important x Urgent matrix
- Cost tagging
- Possible start and end dates
- If the task should be tagged as NEXT
- If the task was COMPLETED

BONUS
- You can expose your Google agenda alongside the tasks

### Development

Clone the repo
```
git clone https://github.com/GuiFV/life.git
```

Create a virtualenv
```
python3 -m venv venv
source venv/bin/activate
```

Create a .env file by copying the sample file (modify as needed)
```
cp .env.sample .env
```

Install the requirements
```
pip install -r requirements-dev.txt
```

Run the migrations
```
python manage.py migrate
```

Collect static files
```
python manage.py collectstatic
```

Run the server
```
python manage.py runserver
```

Access the app at http://localhost:8000

### Using Docker
Install Docker and docker-compose

Clone the repo
```
git clone https://github.com/GuiFV/life.git
```

Create a .env file by copying the sample file (modify as needed)
```
cp .env.sample .env
```

Run docker-compose up to start the containers
```
docker-compose up -d
```

Run the migrations
```
docker-compose run web python manage.py migrate
```

Collect static files
```
docker-compose run web python manage.py collectstatic
```

Access the app at http://localhost:8000


## Contributing

We welcome contributions from the community! Here’s how you can contribute:

- Fork this repository and create a new branch for your changes.
- Make your changes in your fork.
- Submit a pull request to this repository with your changes.


# Changelog

## [0.1.0] - 2023-06-23

* First alpha open to public