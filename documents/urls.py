from rest_framework import routers
from .views import DocumentViewSet, CategoryViewSet, RegisterView, LogoutView
from django.urls import path

router = routers.DefaultRouter()
router.register(r'documents', DocumentViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = router.urls+ [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
]
