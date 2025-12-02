from ninja import Router, Schema
from typing import List
from ninja_jwt.authentication import JWTAuth

from apps.comment.models import Comment

router = Router()


class CommentOut(Schema):
    id: int
    author_id: int
    author_username: str
    post_id: int
    content: str
    parent_id: int | None = None
    like_count: int
    is_edited: bool
    created_at: str


class CommentCreate(Schema):
    post_id: int
    content: str
    parent_id: int | None = None


class CommentUpdate(Schema):
    content: str


class PaginatedCommentsOut(Schema):
    total: int
    page: int
    size: int
    items: List[CommentOut]


class DeleteResponse(Schema):
    success: bool


@router.get("/", response=PaginatedCommentsOut)
def list_comments(request, page: int = 1, size: int = 20, post_id: int | None = None):
    size = max(1, min(size, 100))
    qs = Comment.objects.select_related('author', 'post').filter(is_hidden=False)
    if post_id:
        qs = qs.filter(post_id=post_id)
    qs = qs.order_by('created_at')
    total = qs.count()
    start = (page - 1) * size
    end = start + size
    qs_page = qs[start:end]
    items = [CommentOut(
        id=c.id,
        author_id=c.author_id,
        author_username=c.author.username,
        post_id=c.post_id,
        content=c.content,
        parent_id=c.parent_id,
        like_count=c.get_like_count(),
        is_edited=c.is_edited,
        created_at=c.created_at.isoformat(),
    ) for c in qs_page]
    return PaginatedCommentsOut(total=total, page=page, size=size, items=items)


@router.get("/{comment_id}", response=CommentOut)
def get_comment(request, comment_id: int):
    c = Comment.objects.select_related('author', 'post').filter(id=comment_id, is_hidden=False).first()
    if not c:
        return None
    return CommentOut(
        id=c.id,
        author_id=c.author_id,
        author_username=c.author.username,
        post_id=c.post_id,
        content=c.content,
        parent_id=c.parent_id,
        like_count=c.get_like_count(),
        is_edited=c.is_edited,
        created_at=c.created_at.isoformat(),
    )


@router.post("/", auth=JWTAuth(), response=CommentOut)
def create_comment(request, data: CommentCreate):
    from apps.post.models import Post
    post = Post.objects.filter(id=data.post_id).first()
    if not post:
        return None
    c = Comment.objects.create(
        author=request.user,
        post_id=data.post_id,
        content=data.content,
        parent_id=data.parent_id,
    )
    return CommentOut(
        id=c.id,
        author_id=c.author_id,
        author_username=c.author.username,
        post_id=c.post_id,
        content=c.content,
        parent_id=c.parent_id,
        like_count=0,
        is_edited=c.is_edited,
        created_at=c.created_at.isoformat(),
    )


@router.put("/{comment_id}", auth=JWTAuth(), response=CommentOut)
def update_comment(request, comment_id: int, data: CommentUpdate):
    c = Comment.objects.select_related('author').filter(id=comment_id, is_hidden=False).first()
    if not c:
        return None
    if c.author_id != request.user.id:
        return None
    c.content = data.content
    c.mark_as_edited()
    return CommentOut(
        id=c.id,
        author_id=c.author_id,
        author_username=c.author.username,
        post_id=c.post_id,
        content=c.content,
        parent_id=c.parent_id,
        like_count=c.get_like_count(),
        is_edited=c.is_edited,
        created_at=c.created_at.isoformat(),
    )


@router.delete("/{comment_id}", auth=JWTAuth(), response=DeleteResponse)
def delete_comment(request, comment_id: int):
    c = Comment.objects.filter(id=comment_id, is_hidden=False).first()
    if not c:
        return DeleteResponse(success=False)
    if c.author_id != request.user.id:
        return DeleteResponse(success=False)
    c.delete()
    return DeleteResponse(success=True)
