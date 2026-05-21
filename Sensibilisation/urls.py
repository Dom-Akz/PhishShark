from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("sensibilisation/training/<str:uuid>", views.training_page, name="training"),
    path("sensibilisation/qcm/", views.qcm_page, name="qcm"),
    path("sensibilisation/submit-qcm/", views.cal_qcm_result, name="submit_qcm"),
    path("qcm-result/", views.qcm_result, name="qcm_result"),
    # path("quiz/", views.quiz_page, name="quiz"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
