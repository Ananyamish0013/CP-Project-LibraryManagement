# Library Management System

A simple, modern, and complete mini-project built with Python (Flask) for the backend and Vanilla HTML/CSS/JS for the frontend.

## Features
- **Book Catalog**: Add, view, search, and delete books.
- **Transactions**: Issue and return books.
- **User Management**: Add mock users to interact with.
- **Premium UI**: Modern styling inspired by top-tier SaaS applications.

## Project Structure
- `backend/`: Contains the Flask REST API, database (`SQLite`), and python dependencies.
- `frontend/`: Contains all client-side files (HTML, CSS, JavaScript). Completely decoupled from the backend.

## How to Run Locally

### 1. Start the Backend API

1. Open a terminal and navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. (Optional but recommended) Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask Server:
   ```bash
   python app.py
   ```
   *The server will start on `http://127.0.0.1:5000`. The SQLite `library.db` will be auto-generated inside `backend/instance/`.*

### 2. Open the Frontend

1. Simply open the `frontend/index.html` file in your preferred web browser. 
2. You can either double-click on the file or right-click and choose "Open with -> Google Chrome / Edge / Firefox". 
   - *(Because we used `flask-CORS` in the backend, the static HTML files can successfully communicate with the remote API)*
