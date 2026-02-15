
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('api/v1/docs/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('api/v1/auth/', include('users.urls')),
    path('api/v1/auth/', include('authentication.urls')),
    path('api/v1/', include('main.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
