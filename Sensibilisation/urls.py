from django.urls import path
from . import views

urlpatterns = [
    # path("training/", views.training_page, name="training"),
    path("sensibilisation/qcm/", views.qcm_page, name="qcm"),
    path("sensibilisation/submit-qcm/", views.cal_qcm_result, name="submit_qcm"),
    path("qcm-result/", views.qcm_result, name="qcm_result"),
    # path("quiz/", views.quiz_page, name="quiz"),
]
