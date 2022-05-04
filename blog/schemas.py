from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    content: str


class User(BaseModel):
    name: str
    username: str
    password: str
    email: str
    phone_number: str


class ShowBlog(Blog):
    class Config():
        orm_mode = True


class ShowUser(BaseModel):
    name: str
    username: str
    email: str
    phone_number: str

    class Config():
        orm_mode = True
