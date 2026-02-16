# Architecture Guide

This document explains the backend skeleton design and how to extend it.

## Core Concepts

### 1. App Factory

**Location:** `src/__init__.py`

```python
def create_app(config=None):
    """Create and configure Flask app"""
    app = Flask(__name__)
    app.config.from_object(get_config())
    init_extensions(app)
    # Register blueprints
    return app
```

**Benefits:**
- Multiple app instances for testing/staging/production
- No global state
- Easy to pass configs

### 2. Extensions (Third-Party Setup)

**Location:** `src/extensions.py`

```python
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def init_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
```

**Why separate?**
- Models import `from src.extensions import db` without needing the app
- Prevents circular imports: `models → extensions` (not `models → app → extensions`)
- Extensions are initialized once per app

### 3. Configuration Management

**Location:** `src/config.py`

```python
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Fast, isolated
```

**Pattern:**
1. Base `Config` class with shared settings
2. Environment-specific classes override as needed
3. `get_config()` returns the right class based on `FLASK_ENV`

### 4. Blueprints (Organized Routes)

**Location:** `app/api/health.py`

```python
health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    # Route logic here
    return jsonify({'status': 'healthy'})
```

**Registered in:** `src/__init__.py`
```python
from app.api import health_bp
app.register_blueprint(health_bp)
```

**Week 2 will add:**
```python
from app.api import health_bp, borrowing_bp, users_bp
app.register_blueprint(health_bp)
app.register_blueprint(borrowing_bp, url_prefix='/api/borrowing')
app.register_blueprint(users_bp, url_prefix='/api/users')
```

---

## How to Add a New Feature

### Example: Adding a User endpoint (Week 2)

**Step 1: Create the model**
```python
# app/models/__init__.py
from app.models.user import User

# app/models/user.py
from src.extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

**Step 2: Create CRUD operations**
```python
# app/crud/user_crud.py
from src.extensions import db
from app.models import User

def create_user(email):
    user = User(email=email)
    db.session.add(user)
    db.session.commit()
    return user

def get_user(user_id):
    return User.query.get(user_id)
```

**Step 3: Create routes**
```python
# app/api/users.py
from flask import Blueprint, jsonify, request
from app.crud import create_user, get_user

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['POST'])
def create_user_endpoint():
    data = request.get_json()
    user = create_user(data['email'])
    return jsonify({'id': user.id, 'email': user.email}), 201

@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user_endpoint(user_id):
    user = get_user(user_id)
    if not user:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'id': user.id, 'email': user.email}), 200
```

**Step 4: Register blueprint**
```python
# In src/__init__.py
from app.api import users_bp
app.register_blueprint(users_bp, url_prefix='/api')
```

**Step 5: Create migration**
```bash
flask db migrate -m "Add User model"
flask db upgrade
```

---

## Separation of Concerns

```
Routes (app/api/*.py)
    ↓ (call)
CRUD Operations (app/crud/*.py)
    ↓ (use)
Models (app/models/*.py)
    ↓ (query/insert)
Database (PostgreSQL via SQLAlchemy)
```

**Example:**
```python
# Routes handle HTTP
@users_bp.route('/users/<int:user_id>')
def get_user(user_id):
    user = get_user(user_id)  # Call CRUD
    return jsonify(user.to_dict()), 200

# CRUD handles database logic
def get_user(user_id):
    return User.query.get(user_id)  # Query model

# Models define structure
class User(db.Model):
    id = db.Column(...)
    email = db.Column(...)
```

---

## Database Migrations

Flask-Migrate tracks schema changes in Git.

**Workflow:**
1. Add/modify models in `app/models/`
2. Run: `flask db migrate -m "descriptive message"`
3. This creates a file in `migrations/versions/`
4. Run: `flask db upgrade` to apply
5. Commit both the model and migration file

**Example migration file:**
```python
# migrations/versions/001_initial.py
def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(120), nullable=False),
    )

def downgrade():
    op.drop_table('user')
```

**Why?** Team members clone repo and run `flask db upgrade` instead of manual SQL.

---

## Testing (Week 2+)

Tests use in-memory SQLite (fast, isolated):

```python
# tests/test_users.py
import pytest
from src import create_app
from src.config import TestingConfig

@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        from src.extensions import db
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_create_user(app):
    client = app.test_client()
    response = client.post('/api/users', json={'email': 'test@example.com'})
    assert response.status_code == 201
```

---

## Common Patterns

### Import Models Safely
```python
# ✅ Good: Happens at route time (deferred)
def get_user_endpoint():
    from app.models import User
    return User.query.all()

# ❌ Bad: Circular import risk at module load time
from app.models import User  # top of file
```

### Use `db` from Extensions
```python
# ✅ Good
from src.extensions import db

class User(db.Model):
    pass

def query():
    db.session.query(User).all()

# ❌ Bad
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()  # New instance, not the app's instance
```

### Environment-Based Behavior
```python
# ✅ Good
if app.config['TESTING']:
    # Use in-memory database
else:
    # Use PostgreSQL
```

---

## Questions?

This skeleton is intentionally minimal. As you build features:
- Models, CRUD, and routes grow
- Testing and validation layers added
- Error handling middleware
- Auth/permissions (Week 3+)

Start simple, add complexity as needed. 🚀
