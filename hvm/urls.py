from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeadVisitorViewSet, AccompanyingViewSet, ReceiverViewSet, is_expired, MyObtainTokenPairView, LogoutView, RegisterView, getReceivers
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'leadvisitor', LeadVisitorViewSet)
router.register(r'accompanying', AccompanyingViewSet)
router.register(r'receivers', ReceiverViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('status/', is_expired, name='is_expired'),
    path('token/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('register/', RegisterView.as_view(), name='auth_register'),
]