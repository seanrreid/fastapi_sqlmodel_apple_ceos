import uvicorn
from fastapi import FastAPI
from sqlmodel import Session, select, join, literal_column, func
from db import engine
from models.ceos import Ceo

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/ceos')
def list_ceos():
    with Session(engine) as session:
        statement = select(Ceo)
        results = session.exec(statement).all()
    return results


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
