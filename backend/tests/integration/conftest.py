import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.database import Base, get_db
from fastapi.testclient import TestClient
from api.main import app
from alembic.config import Config
from alembic import command
import os

# Debug setup for VS Code
DEBUG_MODE = os.getenv("DEBUG_TESTS", "false").lower() == "true"
if DEBUG_MODE:
    import debugpy
    debugpy.listen(("0.0.0.0", 5679))  # Use a different port than your main app
    print("Waiting for debugger to attach...")
    debugpy.wait_for_client()
    print("Debugger attached!")

TEST_DATABASE_URL = "postgresql://testuser:testpass@db_test:5432/testdb"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Run Alembic migrations to set up schema and reference data
    import os
    
    # First, let's clean the database completely
    print("Dropping all existing tables...")
    Base.metadata.drop_all(engine)
    
    # Also drop the alembic_version table if it exists
    from sqlalchemy import text
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS alembic_version"))
        conn.commit()
    
    print("Setting up Alembic configuration...")
    alembic_ini_path = os.path.join(os.path.dirname(__file__), '..', '..', 'alembic.ini')
    alembic_cfg = Config(alembic_ini_path)
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    # Set the script location to absolute path so Alembic can find migrations
    script_location = os.path.join(os.path.dirname(__file__), '..', '..', 'alembic')
    alembic_cfg.set_main_option("script_location", script_location)
    
    print("Running Alembic migrations...")
    command.upgrade(alembic_cfg, "head")
    print("Migrations completed!")
    
    # Debug: Check what tables were created
    with engine.connect() as conn:
        result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
        tables = [row[0] for row in result]
        print(f"Tables after migration: {tables}")
    
    yield
    
    # Clean up by dropping all tables
    Base.metadata.drop_all(engine)

@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
