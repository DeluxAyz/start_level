# Advancing Fast API skills


import secrets # for cryptographically secure random numbers
import string # to in a cool way work with random characters

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, HttpUrl
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
# from start_mock_db import add_to_url_db, url_database, get_url_database
# switched from mock data to actual db
from actual_start_database import SessionLocal, engine, Base, URLStuff
from sqlalchemy.orm import Session 

start_app = FastAPI()
# setting up CORS so FastAPI would allow my Svelte start UI to talk to it
start_app.add_middleware(
    CORSMiddleware,
    allow_origins = [
        "http://localhost:5173", # svelte url
        "http://localhost:5174", # i run multiple svelte projects sometimes
    ],
    allow_credentials = True,
    allow_methods = ["*"], # literally allow all
    allow_headers = ["*"],
)

Base.metadata.create_all(bind=engine)
# telling SQLalchemy to take my db schingo and make some actual db files and tables

class URLCreate(BaseModel):
    target_url: HttpUrl # type hints utilized by Pydantic for 'validation'


# since i'm not using the mock db functions anymore, need new ones
def get_actual_base():
    database = SessionLocal()
    try: 
        yield database # this gives the session to my api endpoint
    finally:
        database.close() # after api endpoint is done, this ensures no db connections are open

@start_app.get("/")
async def root():
    return {"message": "Closing the gap between syntax I learnt before and deep logic I know now"}


@start_app.post("/url")
# async def create_url(url: URLCreate, database: dict = Depends(get_url_database)):
# before I depended on the mock db function, but no more!
async def creat_url(url: URLCreate, database: Session = Depends(get_actual_base)):
    base_chars = string.ascii_letters + string.digits
    # getting characters and stuff from string

    random_chars = ''.join(
        secrets.choice(base_chars) for _ in range(5)
    )
    # random chars using secrets for security
    # join method used to join the random chars
    # range(5) used to generate 5 random chars

    # -  add_to_url_db(random_chars, url.target_url)
    # adding to db with random_chars as key before I then switched to using Depends
    # with the same random_chars as the key
    # - database[random_chars] = str(url.target_url) # converting HttpUrl to string because its a special object
    # since I'm using SQLalchemy now 
    # (here I commented out the old approach for learning, but in other areas I'll just delete it to be clean)
    # first making a URLStuff model instance
    target_url = str(url.target_url) # same string convert tho
    new_url_item = URLStuff(short_key = random_chars, target_url = target_url)
    database.add(new_url_item) # putting it in db
    database.commit() # saving

    return {"your_new_short_url": random_chars, "target_url": url.target_url}

@start_app.get("/{url_key}")
async def redirect_to_target(url_key: str, database: Session = Depends(get_actual_base)):
    database_url = database.query(URLStuff).filter(URLStuff.short_key == url_key).first() # basically a search
    
    # if url_key in database: # if .. in checks if a specific value exists inside a collection
    # something new I used before, no more

    if database_url is None or database_url.target_url is None:
        raise HTTPException(status_code=404, detail="We don't have this URL")

    return RedirectResponse(url=database_url.target_url)

    

