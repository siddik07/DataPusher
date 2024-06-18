
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from data import views

router = DefaultRouter()
router.register(r'accounts', views.AccountViewSet)
router.register(r'destinations', views.DestinationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/account/<uuid:account_id>/destinations/', views.get_destinations),
    path('server/incoming_data', views.incoming_data),
]

