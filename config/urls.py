from routes.admin_routes import admin
from routes.user_routes import user

urlpatterns = [
    *admin.urls,
    *user.urls,
]
