from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

app = FastAPI()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

Base.metadata.create_all(bind=engine)

class ItemCreate(BaseModel):
    name: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Carbon Storage Site Mapping Tool API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/items")
def read_items():
    db = SessionLocal()
    items = db.query(Item).all()
    return {"items": [{"id": item.id, "name": item.name} for item in items]}

@app.post("/items")
def create_item(item: ItemCreate):
    db = SessionLocal()
    db_item = Item(name=item.name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"id": db_item.id, "name": db_item.name}

@app.get("/database-test")
def test_database():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        return {"message": "Database connection successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)