from django.urls import path
from . import views

urlpatterns=[
    path("",views.home,name="home"),
    path("room/<str:pk>/",views.room,name="room"),
    path("create-room/",views.Create_Room,name="create-room"),
    path("update-room/<str:pk>/",views.Update_Room,name="update-room"),
    path("delete/<str:pk>/",views.delete,name="delete"),
    path("login/",views.loginPage, name="login"),
    path("logout/",views.logoutPage, name="logout"),
    path("register/",views.registerPage, name="register"),
    path("delete-message/<str:pk>/",views.deleteMessage,name="delete-message"),
    path("profile/<str:pk>/",views.userProfile,name="profile"),
    path("update-user/",views.updateUser,name="update-user"),
    path("topics/",views.topicsPage,name="topics"),
    path("activity/",views.activity,name="activity"),
]