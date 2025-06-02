def user_roles(request):
    return {
        'is_teacher': request.user.is_authenticated and getattr(request.user, 'role', None) == "teacher",
        'is_student': request.user.is_authenticated and getattr(request.user, 'role', None) == "student",
    }




