from django.urls import path
from . import views
from .views import (LoginView, Logout, Register)

urlpatterns = [
    # path('cms/', include("CMSManagement.urls")),
    path('login/', LoginView.as_view(), name='cms_login'),
    path('logout/', views.Logout, name='cms_logout'),
    path('register/', views.Register, name='cms_register'),
    path('restpwd/', views.RestPsw, name='cms_restpwd'),
    path('updatePhone/', views.updatePhone, name='cms_updatePhone'),
    path('addphone/', views.AddPhone, name='cms_AddPhone'),
    path('test/', views.test),
]
