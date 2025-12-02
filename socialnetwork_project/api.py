from ninja import NinjaAPI

from apps.user.api import router as user_router
from apps.user.gamification_api import router as gamification_router
from apps.post.api import router as post_router
from apps.comment.api import router as comment_router
from apps.note.api import router as note_router
from apps.like.api import router as like_router

# token routers provided by ninja_jwt
from ninja_jwt.routers.obtain import obtain_pair_router, sliding_router
from ninja_jwt.routers.verify import verify_router
from ninja_jwt.routers.blacklist import blacklist_router

api = NinjaAPI(title="Social Network API", version="1.0")

api.add_router("/users/", user_router)
api.add_router("/users/", gamification_router)
api.add_router("/posts/", post_router)
api.add_router("/comments/", comment_router)
api.add_router("/notes/", note_router)
api.add_router("/posts/", like_router)

# mount token endpoints
api.add_router("/token/", obtain_pair_router)
api.add_router("/token/", sliding_router)
api.add_router("/token/", verify_router)
api.add_router("/token/", blacklist_router)

