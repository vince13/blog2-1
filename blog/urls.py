from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.home, name="home"),
    path("detail/<int:pk>/", views.post_detail, name="detail"),
    path("new-post/", views.new_post, name="new_post"),
    path("update-post/<int:pk>/", views.update_post, name="update_post"),
    path("delete/<int:pk>/", views.delete_post, name="post_delete"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("user-posts/<str:username>/", views.one_user_post, name="user_post"),
    path("notifications/", views.notifications, name="notifications"),
]
