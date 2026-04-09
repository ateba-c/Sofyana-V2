def student_context(request):
    if not request.user.is_authenticated:
        return {'student': None, 'parent_profile': None}
    try:
        student = request.user.student
    except Exception:
        student = None
    try:
        parent_profile = request.user.parent_profile
    except Exception:
        parent_profile = None
    return {'student': student, 'parent_profile': parent_profile}
