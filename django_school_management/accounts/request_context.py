from threading import local


_request_user_context = local()

class RequestUserContext:
    @staticmethod
    def set_current_user(user):
        _request_user_context.user = user

    @staticmethod
    def get_current_user():
        return getattr(_request_user_context, 'user', None)

    @staticmethod
    def clear_current_user():
        _request_user_context.user = None
