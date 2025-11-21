from database import Base, engine
import models

# Drop all tables
Base.metadata.drop_all(bind=engine)

# Recreate tables with new columns
Base.metadata.create_all(bind=engine)
