# Prediction

Prediction plant diseases

## Specifications

* Use python versions `3.11`
* Use django `5.0.6`
* Use poetry as dependency management

## Install and run project

* Install poetry through [this](https://python-poetry.org/docs/) documentation
* Execute command `make install` to install all dependency package
* Execute command `make migrations` to create new migration in case any changes in project
* Execute command `make migrate` to create new database using sqlite and migrate all tables in database
* Execute command `make run` to run the project
* Execute command `make create-user` to create new superuser

## Documentation

* Swagger documentation is defined [here](http://localhost:8000/swagger)
* Redoc documentation is defined [here](http://localhost:8000/redoc)

## Api that available

* Users API, this provide all CRUD for users
* Prediction API, this provide prediction data to specified images
* Auth API, this provide to create token and refresh the token
* Oauth Api by using google, just pass the token that send from front end
  * To see how it works you can see in [here](https://developers.google.com/identity/gsi/web/guides/verify-google-id-token)
* In each Module API, users and prediction there's a history for interaction

