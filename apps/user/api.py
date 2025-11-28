from ninja import Router, Schema
from ninja.security import django_auth
from typing import List

from apps.user.models import User

router = Router()


class UserOut(Schema):
    id: int
    username: str
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None


class UserCreate(Schema):
    username: str
    email: str | None = None
    password: str
    first_name: str | None = None
    last_name: str | None = None


@router.get("/", response=List[UserOut])
def list_users(request):
    qs = User.objects.all().only('id', 'username', 'email', 'first_name', 'last_name')
    return [UserOut(
        id=u.id,
        username=u.username,
        email=u.email,
        first_name=u.first_name,
        last_name=u.last_name,
    ) for u in qs]


@router.get("/{user_id}", response=UserOut)
def get_user(request, user_id: int):
    u = User.objects.filter(id=user_id).first()
    if not u:
        return  None
    return UserOut(
        id=u.id,
        username=u.username,
        email=u.email,
        first_name=u.first_name,
        last_name=u.last_name,
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
    )
