from database import engine, Base
import models  # Import models to attach them to Base

if __name__ == "__main__":
    print("Tables before create_all:", Base.metadata.tables.keys())
    Base.metadata.create_all(bind=engine)
    print("Tables after create_all:", Base.metadata.tables.keys())
