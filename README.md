# Mini Notes 📝

A simple sticky-notes web app built with Python, SQLite, HTML, CSS, and JavaScript.

Create, view, and delete notes through a colourful, sticky-note-style interface. The backend uses Python's built-in libraries, so no third-party Python packages are required.

## Features

- Create notes with a title and body
- View saved notes in a colourful sticky-note layout
- Delete notes
- Store notes in a local SQLite database
- Responsive frontend for desktop and mobile
- Lightweight backend using Python's standard library

## Tech Stack

- **Backend:** Python
- **Web server:** `http.server`
- **Database:** SQLite (`sqlite3`)
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** AWS Elastic Beanstalk

## Project Structure

```text
mini-notes/
├── README.md
├── Procfile
├── server.py
├── db.py
├── pyproject.toml
├── notes.db          # Created automatically if missing
└── web/
    ├── index.html
    ├── style.css
    └── app.js
```

## Requirements

- Python 3.12 or a compatible Python version
- [uv](https://docs.astral.sh/uv/) (optional, for local development)

No `requirements.txt` is needed because the application uses Python's standard library.

## Run Locally

1. Clone the repository or open the project directory.

2. Initialise the database:

   ```bash
   uv run python db.py
   ```

3. Start the server:

   ```bash
   uv run python server.py
   ```

4. Open the application in your browser:

   [http://127.0.0.1:8000](http://127.0.0.1:8000)

Press `Ctrl+C` in the terminal to stop the server.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/notes` | List all notes |
| POST | `/api/notes` | Create a note |
| DELETE | `/api/notes/{id}` | Delete a note |

### Example: Create a Note

```bash
curl -X POST http://127.0.0.1:8000/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"My first note","body":"Hello from Mini Notes!"}'
```

## Deploy to AWS Elastic Beanstalk

1. Ensure the `Procfile` is in the project root.
2. Confirm it contains:

   ```text
   web: python server.py
   ```

3. Ensure the server listens on `0.0.0.0` and uses the configured
