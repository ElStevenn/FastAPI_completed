from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


SQLALCHEMY_DATABASE_URL = "postgresql://Admin_P:12345@localhost:5432/myFirstDatabase"
# Connection postgresql://<user>:<password>@<host>:<port>/<database_name>
# Port: 5432


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all(bind=engine)
def test_connection():
    try:
        # Try to create a session and query the database
        session = SessionLocal()
        session.execute('SELECT 1')
        session.close()
        print("Connection successful!")
    except OperationalError:
        print("Connection failed! Please check your connection string and database status.")