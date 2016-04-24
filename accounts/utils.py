from django.contrib.auth.decorators import user_passes_test


def user_is_admin(func):
    def test(user):
        return user.is_authenticated() and user.is_superuser

    return user_passes_test(test, login_url="/admin/login/")(func)
