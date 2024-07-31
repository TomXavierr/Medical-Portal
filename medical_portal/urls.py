from django.contrib import admin
from django.urls import path, include
from accounts.views import home, doctor_dashboard_view, patient_dashboard_view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('og-admin/', admin.site.urls),
    path('',home, name='home'),
    path('accounts/',include('accounts.urls')),
    
    path('doctor_dashboard/', doctor_dashboard_view, name='doctor_dashboard'),
    path('patient_dashboard/', patient_dashboard_view, name='patient_dashboard'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)