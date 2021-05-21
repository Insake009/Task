from django.urls import path
from rest_framework import routers
from .views import CategoryViewSet, TaskViewSet, CategoryTaskAPIView

router = routers.SimpleRouter()
router.register('category', CategoryViewSet)
router.register('task', TaskViewSet)

urlpatterns = router.urls


urlpatterns += [
    path('categories/', CategoryTaskAPIView.as_view())
]
