from ninja import NinjaAPI

from apps.user.api import router as user_router
from apps.post.api import router as post_router

# token routers provided by ninja_jwt
from ninja_jwt.routers.obtain import obtain_pair_router, sliding_router
from ninja_jwt.routers.verify import verify_router
from ninja_jwt.routers.blacklist import blacklist_router

api = NinjaAPI(title="Social Network API", version="1.0")

api.add_router("/users/", user_router)
api.add_router("/posts/", post_router)

# mount token endpoints
api.add_router("/token/", obtain_pair_router)
api.add_router("/token/", sliding_router)
api.add_router("/token/", verify_router)
api.add_router("/token/", blacklist_router)

