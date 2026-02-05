## Prerequisites
1. **Python 3.12**
2. **Install `uv` package manager**
   - macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
   - Verify: `uv --version`
3. **Install PostgreSQL**
   - Download the installer for your OS from [PostgreSQL Downloads](https://www.postgresql.org/download/)
   - Verify: `psql --version`
4. **pgAdmin 4** (Optional GUI tool)

## Database Setup
Before running the app, create the local database and user.

1. **Open PostgreSQL command line (psql)**
2. **Create a new user:**
```sql
   CREATE USER user_name WITH PASSWORD 'db_password';
```
3. **Create the database:**
```sql
   CREATE DATABASE db_name OWNER user_name;
```
   
   *(Replace `user_name`, `db_password`, and `db_name` with your desired credentials)*

## Application Setup
1. **Install dependencies:** `uv sync`
2. **Configure environment:**
   - Copy `.env.example` to a new `.env` file in the `backend` directory
   - Update `DATABASE_URL` in `.env` with your database credentials:

## Running the Server
1. **Start the server:** `uv run run.py`
2. **Verify it's running:**
   - Home page: `http://127.0.0.1:5000`
   - Database connection test: `http://127.0.0.1:5000/test-db`