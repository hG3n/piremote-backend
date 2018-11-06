import tornado.web
import tornado.escape

class BaseHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        origin = self.request.headers.get('Origin')
        if origin:
            self.set_header('Access-Control-Allow-Origin', origin)

        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.set_header("Access-Control-Allow-Headers",
                        "x-requested-with, Content-Type, X-CSRF-Token, X-XSRF-Token, X-Xsrftoken, X-CSRFToken")

        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
