from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ThreadViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'threads', ThreadViewSet, basename='thread')

threads_router = NestedDefaultRouter(router, r'threads', lookup='thread')
threads_router.register(r'messages', MessageViewSet, basename='thread-messages')

urlpatterns = router.urls + threads_router.urls
