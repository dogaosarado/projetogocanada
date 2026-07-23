from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db, get_admin_user
from app.models.content import Post
from app.models.user import User
from app.schemas.content import PostCreate, PostUpdate, PostResponse

router = APIRouter(prefix="/blog", tags=["blog"])

@router.get("", response_model=list[PostResponse])
def list_posts(db: Session = Depends(get_db)):
    return db.query(Post).filter(Post.published == True).order_by(Post.created_at.desc()).all()

@router.get("/{slug}", response_model=PostResponse)
def get_post(slug: str, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.slug == slug, Post.published == True).first()
    if not post:
        raise HTTPException(404, "Post não encontrado.")
    return post

# admin
@router.get("/admin/all", response_model=list[PostResponse])
def list_all_posts(db: Session = Depends(get_db), _: User = Depends(get_admin_user)):
    return db.query(Post).order_by(Post.created_at.desc()).all()

@router.post("/admin", response_model=PostResponse, status_code=201)
def create_post(body: PostCreate, db: Session = Depends(get_db), _: User = Depends(get_admin_user)):
    exists = db.query(Post).filter(Post.slug == body.slug).first()
    if exists:
        raise HTTPException(409, "Slug já existe.")
    post = Post(**body.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.patch("/admin/{post_id}", response_model=PostResponse)
def update_post(post_id: int, body: PostUpdate, db: Session = Depends(get_db), _: User = Depends(get_admin_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post não encontrado.")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(post, k, v)
    db.commit()
    db.refresh(post)
    return post

@router.delete("/admin/{post_id}", status_code=204)
def delete_post(post_id: int, db: Session = Depends(get_db), _: User = Depends(get_admin_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post não encontrado.")
    db.delete(post)
    db.commit()