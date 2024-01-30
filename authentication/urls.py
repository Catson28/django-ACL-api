# authentication/urls.py
from django.contrib import admin
from django.urls import path
from authentication import views as auth_view
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('auth/login', auth_view.CustomLoginView.as_view(), name='custom-login'),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('protected-view/', auth_view.ProtectedView.as_view(), name='protected-view'),

    path('support/auth/login', auth_view.SupportLoginView.as_view()),
    path("support/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Adicione a URL protegida com base na permissão 'IsSupportOrReadOnly'
    path('support/protected-view/', auth_view.SupportProtectedView.as_view(), name='support-protected-view'),

    path('patient/auth/login', auth_view.PatientLoginView.as_view()),
    path("patient/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Adicione a URL protegida com base na permissão 'IsPatientOrReadOnly'
    path('patient/protected-view/', auth_view.PatientProtectedView.as_view(), name='patient-protected-view'),

    path('admin/auth/login', auth_view.AdminLoginView.as_view()),
    path("admin/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Adicione a URL protegida com base na permissão 'IsAdminOrReadOnly'
    path('admin/protected-view/', auth_view.AdminProtectedView.as_view(), name='admin-protected-view'),

    path('staff/auth/login', auth_view.StaffLoginView.as_view()),
    path("staff/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Adicione a URL protegida com base na permissão 'IsStaffOrReadOnly'
    path('staff/protected-view/', auth_view.StaffProtectedView.as_view(), name='staff-protected-view'),
    path('auth/logout/', auth_view.LogoutView.as_view(), name='logout'),
]
