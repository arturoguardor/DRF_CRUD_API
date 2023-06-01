from django.urls import path
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from products import views

router = routers.DefaultRouter()
router.register(r"products", views.ProductView, "products")

urlpatterns = [
    path("", views.ProductView.as_view()),
    path("docs/", include_docs_urls(title='Documentation Products API')),
    path('users/', views.UserList.as_view()),
]
