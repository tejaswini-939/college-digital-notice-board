# College Digital Notice Board

A small notice board built with Python Flask, HTML templates, CSS, and Bootstrap. Students can sign up, log in, view notices, search by title, and log out. Sample notices and demo accounts are held in Python lists and dictionaries, so there is no database or external API.

## Run on Windows

1. Install Python 3.10 or newer from [python.org](https://www.python.org/downloads/). During installation, select **Add Python to PATH**.
2. Open Command Prompt or PowerShell and change to this project folder:

   ```powershell
   cd path\to\college-notice-board
   ```

3. (Recommended) Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .venv\Scripts\activate
   ```

4. Install the Python packages:

   ```powershell
   py -m pip install -r requirements.txt
   ```

5. Create a temporary secret for signing the Flask session cookie. Keep this command in the same PowerShell window where you will run the app:

   ```powershell
   $env:SESSION_SECRET = (py -c "import secrets; print(secrets.token_hex(32))")
   ```

   Replit already provides a secret named `SESSION_SECRET`. For a real deployment, set a private, persistent secret in the hosting environment instead of generating one on each start.

6. Start the application:

   ```powershell
   py app.py
   ```

7. Open <http://127.0.0.1:5000> in your browser. Press `Ctrl+C` in the terminal to stop the server.

## Test the student account flow

1. Open `/signup`, enter a name, email, and matching password (at least 8 characters). Submit the form; the app redirects you to `/login`.
2. Try signing up again with the same email or with mismatched passwords to see the validation messages.
3. Log in using the account you created. The notice board opens and shows your signed-in name.
4. Search for a notice title, then use **Log out**.
5. Visit `/` after logging out. The app redirects you to `/login` until you sign in again.

Accounts are stored only in memory. They disappear when Flask restarts and are not shared by multiple application workers or containers. This is for a classroom demonstration, not production authentication.

## Run with Docker Desktop

From this folder, build the image and create a temporary local secret:

```powershell
docker build -t college-notice-board .
$sessionSecret = py -c "import secrets; print(secrets.token_hex(32))"
docker run --rm -p 5000:5000 --env "SESSION_SECRET=$sessionSecret" college-notice-board
```

Open <http://localhost:5000>. The container listens on port `5000` and runs Flask with Gunicorn, which is suitable for a Docker-based deployment.

## Files in this project

- `app.py` — Flask routes, sample notices, in-memory student accounts, password hashing, login sessions, validation, and title search.
- `templates/login.html` — student login form.
- `templates/signup.html` — student registration form.
- `templates/index.html` — protected notice board page.
- `templates/_flash_messages.html` — reusable success and error messages.
- `static/css/style.css` — custom colours, card styling, responsive layout, and account form styles.
- `static/css/bootstrap.min.css` — the Bootstrap stylesheet, saved locally so the page does not depend on a CDN.
- `static/favicon.svg` — the small icon shown in the browser tab.
- `requirements.txt` — Flask for the app and Gunicorn for Linux containers; Gunicorn is skipped on Windows.
- `Dockerfile` — instructions for building a Docker image and running the app in a container.
- `.dockerignore` — excludes local development files from the Docker build context.
- `.gitignore` — keeps Python cache files, virtual environments, and local environment files out of Git.
- `README.md` — setup, run, Docker, and file-purpose instructions.

## Edit the sample notices

Open `app.py` and edit the dictionaries in the `NOTICES` list. Each notice has `title`, `description`, `category`, and `date` fields. Keep the category names as `Examinations`, `Placements`, `Events`, or `General` to use the matching badge colour. Demo users are stored separately in the `USERS` dictionary and are cleared whenever the process restarts.
