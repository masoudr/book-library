# Book Library Sample Project

A Django based Book Library project.
This project is a sample app that can be used for other projects.

## Features

* Use a fully custom user model instead of the default Django User model
* Setting up the project with Docker
* MySQL as Django Database model
* Send Last N Book to each Author Email with Celery periodic task
* Using Mongo for logging celery tasks
* Using ElasticSearch to search for book names and authors
* Lots of unit tests

## Usage

* To start project, run:

    ```shell
    cd <project_dir>
    docker-compose build
    docker-compose up
    ```

    The API will be available at [http://127.0.0.1:8000/api](http://127.0.0.1:8000/api)

* To search for a book or author with ES:

    ```shell
    curl -X GET http://localhost:8000/api/books/?search=SomeBook
    ```

* Sent mails can be viewed in Django mail file engine:

  ```shell
  <project_dir>/log/app-messages
  ```

* Celery periodic task can be set in '<project_dir>/app/core/tasks.py`:

  ```python
  @periodic_task(run_every=(crontab(hour=17, minute=0, day_of_week=1)), name="send_mail_to_authors", ignore_result=True)
  def send_mail_to_authors():
      pass
  ```

## Test

To test project, run:

```shell
docker-compose.exe run --rm app bash -c "python manage.py test"
```

## Credits

* Masoud Rahimi: [masoudrahimi.com](http://masoudrahimi.com)
