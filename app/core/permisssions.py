from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Check that login user is an administrator.
    """

    def has_permission(self, request, view):
        user = request.user \
            if request.user.is_authenticated else None
        if user:
            return user.is_staff
        return False


class IsTeacherUser(permissions.BasePermission):
    """
    Check that login user is a Teacher.
    """

    def has_permission(self, request, view):
        user = request.user \
            if request.user.is_authenticated else None
        if user:
            return user.is_staff or user.is_teacher
        return False


class IsStudentUser(permissions.BasePermission):
    """
    Check that login user is a Student.
    """

    def has_permission(self, request, view):
        user = request.user \
            if request.user.is_authenticated else None
        if user:
            return user.is_staff or user.is_student \
                or user.is_student
        return False


class IsGuardianUser(permissions.BasePermission):
    """
    Check that login user is a Guardian.
    """

    def has_permission(self, request, view):
        user = request.user \
            if request.user.is_authenticated else None
        if user:
            return user.is_staff or user.is_student \
                or user.is_student or user.is_guardian
        return False
