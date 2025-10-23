# Phonebook Contacts API

A small, educational `Django REST Framework` API for managing contacts with secure validation, JWT auth, and structured logging.

## Features

- Create, list, and delete contacts
- Strict input validation for names and phone numbers
- JWT-based authentication (SimpleJWT)
- Group-based permissions (reader, writer)
- Signup endpoint (issues access token)
- Structured logging (console + JSON file)
- CI via GitHub Actions

## Tech Stack

- Python

- Django

- Django REST Framework

- djangorestframework-simplejwt

- structlog

- colorama

- pytest

- pytest-django

## Requirements

- Python `3.12`+
- `pip` / `virtualenv`
- macOS/Linux recommended (can also use WSL for windows users)

## Environment Variables

After you've cloned the project, you're going to need to set your `.env` variables. I've provided the list of the variable names below. You are able to generate a random secret key by using the Django sell.

- `SECRET`: Django secret key
- `DEBUG`: 0 or 1
- `LOG_LEVEL`: INFO, WARNING, etc.
- `ALLOWED_HOSTS`: e.g. testserver,localhost,127.0.0.1

## Setup

- Clone and create a virtual environment:

  - `git clone https://github.com/kn1ghtm0nster/phone-book-api.git`
  - `cd phone-book-api`
  - `python -m venv .venv`
  - `source .venv/bin/activate`

- Install dependencies:

  - `pip install -r requirements.txt`

- Migrate:

  - `python manage.py migrate`

- Run:

  - `python manage.py runserver`

## Testing & CI

- Run: `pytest -q`

  - **NOTE:** Tests disable file logging and use in-memory DB

- `GitHub Actions` runs pytest on PRs and `main` pushes

## Project Structure

- `config/`: Django project settings and URLs
- `phonebook/api/`: DRF views, serializers, utilities
- `phonebook/services/`: business logic services
- `tests/`: unit and API tests

## Authentication & Authorization

- Signup: POST /auth/signup/ → returns `access_token`
- JWT:
  - POST /auth/token/
  - POST /auth/token/refresh/
- Groups:
  - reader: can GET list
  - writer: can create/delete

## API Endpoints (Quickstart)

- `GET` /phone-book/list/ → list contacts
- `POST` /phone-book/add/ → create contact
  - `body`: `{"name":"Alice Smith","phone_number":"(123) 456-7890"}`
- `DELETE` /phone-book/delete/?name=Alice%20Smith
- `DELETE` /phone-book/delete/?phone_number=(123)%20456-7890

Protected routes require Authorization: `Bearer <access_token>`.

## A Note to Visitors

This project was built for **educational purposes only**. All credit for the project requirements belongs to Professor Thomas Jones at the University of Texas at Arlington.

This is a minimal `RESTful` API and **not production-ready**. It can be _extended_ (e.g., UI, more CRUD endpoints like contact details, addresses, work numbers). I used a Domain-Driven Design style to practice that pattern; **not all codebases follow it**.

In addition, I did deviate from the original specs to implement correct `HTTP` methods that would be seen in `CRUD` applications such as sending `DELETE` requests instead of `PUT`. While it _is_ the correct method to use, enterprise applications (large organizations) tend to use `PUT` so that the record isn't _actually_ deleted but instead is "labeled" as deleted.

The database for this project is held in `SQLite` as it comes supported by Django as the default database. SQLite is used for simplicity. In _most_ production systems, you’d use `PostgreSQL` or `SQL Server` and likely implement **soft-deletes (server marks a record as deleted)** even if clients make HTTP `DELETE` requests.
