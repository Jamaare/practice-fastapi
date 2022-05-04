from turtle import title
from fastapi import Depends, FastAPI, status, Response, HTTPException
#from requests import Response
from . import schemas, models
from .database import *
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/")
def index():
    return("Hello", "world!")


@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create(blog: schemas.Blog, db: Session = Depends(get_db)):
    #new_post = models.Blog(title=blog.title, content=blog.content)
    new_post = models.Blog(**blog.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/blog")
def posts(db: Session = Depends(get_db)):
    all_posts = db.query(models.Blog).all()
    return all_posts


@app.get("/blog/{blog_id}", status_code=200, response_model=schemas.ShowBlog)
def posts(blog_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Blog).filter(models.Blog.id == blog_id).first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{blog_id} does not exist")
    return post


@app.delete("/blog/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Blog).filter(models.Blog.id == post_id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{post_id} does not exist")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/blog/{post_id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(post_id: int, blog: schemas.Blog, db: Session = Depends(get_db)):

    post = db.query(models.Blog).filter(models.Blog.id == post_id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{post_id} does not exist")

    post.update(blog.dict(), synchronize_session=False)
    db.commit()

    return {"data": post.first()}
