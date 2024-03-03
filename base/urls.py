from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("login/", views.login_page, name="login"),

    path("register/", views.register_page, name="register"),

    path("log-out/", views.log_out, name="log-out"),

    # Dynamic url redirection (pk is extra parameter(id) passed with the url which is of string type)
    path("room/<str:pk>/", views.room, name="room"),

    # URL path for user profile
    path("profile/<str:pk>/", views.user_profile, name="user-profile"),
    
    # URL of input form for user to create their own room 
    path("create-room/", views.create_room, name="create_room"),
    
    # URL Path for updating the room which was created
    path("update-room/<str:pk>/", views.update_room, name="update_room"),

    # URL Path for deleting room With pk as id-> parameter
    path("delete-room/<str:pk>/", views.delete_room, name="delete_room"),

    path("delete-message/<str:pk>/", views.delete_message, name="delete-message"),

    path("update-user/", views.update_user, name="update-user"),

    # For mobile responsive
    path("topics/", views.show_topics, name="topics"),

    path("activities/", views.activities, name="activities"),

    path("like-room/<str:pk>/", views.like_room, name="like_room"),
]
