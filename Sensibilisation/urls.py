from django.urls import path
from . import views

urlpatterns = [
    path("training/", views.training_page, name="training"),
    # path("quiz/", views.quiz_page, name="quiz"),
]
