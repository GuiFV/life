"""project_name URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from life.core import views

urlpatterns = [
    # path('summernote/', include('django_summernote.urls')),
    path('profile/', views.profile, name='profile'),
    path('account/delete_account/', views.delete_account, name='delete_account'),
    path('edit_goal/<pk>', views.edit_goal, name='edit_goal'),
    path('notes/', views.notes, name='notes'),
    path('delete_goal/<pk>', views.delete_goal, name='delete_goal'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('gym/', include('life.gym.urls')),
    path('', views.home, name='home'),
]

urlpatterns += [
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
