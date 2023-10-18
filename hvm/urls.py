from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeadVisitorViewSet, AccompanyingViewSet, getAccompanyingVisitors, getLeadVisitors, is_expired, MyObtainTokenPairView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'leadvisitor', LeadVisitorViewSet)
router.register(r'accompanying', AccompanyingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('getAccompanyingVisitors/', getAccompanyingVisitors, name='getAccompanyingVisitors'),
    path('getLeadVisitors/', getLeadVisitors, name='getLeadVisitors'),
    path('status/', is_expired, name='is_expired'),
    path('token/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
]