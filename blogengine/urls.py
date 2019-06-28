from django.contrib import admin
from django.urls import path, include
from .views import redirect_block
from users import views as usersView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', redirect_block),
    path('admin/', admin.site.urls),
    path('api/v1/blog/', include('blog.urls')),
    # path('api/v1/auth/', include('rest_framework.urls')),
    path('blog/', include('blog.urls')),
    path('registration/', usersView.signup, name="registration"),
    path('auth/registration/', usersView.UserCreateAPIView.as_view(), name="auth-registration"),
    path('logout/', usersView.logout_view, name="logout"),
    path('login/', usersView.login_view, name="login"),
    path('auth/login/', usersView.login_rest, name="auth-login"),
    path('profile/', usersView.profile, name="profile"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
