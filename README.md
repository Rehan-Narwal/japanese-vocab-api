# Japanese Vocabulary Learning API

This is a FastAPI project I built to save Japanese words and keep track of which ones I'm still learning and which ones I already know.

It uses the Jisho API to look up words, and stores each user's vocabulary in a PostgreSQL database.

## What it does

- Register and log in with an email and password
- Search for Japanese words using Jisho
- Save words to a personal learning list
- Mark saved words as known
- View or delete saved words

## Built with

- Python and FastAPI
- PostgreSQL and SQLAlchemy
- JWT for authentication
- Jisho API for word searches

## API

The deployed API and interactive documentation are available here:

https://japanese-vocab-api.onrender.com/docs

Main endpoints:

| Method | Endpoint | Description |
|---|---|---|
| POST | `/register` | Create an account |
| POST | `/login` | Log in and get an access token |
| GET | `/search?word=...` | Search Jisho |
| POST | `/add?word=...` | Save a word |
| GET | `/learning` | Get words in the learning list |
| PUT | `/mark-known?id=...` | Mark a word as known |
| GET | `/known` | Get known words |
| DELETE | `/delete?id=...` | Delete a saved word |

The `/add`, `/learning`, `/mark-known`, `/known`, and `/delete` endpoints require a bearer token. The search endpoint is public.

## Run locally

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project folder with your PostgreSQL connection string and a secret key:

```env
DATABASE_URL=your_postgresql_connection_string
SECRET_KEY=your_secret_key
```

5. Start the server:

```bash
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` to test the endpoints.

## Things I might add later

- A simple frontend
- Spaced repetition for reviewing words
- Caching for Jisho searches
- Better handling of external API errors
