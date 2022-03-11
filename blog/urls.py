from django.urls import path, include

from rest_framework import routers
from .api import BlogViewSet

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register('api/blog', BlogViewSet, 'blog')


urlpatterns = router.urls + [
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('pages/', include(wagtail_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)