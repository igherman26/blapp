from django.conf.urls.static import static
from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from rest_framework import routers
from blapp import views

router = routers.DefaultRouter()
router.register(r'profiles', views.ProfileViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'likes', views.LikeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)