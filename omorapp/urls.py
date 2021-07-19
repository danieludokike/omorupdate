from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "omorapp"
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("blogs/", views.blog_post_display_view, name='blog'),
    path("blog/<int:pk>/details/", views.blog_post_detail_view, name='blog_details'),

    path("about-omor-update/", views.about_omorupdate_view, name='about'),
    path("team-omor-update/", views.omorupdate_members, name='members'),

    path("user/contact/", views.UserContactView.as_view(), name='contact'),

    path("account/user/signup/", views.UserSignupView.as_view(), name='signup'),
    path("account/user/signup-success/", views.registration_success_view, name="registration_success"),
    path("account/user/login/", views.UserLoginView.as_view(), name='login'),
    path("account/user/join-team-omor-update", views.join_omor_update, name="join_team"),
    path("account/user/logout/", views.logout_view, name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
