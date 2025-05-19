from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'cvs', views.CVViewSet)

urlpatterns = [
    path('', views.CVListView.as_view(), name='cv_list'),
    path('cv/<int:pk>/', views.CVDetailView.as_view(), name='cv_detail'),
    path('cv/<int:pk>/pdf/', views.cv_pdf, name='cv_pdf'),
    path('cv/<int:pk>/translate/', views.translate_cv, name='cv_translate'),
    path('api/', include(router.urls)),
] 