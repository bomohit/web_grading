from django.urls import path

from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("home", views.home, name="home"),
    path("login", views.login, name="login"),
    path("selectionCourse", views.selectionCourse, name="selectionCourse"),
    path("selectionClass", views.selectionClass, name="selectionClass"),
    path("uploadQuestion", views.uploadQuestion, name="uploadQuestion"),
    path("submitAssignment", views.submitAssignment, name="submitAssignment"),
    path("showlist", views.showlist, name="showlist"),
    path("logout", views.logout, name="logout"),
]
