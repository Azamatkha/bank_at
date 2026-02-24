from django.contrib import admin
from django.urls import path,include
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from bank_resurs_at.admin_site import resurs_admin_site

schema_view = get_schema_view(
    openapi.Info(
        title="Credit Details API",
        default_version='v1',
        description="API for Credit Details Integration",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admins/resurs/', resurs_admin_site.urls),
    path('swagger/',schema_view.with_ui('swagger',cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/bank-resurs/',include('bank_resurs_at.urls')),
    path('api/v1/bank/', include('bank_at.urls')),
    path("api/v1/token/", TokenObtainPairView.as_view()),
]
urlpatterns += [
    path(''.TemplateView.as_view(template_name="home.html")),
    path('login/', TemplateView.as_view(template_name="login.html")),
    path('home/', TemplateView.as_view(template_name="home.html")),
    path('payment/', TemplateView.as_view(template_name="payment.html")),
]