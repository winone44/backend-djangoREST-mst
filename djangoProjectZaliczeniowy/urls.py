"""djangoProjectZaliczeniowy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from rest_framework.routers import DefaultRouter
from myapp.views import ArticleViewSet, CommentViewSet
from django.urls import path, include

#
# Pracujemy na klasie router która na podstawie widoku będzie wstanie wygenerować zasoby
#


router = DefaultRouter()  # Tworzymy router
router.register('api/articles', ArticleViewSet)  # Rejestrujemy klasę widoku pod zasobem. Potrzeba podać prefix
router.register('api/comments', CommentViewSet)  # Rejestrujemy klasę widoku pod zasobem. Potrzeba podać prefix

urlpatterns = router.urls  # urlpatterns - plik reprezentujący zasoby musi zawierać zmienna która posiada lisę zasobów

urlpatterns += [
    path('api/users/', include('users.urls')),
    path('admin/', admin.site.urls),
]
