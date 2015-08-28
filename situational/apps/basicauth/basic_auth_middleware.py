from django.http import HttpResponse
from django.conf import settings


class BasicAuthMiddleware(object):

    def unauthed(self):
        response = HttpResponse(
            """<html><title>Auth required</title><body>
               <h1>Authorization Required</h1></body></html>""",
            content_type="text/html")
        response['WWW-Authenticate'] = 'Basic realm="Development"'
        response.status_code = 401
        return response

    def _auth_required(self):
        if settings.BASICAUTH_DISABLED == "True":
            return False
        return True

    def process_request(self, request):
        if not self._auth_required():
            return None

        import base64
        if 'HTTP_AUTHORIZATION' not in request.META:
            return self.unauthed()
        else:
            authentication = request.META['HTTP_AUTHORIZATION']
            (authmeth, auth) = authentication.split(' ', 1)
            if 'basic' != authmeth.lower():
                return self.unauthed()
            auth = base64.b64decode(auth.strip()).decode('utf-8')
            username, password = auth.split(':', 1)
            if username == settings.BASICAUTH_USERNAME \
                    and password == settings.BASICAUTH_PASSWORD:
                return None

            return self.unauthed()
