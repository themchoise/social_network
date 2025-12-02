from ninja import Router, Schema
from typing import List
from ninja_jwt.authentication import JWTAuth

from apps.note.models import Note

router = Router()


class NoteOut(Schema):
    id: int
    title: str
    content: str
    author_id: int
    author_username: str
    subject_id: int
    note_type: str
    privacy_level: str
    views_count: int
    downloads_count: int
    is_featured: bool
    created_at: str


class NoteCreate(Schema):
    title: str
    content: str
    subject_id: int
    note_type: str = 'class'
    privacy_level: str = 'public'
    tags: str | None = None


class NoteUpdate(Schema):
    title: str | None = None
    content: str | None = None
    note_type: str | None = None
    privacy_level: str | None = None
    tags: str | None = None


class PaginatedNotesOut(Schema):
    total: int
    page: int
    size: int
    items: List[NoteOut]


class DeleteResponse(Schema):
    success: bool


@router.get("/", response=PaginatedNotesOut)
def list_notes(request, page: int = 1, size: int = 20, author_id: int | None = None, subject_id: int | None = None, search: str | None = None):
    size = max(1, min(size, 100))
    qs = Note.objects.select_related('author', 'subject').filter(is_active=True, privacy_level='public')
    if author_id:
        qs = qs.filter(author_id=author_id)
    if subject_id:
        qs = qs.filter(subject_id=subject_id)
    if search:
        qs = qs.filter(title__icontains=search)
    qs = qs.order_by('-created_at')
    total = qs.count()
    start = (page - 1) * size
    end = start + size
    qs_page = qs[start:end]
    items = [NoteOut(
        id=n.id,
        title=n.title,
        content=n.content,
        author_id=n.author_id,
        author_username=n.author.username,
        subject_id=n.subject_id,
        note_type=n.note_type,
        privacy_level=n.privacy_level,
        views_count=n.views_count,
        downloads_count=n.downloads_count,
        is_featured=n.is_featured,
        created_at=n.created_at.isoformat(),
    ) for n in qs_page]
    return PaginatedNotesOut(total=total, page=page, size=size, items=items)


@router.get("/{note_id}", response=NoteOut)
def get_note(request, note_id: int):
    n = Note.objects.select_related('author', 'subject').filter(id=note_id, is_active=True).first()
    if not n:
        return None
    return NoteOut(
        id=n.id,
        title=n.title,
        content=n.content,
        author_id=n.author_id,
        author_username=n.author.username,
        subject_id=n.subject_id,
        note_type=n.note_type,
        privacy_level=n.privacy_level,
        views_count=n.views_count,
        downloads_count=n.downloads_count,
        is_featured=n.is_featured,
        created_at=n.created_at.isoformat(),
    )


@router.post("/", auth=JWTAuth(), response=NoteOut)
def create_note(request, data: NoteCreate):
    from apps.subject.models import Subject
    subject = Subject.objects.filter(id=data.subject_id).first()
    if not subject:
        return None
    n = Note.objects.create(
        title=data.title,
        content=data.content,
        author=request.user,
        subject_id=data.subject_id,
        note_type=data.note_type,
        privacy_level=data.privacy_level,
        tags=data.tags or '',
    )
    return NoteOut(
        id=n.id,
        title=n.title,
        content=n.content,
        author_id=n.author_id,
        author_username=n.author.username,
        subject_id=n.subject_id,
        note_type=n.note_type,
        privacy_level=n.privacy_level,
        views_count=n.views_count,
        downloads_count=n.downloads_count,
        is_featured=n.is_featured,
        created_at=n.created_at.isoformat(),
    )


@router.put("/{note_id}", auth=JWTAuth(), response=NoteOut)
def update_note(request, note_id: int, data: NoteUpdate):
    n = Note.objects.select_related('author', 'subject').filter(id=note_id, is_active=True).first()
    if not n:
        return None
    if n.author_id != request.user.id:
        return None
    if data.title is not None:
        n.title = data.title
    if data.content is not None:
        n.content = data.content
    if data.note_type is not None:
        n.note_type = data.note_type
    if data.privacy_level is not None:
        n.privacy_level = data.privacy_level
    if data.tags is not None:
        n.tags = data.tags
    n.save()
    return NoteOut(
        id=n.id,
        title=n.title,
        content=n.content,
        author_id=n.author_id,
        author_username=n.author.username,
        subject_id=n.subject_id,
        note_type=n.note_type,
        privacy_level=n.privacy_level,
        views_count=n.views_count,
        downloads_count=n.downloads_count,
        is_featured=n.is_featured,
        created_at=n.created_at.isoformat(),
    )


@router.delete("/{note_id}", auth=JWTAuth(), response=DeleteResponse)
def delete_note(request, note_id: int):
    n = Note.objects.filter(id=note_id, is_active=True).first()
    if not n:
        return DeleteResponse(success=False)
    if n.author_id != request.user.id:
        return DeleteResponse(success=False)
    n.delete()
    return DeleteResponse(success=True)
