import sqlite3
from fastapi import FastAPI

app = FastAPI()


@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect('chinook.db')


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()


@app.get("/tracks")
async def get_tracks(page: int = 0, per_page: int = 10):
    cursor = app.db_connection.cursor()
    tracks = cursor.execute("SELECT trackid, name, albumid, mediatypeid, genreid, composer, milliseconds, "
        "bytes, unitprice FROM tracks ORDER BY trackid LIMIT ? OFFSET ?;",
        (per_page, page * per_page),
    ).fetchall()
    return tracks



#SELECT * from tracks LIMIT 10 OFFSET 10