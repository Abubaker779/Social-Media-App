
from django.urls import path, re_path

from . import views

app_name="network"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    path("get",views.get_posts, name="get"),
    path("post",views.add_post, name="post"),
    re_path(r'^put/(?P<post_id>\d+)/(?P<modification_type>[^/]+)/?(?P<extra>comment)?/?$', views.modify_post, name='put'), 
    path("follow/<int:person_id>/<str:n_o_t>", views.follow, name="follow")
]
