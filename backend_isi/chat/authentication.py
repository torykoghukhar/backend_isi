from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            access_token = request.COOKIES.get('access_token')
            if access_token:
                raw_token = access_token
                validated_token = self.get_validated_token(raw_token)
                return self.get_user(validated_token), validated_token
        return super().authenticate(request)
