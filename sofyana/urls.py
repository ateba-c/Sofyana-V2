from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('qa/', include('qastudio.urls')),
    path('', include('quiz.urls')),
]
