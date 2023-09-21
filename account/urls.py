from django.urls import path, include
from rest_framework.routers import SimpleRouter
from account.views import UserViewSet, CustomLoginView, CustomLogoutView

router = SimpleRouter()
router.register('', UserViewSet)

urlpatterns = [
    path('login/', CustomLoginView.as_view()),
    path('logout/', CustomLogoutView.as_view()),
    path('', include(router.urls)),
]
