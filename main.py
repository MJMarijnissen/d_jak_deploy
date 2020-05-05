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

class NewAlbum(BaseModel):
    title: str
    artist_id: int

class Album(BaseModel):
    AlbumId: int
    Title: str
    ArtistId: int

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

@app.post("/albums", status_code=status.HTTP_201_CREATED, response_model=Album)
async def new_album(album: NewAlbum, db: sqlite3.Connection = Depends(get_db)):
    artist = db.execute(
        "SELECT name FROM artists WHERE artistid = ?;", (album.artist_id,)
    ).fetchone()
    if not artist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"error": f"No artist with this Id: {album.artist_id}"}},
        )
    cursor = db.execute(
        "INSERT INTO albums (title, artistid) VALUES (?, ?);",
        (album.title, album.artist_id),
    )
    db.commit()
    album = db.execute(
        "SELECT albumid, title, artistid FROM albums WHERE albumid = ?;",
        (cursor.lastrowid,),
    ).fetchone()
    return album


@app.get("/albums/{album_id}", response_model=Album)
async def gat_album_by_id(album_id: int, db: sqlite3.Connection = Depends(get_db)):
    album = db.execute(
        "SELECT albumid, title, artistid FROM albums WHERE albumid = ?;", (album_id,),
    ).fetchone()
    if not album:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"error": f"No album with this Id: {album_id}"}},
        )
    return album