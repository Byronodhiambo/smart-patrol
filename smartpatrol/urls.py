"""smartpatrol URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from chat import views as chat_views

extra_patterns =  [
    path('chat/', chat_views.index, name='index'),
    path('report/', chat_views.report, name='report'),
    path('help/', chat_views.help, name='help'),

]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls', namespace='chat')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('chat_view/', include(extra_patterns)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
