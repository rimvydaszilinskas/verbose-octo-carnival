class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_arg, view_kwargs):
        # TODO talk with authentication microservice
        print("middleware workign!")
        pass
