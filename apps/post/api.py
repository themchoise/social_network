from ninja import Router, Schema
from typing import List
from ninja_jwt.authentication import JWTAuth

from apps.post.models import Post

router = Router()


class AuthorDetail(Schema):
    id: int
    username: str
    level: int
    total_points: int
    is_verified: bool


class PostOut(Schema):
    id: int
    author_id: int
    author_username: str
    author: AuthorDetail
    content: str
    views_count: int
    like_count: int
    comment_count: int
    created_at: str


class PostCreate(Schema):
    content: str


class PostUpdate(Schema):
    content: str


class PaginatedPostsOut(Schema):
    total: int
    page: int
    size: int
    items: List[PostOut]


class DeleteResponse(Schema):
    success: bool


@router.get("/", response=PaginatedPostsOut)
def list_posts(request, page: int = 1, size: int = 20, search: str | None = None, ordering: str | None = None):
    size = max(1, min(size, 100))
    qs = Post.objects.select_related('author').filter(is_hidden=False)
    if search:
        qs = qs.filter(content__icontains=search)
    allowed_ordering = {
        'created_at': 'created_at',
        '-created_at': '-created_at',
        'views_count': 'views_count',
        '-views_count': '-views_count',
    }
    order_field = allowed_ordering.get(ordering or '-created_at', '-created_at')
    qs = qs.order_by(order_field)
    total = qs.count()
    start = (page - 1) * size
    end = start + size
    qs_page = qs[start:end]
    items = [PostOut(
        id=p.id,
        author_id=p.author_id,
        author_username=p.author.username,
        author=AuthorDetail(
            id=p.author.id,
            username=p.author.username,
            level=p.author.level,
            total_points=p.author.total_points,
            is_verified=p.author.is_verified,
        ),
        content=p.content,
        views_count=p.views_count,
        like_count=p.get_like_count(),
        comment_count=p.get_comment_count(),
        created_at=p.created_at.isoformat(),
    ) for p in qs_page]
    return PaginatedPostsOut(total=total, page=page, size=size, items=items)


@router.get("/{post_id}", response=PostOut)
def get_post(request, post_id: int):
    p = Post.objects.select_related('author').filter(id=post_id, is_hidden=False).first()
    if not p:
        return None
    return PostOut(
        id=p.id,
        author_id=p.author_id,
        author_username=p.author.username,
        author=AuthorDetail(
            id=p.author.id,
            username=p.author.username,
            level=p.author.level,
            total_points=p.author.total_points,
            is_verified=p.author.is_verified,
        ),
        content=p.content,
        views_count=p.views_count,
        like_count=p.get_like_count(),
        comment_count=p.get_comment_count(),
        created_at=p.created_at.isoformat(),
    )


@router.post("/", auth=JWTAuth(), response=PostOut)
def create_post(request, data: PostCreate):
    user = request.user
    p = Post.objects.create(author=user, content=data.content)
    return PostOut(
        id=p.id,
        author_id=p.author_id,
        author_username=p.author.username,
        author=AuthorDetail(
            id=p.author.id,
            username=p.author.username,
            level=p.author.level,
            total_points=p.author.total_points,
            is_verified=p.author.is_verified,
        ),
        content=p.content,
        views_count=p.views_count,
        like_count=0,
        comment_count=0,
        created_at=p.created_at.isoformat(),
    )


@router.put("/{post_id}", auth=JWTAuth(), response=PostOut)
def update_post(request, post_id: int, data: PostUpdate):
    p = Post.objects.select_related('author').filter(id=post_id, is_hidden=False).first()
    if not p:
        return None
    if p.author_id != request.user.id:
        return None  # could raise 403; returning None yields 404 style
    p.content = data.content
    p.save(update_fields=["content", "updated_at"])
    return PostOut(
        id=p.id,
        author_id=p.author_id,
        author_username=p.author.username,
        author=AuthorDetail(
            id=p.author.id,
            username=p.author.username,
            level=p.author.level,
            total_points=p.author.total_points,
            is_verified=p.author.is_verified,
        ),
        content=p.content,
        views_count=p.views_count,
        like_count=p.get_like_count(),
        comment_count=p.get_comment_count(),
        created_at=p.created_at.isoformat(),
    )


@router.delete("/{post_id}", auth=JWTAuth(), response=DeleteResponse)
def delete_post(request, post_id: int):
    p = Post.objects.filter(id=post_id, is_hidden=False).first()
    if not p:
        return DeleteResponse(success=False)
    if p.author_id != request.user.id:
        return DeleteResponse(success=False)
    p.delete()
    return DeleteResponse(success=True)
