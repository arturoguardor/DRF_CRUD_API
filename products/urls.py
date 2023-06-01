from django.urls import include, path
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from products import views

router = routers.DefaultRouter()
router.register(r"products", views.ProductView, "products")

urlpatterns = [
    path("products/", include(router.urls)),
    path('docs/', include_docs_urls(title='Products API')),
]
