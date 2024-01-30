# permissions.py

from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permissão personalizada para permitir apenas usuários administradores
    modificarem dados. Os usuários não administradores têm apenas permissão de leitura.
    """

    def has_permission(self, request, view):
        # Se o usuário for um administrador, eles têm permissão para todas as operações.
        return request.user and any(role.display == 'admin' for role in request.user.role.all())


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Permissão personalizada para permitir apenas usuários com a função 'staff'
    modificarem dados. Os usuários não 'staff' têm apenas permissão de leitura.
    """

    """
    def has_permission(self, request, view):
        # Se o usuário for 'staff', eles têm permissão para todas as operações.
        return request.user and request.user.role.display == 'staff'
    """
    def has_permission(self, request, view):
        # Se o usuário for 'staff', eles têm permissão para todas as operações.
        return request.user and any(role.display == 'staff' for role in request.user.role.all())


class IsSupportOrReadOnly(permissions.BasePermission):
    """
    Permissão personalizada para permitir apenas usuários com a função 'support'
    modificarem dados. Os usuários não 'support' têm apenas permissão de leitura.
    """

    def has_permission(self, request, view):
        # Se o usuário for 'support', eles têm permissão para todas as operações.
        return request.user and any(role.display == 'support' for role in request.user.role.all())

class IsPatientOrReadOnly(permissions.BasePermission):
    """
    Permissão personalizada para permitir apenas usuários com a função 'patient'
    modificarem dados. Os usuários não 'patient' têm apenas permissão de leitura.
    """

    def has_permission(self, request, view):
        # Se o usuário for 'patient', eles têm permissão para todas as operações.
        # return request.user and request.user.role.id == 'patient'
        return request.user and any(role.display == 'patient' for role in request.user.role.all())


