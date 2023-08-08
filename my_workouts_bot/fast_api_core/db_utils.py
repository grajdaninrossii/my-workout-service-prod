from models import async_session

# Dependency
async def get_db():
    db = async_session()
    try:
        yield db
    finally:
        db.close()