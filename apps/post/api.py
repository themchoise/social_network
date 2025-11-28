from ninja import Router, Schema
from typing import List
from ninja.security import django_auth

from ninja_jwt.authentication import JWTAuth

from apps.post.models import Post

router = Router()


class PostOut(Schema):
    id: int
    author_id: int
    content: str
    created_at: str


class PostCreate(Schema):
    content: str


@router.get("/", response=List[PostOut])
def list_posts(request):
    qs = Post.objects.select_related('author').filter(is_hidden=False).order_by('-created_at')[:50]
    result = []
    for p in qs:
        result.append(PostOut(
            id=p.id,
            author_id=p.author_id,
            content=p.content,
            created_at=p.created_at.isoformat(),
        ))
    return result


@router.get("/{post_id}", response=PostOut)
def get_post(request, post_id: int):
    p = Post.objects.filter(id=post_id, is_hidden=False).first()
    if not p:
        return None
    return PostOut(
        id=p.id,
        author_id=p.author_id,
        content=p.content,
        created_at=p.created_at.isoformat(),
    )


@router.post("/", auth=JWTAuth(), response=PostOut)
def create_post(request, data: PostCreate):
    user = request.user
    p = Post.objects.create(author=user, content=data.content)
    return PostOut(
        id=p.id,
        author_id=p.author_id,
        content=p.content,
        created_at=p.created_at.isoformat(),
    )
