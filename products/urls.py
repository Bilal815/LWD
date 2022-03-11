from django.urls import path
from .views import api_create_contact_view
from django.urls import path, include
from . import views, viewsets
from rest_framework import routers

router = routers.DefaultRouter()

router.register("api/products", views.ProductDocumentView)
router.register("api/product-lists", views.ListProductView)
router.register("api/product-search", viewsets.ProductSearchViewSet)

app_name = "products"

urlpatterns = [
    path('api/contact', api_create_contact_view, name='contact'),
    path("api/category/", views.CategoryListAPIView.as_view()),
    path("api/category/<int:pk>/", views.CategoryAPIView.as_view()),
    path("api/list/product/", views.ListProductAPIView.as_view()),
    path("api/serpy/product/", views.SerpyListProductAPIView.as_view()),
    path("api/list-product/user/", views.ListUserProductAPIView.as_view()),
    path("api/create/product/", views.CreateProductAPIView.as_view()),
    path("api/product/<int:pk>/delete/", views.DestroyProductAPIView.as_view()),
    path("api/product/<str:uuid>/", views.ProductDetailView.as_view()),
    path("api/product/views/", views.ProductViewsAPIView.as_view()),
    # Try requests lib and microservices here. #
    path("api/micro/", views.ListMicroServiceView.as_view()),
    path("api/micro/create/", views.MicroServiceCreateView.as_view()),
    path("api/get/", views.GETRequests.as_view()),
    path("api/post/", views.POSTRequests.as_view()),
] + router.urls

urlpatterns += [
    path('api/search/', include('haystack.urls')),
]