import sqlite3
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from starlette import status


app = FastAPI()


class Track(BaseModel):
    TrackId: int
    Name: str
    AlbumId: Optional[int]
    MediaTypeId: int
    GenreId: Optional[int]
    Composer: Optional[str]
    Milliseconds: int
    Bytes: Optional[int]
    UnitPrice: float

@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect('chinook.db')


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()


async def get_db():
    factory = app.db_connection.row_factory
    app.db_connection.row_factory = sqlite3.Row
    try:
        yield app.db_connection
    finally:
        app.db_connection.row_factory = factory


@app.get("/tracks", response_model=List[Track])
async def get_tracks(page: int = 0, per_page: int = 10, db: sqlite3.Connection = Depends(get_db)):
    cursor = app.db_connection.cursor()
    tracks = cursor.execute( "SELECT trackid, name, albumid, mediatypeid, genreid, composer, milliseconds, "
        "bytes, unitprice FROM tracks ORDER BY trackid LIMIT ? OFFSET ?;",
        (per_page, page * per_page),
    ).fetchall()
    return tracks


@app.get("/tracks/composers/", response_model=List[str],)
async def composers_tracks(composer_name: str, db: sqlite3.Connection = Depends(get_db)):
    db.row_factory = lambda c, x: x[0]
    data = db.execute(
        "SELECT name FROM tracks WHERE composer = ? ORDER BY name;", (composer_name,)
    ).fetchall()
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": f"Composer: {composer_name} not found"},
        )
    else:
        return data