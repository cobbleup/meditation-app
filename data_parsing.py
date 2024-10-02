import os
import json
from http.cookies import SimpleCookie
from random import choices


cookies = SimpleCookie(os.getenv("HTTP_COOKIE"))


try:

    visits = int(cookies["visits"].value) + 1

except KeyError:

    visits = 1


cookies["visits"] = str(visits)

cookies["visits"]["max-age"] = 5  # Expire after 5 seconds

class WebRequestHandler(BaseHTTPRequestHandler):
    @cached_property
    def url(self):
        return urlparse(self.path)

    @cached_property
    def query_data(self):
        return dict(parse_qsl(self.url.query))

    @cached_property
    def post_data(self):
        content_length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(content_length)

    @cached_property
    def form_data(self):
        return dict(parse_qsl(self.post_data.decode("utf-8")))

    @cached_property
    def cookies(self):
        return SimpleCookie(self.headers.get("Cookie"))
    
    def get_response(self):
        return json.dumps(
            {
                'query_data': self.query_data(),

                'post_data': self.post_data.decode('UTF-8'),

                'form_data': self.form_data(),

                'cookies': {
                    name: cookie.value
                    for name, cookie in self.cookies.items()
                }
            }
        )

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(self.get_response().encode("utf-8"))

    def do_POST(self):
        self.do_GET()


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), WebRequestHandler)
    server.serve_forever()

