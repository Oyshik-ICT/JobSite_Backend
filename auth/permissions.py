from rest_framework.permissions import BasePermission
from core.choices import UserRole

class IsRecruiter(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == UserRole.RECRUITER
    
class IsCandidate(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == UserRole.CANDIDATE
    
class IsRecruiterOrCandidateOrAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (user.role in [UserRole.CANDIDATE, UserRole.RECRUITER] or user.is_staff)
    
    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.is_staff:
            return True
        if user.role == UserRole.RECRUITER:
            return True
        if user.role == UserRole.CANDIDATE:
            return obj == user
        
        return False