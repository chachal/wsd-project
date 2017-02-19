from shop.models import User

"""
Check if user has admin status.
"""
def check_admin(user):
    if (user.is_authenticated() and (user.profile.role == "admin") or (user.is_superuser)):
        return True
    return False

"""
Check if user has developer status.
"""
def check_developer(user):
    if (user.is_authenticated() and (user.profile.role == "developer" \
        or user.profile.role == 'admin' \
        or user.is_superuser)):
        return True
    return False
