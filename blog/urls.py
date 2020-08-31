from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from blog.views import LoginView, logout_view
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.posts, name='posts'),
    path('new_post/', views.new_post, name='new_post'),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path('register/', views.register, name='register'),
    path('from_old_to_new/', views.sort_posts_from_old_to_new, name='from_old_to_new'),
    path('from_new_to_old/', views.sort_posts_from_new_to_old, name='from_new_to_old'),
    path('from_last_24_hours/', views.sort_posts_from_last_24_hours, name='from_last_24_hours'),
    path('current_user_posts/', views.current_user_posts, name='current_user_posts'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
