from ninja import Router, Schema
from typing import List
from ninja_jwt.authentication import JWTAuth

from apps.user.models import User, UserPointsHistory
from apps.achievement.models import UserAchievement

router = Router()


class UserStatsOut(Schema):
    user_id: int
    username: str
    total_points: int
    level: int
    experience_points: int
    achievements_count: int
    posts_count: int
    comments_count: int


class AchievementOut(Schema):
    id: int
    name: str
    description: str
    points: int
    earned_at: str


class LeaderboardEntry(Schema):
    rank: int
    user_id: int
    username: str
    total_points: int
    level: int
    is_verified: bool


class LeaderboardOut(Schema):
    entries: List[LeaderboardEntry]


class PointsHistoryOut(Schema):
    points: int
    source: str
    description: str
    created_at: str


class AwardPointsRequest(Schema):
    user_id: int
    points: int
    source: str = 'admin_bonus'
    description: str | None = None


class AwardPointsResponse(Schema):
    success: bool
    new_total: int
    new_level: int


@router.get("/{user_id}/stats", response=UserStatsOut)
def get_user_stats(request, user_id: int):
    user = User.objects.filter(id=user_id).first()
    if not user:
        return None
    
    achievements_count = user.user_achievements.count()
    posts_count = user.posts.count()
    comments_count = user.comments.count()
    
    return UserStatsOut(
        user_id=user.id,
        username=user.username,
        total_points=user.total_points,
        level=user.level,
        experience_points=user.experience_points,
        achievements_count=achievements_count,
        posts_count=posts_count,
        comments_count=comments_count,
    )


@router.get("/{user_id}/achievements", response=List[AchievementOut])
def get_user_achievements(request, user_id: int):
    user = User.objects.filter(id=user_id).first()
    if not user:
        return []
    
    user_achievements = UserAchievement.objects.filter(user=user).select_related('achievement')
    
    return [AchievementOut(
        id=ua.achievement.id,
        name=ua.achievement.name,
        description=ua.achievement.description,
        points=ua.achievement.points,
        earned_at=ua.earned_at.isoformat(),
    ) for ua in user_achievements]


@router.get("/leaderboard", response=LeaderboardOut)
def get_leaderboard(request, limit: int = 50):
    limit = max(1, min(limit, 100))
    top_users = User.objects.order_by('-total_points')[:limit]
    
    entries = [LeaderboardEntry(
        rank=idx + 1,
        user_id=u.id,
        username=u.username,
        total_points=u.total_points,
        level=u.level,
        is_verified=u.is_verified,
    ) for idx, u in enumerate(top_users)]
    
    return LeaderboardOut(entries=entries)


@router.get("/{user_id}/points-history", response=List[PointsHistoryOut])
def get_points_history(request, user_id: int, limit: int = 50):
    limit = max(1, min(limit, 100))
    history = UserPointsHistory.objects.filter(user_id=user_id).order_by('-created_at')[:limit]
    
    return [PointsHistoryOut(
        points=h.points,
        source=h.source,
        description=h.description,
        created_at=h.created_at.isoformat(),
    ) for h in history]


@router.post("/award-points", auth=JWTAuth(), response=AwardPointsResponse)
def award_points(request, data: AwardPointsRequest):
    # Only admin or staff can award points
    if not request.user.is_staff:
        return AwardPointsResponse(success=False, new_total=0, new_level=0)
    
    user = User.objects.filter(id=data.user_id).first()
    if not user:
        return AwardPointsResponse(success=False, new_total=0, new_level=0)
    
    # Add points
    user.add_points(data.points)
    
    # Create history entry
    UserPointsHistory.objects.create(
        user=user,
        points=data.points,
        source=data.source,
        description=data.description or f'Admin awarded {data.points} points',
    )
    
    return AwardPointsResponse(
        success=True,
        new_total=user.total_points,
        new_level=user.level,
    )
