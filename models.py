
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional

# country models

class CountryBase(SQLModel):
    country_name : str = Field(unique = True )

class Country(CountryBase , table = True):
    id : Optional[int] = Field(default = None , primary_key = True)
    country_users: list["User"] = Relationship(back_populates="country")
    

class CountryCreate(CountryBase):
    pass

class CountryRead(CountryBase):
    id : int

class CountryUpdate(SQLModel):
    name : Optional[str]




# user models

class UserBase(SQLModel):
    name : str
    email : str = Field(unique = True)
    password : str
    country_name : str = Field(foreign_key="country.country_name")

class User(UserBase , table = True):
    id : Optional[int] = Field(default = None , primary_key = True)
    country: Optional["Country"] = Relationship(back_populates="country_users")
    

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id : int


class UserUpdate(UserBase):
   pass
