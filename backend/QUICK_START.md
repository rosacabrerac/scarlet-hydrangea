# Week 1 Backend Skeleton - Quick Reference

## What's Built (Week 1)

✅ App factory pattern  
✅ Environment-based configuration  
✅ Flask-SQLAlchemy with PostgreSQL  
✅ Flask-Migrate (database versioning)  
✅ Flask-JWT-Extended (auth ready)  
✅ Health check endpoint  
✅ Clean folder structure  

## How to Start Working

### First Time Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .
cp .env.example .env
# Edit .env with your database credentials
python create_db.py
flask db init
python run.py
```

### Running the App
```bash
python run.py
# Visit http://localhost:5000/health
```

### Adding a New Feature (Week 2+)

1. **Create model** in `app/models/your_model.py`
2. **Create CRUD** in `app/crud/your_crud.py`
3. **Create routes** in `app/api/your_routes.py`
4. **Register blueprint** in `src/__init__.py`
5. **Create migration:** `flask db migrate -m "Add your feature"`
6. **Apply migration:** `flask db upgrade`

## Important Files

| File | Purpose |
|------|---------|
| `src/__init__.py` | App factory |
| `src/config.py` | Configuration classes |
| `src/extensions.py` | DB, Migrate, JWT setup |
| `app/api/health.py` | Example blueprint |
| `.env` | Your credentials (git-ignored) |
| `migrations/` | Database version control |

## Common Commands

```bash
# Run app
python run.py

# Check health
curl http://localhost:5000/health

# Database migrations
flask db migrate -m "description"
flask db upgrade
flask db downgrade  # Rollback

# Run tests (Week 2)
pytest

# Activate venv (Windows)
venv\Scripts\activate

# Activate venv (Mac/Linux)
source venv/bin/activate
```

## Architecture Rules

1. **Business logic in CRUD, not routes**
   - Routes: Handle HTTP only
   - CRUD: Handle database logic
   - Models: Define data structure

2. **Import extensions from `src.extensions`**
   - `from src.extensions import db`
   - Never create your own SQLAlchemy instance

3. **Use blueprints for routes**
   - Don't write routes in `src/__init__.py`
   - Put them in `app/api/your_feature.py`

4. **Config from environment**
   - Credentials in `.env`
   - Never hardcode secrets

5. **Migrations for schema changes**
   - Always run `flask db migrate` after model changes
   - Commit migration files to Git

## Troubleshooting

**App won't start?**
```bash
# Check Python path
which python  # or: where python (Windows)

# Check imports
python -c "from src import create_app"
```

**Database connection fails?**
```bash
# Verify .env has correct DATABASE_URL
cat .env

# Check PostgreSQL is running
psql -U postgres  # Should connect
```

**Migrations confusing?**
```bash
# See migration status
flask db history
flask db current

# See what changed
git diff migrations/versions/
```

## Next Week (Week 2)

- Build `User` model
- Build `Book` model
- Build `Borrow` model
- Add CRUD operations
- Create API endpoints
- Add input validation

---

**Questions?** Check `ARCHITECTURE.md` or ask in PRs. We're building this together! 🚀
