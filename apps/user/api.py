from ninja import Router, Schema
from typing import List
from ninja_jwt.authentication import JWTAuth

from apps.user.models import User

router = Router()


class AchievementSummary(Schema):
    id: int
    name: str
    points: int


class UserOut(Schema):
    id: int
    username: str
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    total_points: int
    level: int
    is_verified: bool
    achievements: List[AchievementSummary] = []


class UserCreate(Schema):
    username: str
    email: str | None = None
    password: str
    first_name: str | None = None
    last_name: str | None = None


class UserUpdate(Schema):
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None


class PaginatedUsersOut(Schema):
    total: int
    page: int
    size: int
    items: List[UserOut]


class DeleteResponse(Schema):
    success: bool


@router.get("/", response=PaginatedUsersOut)
def list_users(request, page: int = 1, size: int = 20, search: str | None = None):
    size = max(1, min(size, 100))
    qs = User.objects.all()
    if search:
        qs = qs.filter(username__icontains=search)
    qs = qs.order_by('-created_at')
    total = qs.count()
    start = (page - 1) * size
    end = start + size
    qs_page = qs[start:end]
    items = []
    for u in qs_page:
        achievements = [AchievementSummary(
            id=ua.achievement.id,
            name=ua.achievement.name,
            points=ua.achievement.points,
        ) for ua in u.user_achievements.select_related('achievement')[:5]]
        items.append(UserOut(
            id=u.id,
            username=u.username,
            email=u.email,
            first_name=u.first_name,
            last_name=u.last_name,
            bio=u.bio,
            total_points=u.total_points,
            level=u.level,
            is_verified=u.is_verified,
            achievements=achievements,
        ))
    return PaginatedUsersOut(total=total, page=page, size=size, items=items)


@router.get("/{user_id}", response=UserOut)
def get_user(request, user_id: int):
    u = User.objects.filter(id=user_id).first()
    if not u:
        return None
    achievements = [AchievementSummary(
        id=ua.achievement.id,
        name=ua.achievement.name,
        points=ua.achievement.points,
    ) for ua in u.user_achievements.select_related('achievement')[:5]]
    return UserOut(
        id=u.id,
        username=u.username,
        email=u.email,
        first_name=u.first_name,
        last_name=u.last_name,
        bio=u.bio,
        total_points=u.total_points,
        level=u.level,
        is_verified=u.is_verified,
        achievements=achievements,
    )


@router.post("/", response=UserOut)
def create_user(request, data: UserCreate):
    u = User.objects.create_user(
        username=data.username,
        email=data.email,
        password=data.password,
        first_name=data.first_name or '',
        last_name=data.last_name or '',
    )
    return UserOut(
        id=u.id,
        username=u.username,
        email=u.email,
        first_name=u.first_name,
        last_name=u.last_name,
        bio=u.bio,
        total_points=u.total_points,
        level=u.level,
        is_verified=u.is_verified,
        achievements=[],
    )


@router.put("/{user_id}", auth=JWTAuth(), response=UserOut)
def update_user(request, user_id: int, data: UserUpdate):
    u = User.objects.filter(id=user_id).first()
    if not u:
        return None
    if u.id != request.user.id:
        return None
    if data.email is not None:
        u.email = data.email
    if data.first_name is not None:
        u.first_name = data.first_name
    if data.last_name is not None:
        u.last_name = data.last_name
    if data.bio is not None:
        u.bio = data.bio
    u.save()
    achievements = [AchievementSummary(
        id=ua.achievement.id,
        name=ua.achievement.name,
        points=ua.achievement.points,
    ) for ua in u.user_achievements.select_related('achievement')[:5]]
    return UserOut(
        id=u.id,
        username=u.username,
        email=u.email,
        first_name=u.first_name,
        last_name=u.last_name,
        bio=u.bio,
        total_points=u.total_points,
        level=u.level,
        is_verified=u.is_verified,
        achievements=achievements,
    )


@router.delete("/{user_id}", auth=JWTAuth(), response=DeleteResponse)
def delete_user(request, user_id: int):
    u = User.objects.filter(id=user_id).first()
    if not u:
        return DeleteResponse(success=False)
    if u.id != request.user.id:
        return DeleteResponse(success=False)
    u.delete()
    return DeleteResponse(success=True)
