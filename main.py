from fastapi import FastAPI , Depends , HTTPException, Query
from typing import Annotated
from sqlmodel import Session , select
from db import  get_db , create_db_and_tables
from models import *


app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"Hello": "World"}


# get all the users

@app.get("/users" , response_model=list[User])
def get_users(session : Annotated[Session, Depends(get_db)], offset : int = Query(default=0 , le= 4), limit : int = Query(default=2 , le=4)):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users

# create new user

@app.post("/create-users" , response_model=UserRead)
def create_user(user : UserCreate , session : Annotated[Session, Depends(get_db)]):
    user_to_insert = User.model_validate(user)
    session.add(user_to_insert)
    session.commit()
    session.refresh(user_to_insert)
    return user_to_insert

# get user by id
@app.get("/users/{user_id}" , response_model=UserRead)
def get_user_by_id(user_id : int , session : Annotated[Session, Depends(get_db)]):
    user = session.get(User , user_id)
    if not user:
        raise HTTPException(status_code=404 , detail="User not found")
    return user

# update user

@app.put("/users/{user_id}")
def update_user(user_id : int , user : UserUpdate , session : Annotated[Session, Depends(get_db)]):
    user_to_update = session.get(User , user_id)
    if not user_to_update:
        raise HTTPException(status_code=404 , detail="User not found")
    user_to_update.name = user.name
    user_to_update.email = user.email
    session.add(user_to_update)
    session.commit()
    session.refresh(user_to_update)
    return user_to_update

# delete user

@app.delete("/users/{user_id}")
def delete_user(user_id : int , session : Annotated[Session, Depends(get_db)]):
    user_to_delete = session.get(User , user_id)
    if not user_to_delete:
        raise HTTPException(status_code=404 , detail="User not found")
    session.delete(user_to_delete)
    session.commit()
    return {"message" : "User deleted"}

# get all the countries

@app.get("/countries" , response_model=list[Country])
def get_countries(session : Annotated[Session, Depends(get_db)], offset : int = Query(default=0 , le= 4), limit : int = Query(default=2 , le=4)):
    countries = session.exec(select(Country).offset(offset).limit(limit)).all()
    return countries

# create new country

@app.post("/countries/" , response_model=CountryRead)
def create_country(country : CountryCreate , session : Annotated[Session, Depends(get_db)]):
    country_to_insert = Country.model_validate(country)
    session.add(country_to_insert)
    session.commit()
    session.refresh(country_to_insert)
    return country_to_insert

# get country by id

@app.get("/countries/{country_id}" , response_model=CountryRead)
def get_country_by_id(country_id : int , session : Annotated[Session, Depends(get_db)]):
    country = session.get(Country , country_id)
    if not country:
        raise HTTPException(status_code=404 , detail="Country not found")
    return country

# update country

@app.put("/countries/{country_id}")
def update_country(country_id : int , country : CountryUpdate , session : Annotated[Session, Depends(get_db)]):
    country_to_update = session.get(Country , country_id)
    if not country_to_update:
        raise HTTPException(status_code=404 , detail="Country not found")
    country_to_update.country_name = country.name
    session.add(country_to_update)
    session.commit()
    session.refresh(country_to_update)
    return country_to_update

# delete country

@app.delete("/countries/{country_id}")
def delete_country(country_id : int , session : Annotated[Session, Depends(get_db)]):
    country_to_delete = session.get(Country , country_id)
    if not country_to_delete:
        raise HTTPException(status_code=404 , detail="Country not found")
    session.delete(country_to_delete)
    session.commit()
    return {"message" : "Country deleted"}
    

