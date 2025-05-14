from rest_framework import routers
from .views import VentaViewSet


router = routers.DefaultRouter()
router.register(r'ventas', VentaViewSet)



urlpatterns = router.urls
