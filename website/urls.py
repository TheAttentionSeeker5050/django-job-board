from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from users.views import UserLoginView, UserRegisterView, UserLogoutView, DummyLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    
    # the user routes
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    # dummy login
    path('dummy-login/', DummyLoginView.as_view(), name='dummy-login'),

    # app routes
    path('profile/', include('users.urls')),
    path('companies/', include('companies.urls')),
    path('jobs/', include('jobs.urls')),
    path('resumes/', include('resumes.urls')),
    path('applications/', include('applications.urls')),

    # django browser reload
    path("__reload__/", include("django_browser_reload.urls")),

    # text editor import
    path('tinymce/', include('tinymce.urls')),

    # error pages
    path('error/', TemplateView.as_view(template_name='error.html'), name='error'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
