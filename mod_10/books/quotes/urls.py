from django.urls import path

from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.main, name="main"),
    path("page/<int:page>/", views.main, name="main"),
    path("author/add", views.add_author, name="add_author"),
    path("author/<str:question_id>", views.author, name="author"),
    path("tag/<str:tag_name>/page/<int:page>/", views.find_by_tag, name="find_by_tag"),
    path("tag/", views.tag, name="tag"),
    path("add/", views.add_quote, name="add_quote"),
]
