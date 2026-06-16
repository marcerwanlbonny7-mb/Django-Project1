from rest_framework.permissions import BasePermission


class EstClient(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'CLIENT'


class EstAgent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'AGENT'


class EstAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'


class EstAgentOuAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['AGENT', 'ADMIN']


class EstProprietaireOuAgentOuAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role == 'ADMIN':
            return True
        if hasattr(obj, 'client') and obj.client == user:
            return True
        if hasattr(obj, 'destinataire') and obj.destinataire == user:
            return True
        if hasattr(obj, 'user') and obj.user == user:
            return True
        if user.role == 'AGENT':
            return True
        return False
