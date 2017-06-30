# lurl

> A small url shortener API written with django-rest-framework using Postgres as a backend.


## Quick Run Requirements

You must have docker installed. This has only been tested 17.06.0-ce-mac18 (18433) on OS X.

## Running

In the repo root run

    docker-compose up

After everything has come up completely you'll need to run the migrations. You'll know it's ready when you see the following log:

    db_1      | PostgreSQL init process complete; ready for start up.

Once you see this log, run this in a different terminal in the repo root:

    docker-compose exec django python manage.py migrate
