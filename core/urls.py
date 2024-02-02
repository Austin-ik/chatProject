from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('chat/api/', include('chat.urls')),  # new
    path('admin/', admin.site.urls),
]
