from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registo/', views.registo_view, name='registo'),
    path('magic-login/', views.magic_login_request, name='magic_login'),
    path('magic-login/<str:token>/', views.magic_login_verify, name='magic_login_verify'),
]
