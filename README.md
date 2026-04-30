# Japanese Vocabulary Learning API

A backend-focused API built with FastAPI for managing Japanese vocabulary learning.
The system is designed to handle user authentication, external API integration, and per-user learning progress.

---

## Motivation

I wanted to build a backend system that goes beyond basic CRUD operations and reflects a more realistic use case.

This project is based on a vocabulary learning workflow, where users can save words and track their progress by categorizing them as "learning" or "known".

The focus was on designing the backend architecture — handling authentication, user-specific data, and state transitions — rather than building a frontend interface.


## Features

* JWT-based user authentication
* Search Japanese words using Jisho API
* Save words to a personal learning list
* Track progress (learning → known)
* User-specific data isolation

---

## Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy ORM
* JWT Authentication
* External API: Jisho

---

## System Design Overview

* Users authenticate via JWT tokens
* Protected routes use dependency injection (`get_current_user`)
* Words are stored per user with ownership enforced at query level
* External data is fetched from Jisho API and normalized before storage
* Learning state is tracked using a status field (`learning`, `known`)

---

## API Usage

### Live API

https://japanese-vocab-api.onrender.com/docs

### Authentication Flow

1. Register a user
2. Login to receive access token
3. Click **Authorize** in `/docs`
4. Enter:

   ```
   <your_token>
   ```
5. Access protected endpoints

---

## Example Endpoints

* `POST /register` — create user
* `POST /login` — get JWT token
* `GET /search?word=...` — search vocabulary
* `POST /add` — add word to learning list
* `GET /learning` — retrieve learning words
* `PUT /mark-known` — update word status
* `GET /known` — retrieve known words
* `DELETE /delete` — remove word

---

## Design Decisions

* Used JWT for stateless authentication
* Chose FastAPI for automatic docs and dependency injection
* Separated learning and known states for extensibility
* Integrated external API instead of static dataset for real-world data handling

---

## Future Improvements

* Add frontend for daily usability
* Implement spaced repetition system (SRS)
* Add caching for external API calls
* Improve error handling and retries

---

## Notes

* This project focuses on backend system design and API architecture
* All functionality can be tested via FastAPI's interactive `/docs` interface
