
from django.urls import path

from .import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("follow", views.follow, name="follow"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("delete_like/<int:post_id>", views.delete_like, name="delete_like"),
    path("add_like/<int:post_id>", views.add_like, name="add_like"),
    path('post_data/<int:post_id>/', views.get_post_data, name='get_post_data'),

]
