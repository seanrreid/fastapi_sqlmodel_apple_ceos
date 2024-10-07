import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from db import get_session
from models.ceos import Ceo

app = FastAPI()

# Setup our origins...
# ...for now it's just our local environments
origins = [
    "http://localhost",
    "http://localhost:3000",
]

# Add the CORS middleware...
# ...this will pass the proper CORS headers
# https://fastapi.tiangolo.com/tutorial/middleware/
# https://fastapi.tiangolo.com/tutorial/cors/
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

# Create


@app.post("/create")
async def create_ceo(name: str, slug: str, year: int, session: Session = Depends(get_session)):
    ceo = Ceo(name=name, slug=slug, year=year)
    session.add(ceo)
    session.commit()
    return {"CEO added": ceo.name}

# Read


@app.get('/ceos')
# Add Session dependency from db file
def list_ceos(session: Session = Depends(get_session)):
    statement = select(Ceo)
    results = session.exec(statement)
    return results.all()


@app.get('/ceos/{slug}')
def get_ceos(slug: str, session: Session = Depends(get_session)):
    statement = select(Ceo).where(Ceo.slug == slug)
    # This will return any value that is "like" the slug
    results = session.exec(statement)
    return results.one()

# Update


@app.put('/ceos/{id}/update')
async def update_ceo(id: int, name: str = None, slug: str = None, year: int = None, session: Session = Depends(get_session)):
    statement = select(Ceo).where(Ceo.id == id)
    results = session.exec(statement)
    ceo = results.one()
    if ceo is not None:
        if name:
            ceo.name = name
        if slug:
            ceo.slug = slug
        if year:
            ceo.year = year
        session.add(ceo)
        session.commit()
        return {"Updated CEO": ceo.name}
    else:
        return {"message": "User ID not found"}


# Delete
@app.delete('/ceos/{id}/delete')
async def remove_ceo(id: int, session: Session = Depends(get_session)):
    ceo = session.query(Ceo).filter(Ceo.id == id).first()
    if ceo is not None:
        session.delete(ceo)
        session.commit()
        return {"Deleted CEO": ceo.name}
    else:
        return {"message": "User ID not found"}


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
