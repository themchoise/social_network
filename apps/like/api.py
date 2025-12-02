from ninja import Router, Schema
from ninja_jwt.authentication import JWTAuth

from apps.like.models import Like

router = Router()


class LikeToggleResponse(Schema):
    success: bool
    liked: bool
    like_count: int


@router.post("/{post_id}/like", auth=JWTAuth(), response=LikeToggleResponse)
def toggle_post_like(request, post_id: int):
    from apps.post.models import Post
    post = Post.objects.filter(id=post_id).first()
    if not post:
        return LikeToggleResponse(success=False, liked=False, like_count=0)
    
    like_instance, created = Like.objects.toggle_like(request.user, post)
    liked = created
    like_count = Like.objects.get_like_count_for_object(post)
    
    return LikeToggleResponse(success=True, liked=liked, like_count=like_count)
