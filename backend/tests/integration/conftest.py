import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.database import Base, get_db
from fastapi.testclient import TestClient
from api.main import app
from alembic.config import Config
from alembic import command
import os

# Optional debug setup for VS Code - only activates when DEBUG_TESTS=true
DEBUG_MODE = os.getenv("DEBUG_TESTS", "false").lower() == "true"
if DEBUG_MODE:
    import debugpy
    debugpy.listen(("0.0.0.0", 5679))
    print("Waiting for debugger to attach...")
    debugpy.wait_for_client()
    print("Debugger attached!")

TEST_DATABASE_URL = "postgresql://testuser:testpass@db_test:5432/testdb"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Clean the database completely before running migrations
    Base.metadata.drop_all(engine)
    
    # Also drop the alembic_version table if it exists to force fresh migrations
    from sqlalchemy import text
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS alembic_version"))
        conn.commit()
    
    # Run Alembic migrations to set up schema
    alembic_ini_path = os.path.join(os.path.dirname(__file__), '..', '..', 'alembic.ini')
    alembic_cfg = Config(alembic_ini_path)
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    # Set the script location to absolute path so Alembic can find migrations
    script_location = os.path.join(os.path.dirname(__file__), '..', '..', 'alembic')
    alembic_cfg.set_main_option("script_location", script_location)
    command.upgrade(alembic_cfg, "head")
    
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
