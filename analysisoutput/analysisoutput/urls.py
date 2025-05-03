"""
URL configuration for analysisoutput project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include  # Import path function to define URL patterns
from output.views import SignUpView, FileUploadView, FileListView, process_file  # Import views from the current app
from django.contrib.auth.views import LoginView, LogoutView  # Import built-in login and logout views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/login/')),
    path('signup/', SignUpView.as_view(), name='signup'),  # URL for user signup, handled by SignUpView
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),  # URL for user login, uses built-in LoginView with a custom template
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # URL for user logout, uses built-in LogoutView
    path('upload/', FileUploadView.as_view(), name='upload'),  # URL for file uploads, handled by FileUploadView
    path('list/', FileListView.as_view(), name='file_list'),  # Default URL (home page) showing the list of uploaded files
    path('process/<int:file_id>/', process_file, name='process'),  # URL for processing a file, requires a file ID as an integer parameter
    path('admin/', admin.site.urls),
    path('files/', include('output.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

