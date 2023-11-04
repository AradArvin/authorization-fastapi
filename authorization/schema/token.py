from pydantic import BaseModel, Field, EmailStr



class User(BaseModel):
    _id: str
    username: str | None=None
    fullname: str | None=None
    email: EmailStr = Field()
    password: str = Field()

    class Config:
        populate_by_name = True


