from http.server import BaseHTTPRequestHandler, HTTPServer


class TestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        print(
            f"\nReceived request: {self.path}"
        )

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/plain"
        )

        self.end_headers()

        self.wfile.write(
            b"IDS SQL Injection Test Server"
        )


if __name__ == "__main__":

    server_address = (
        "127.0.0.1",
        8080
    )

    server = HTTPServer(
        server_address,
        TestHandler
    )

    print(
        "SQL Injection test server running on "
        "http://127.0.0.1:8080"
    )

    try:

        server.serve_forever()

    except KeyboardInterrupt:

        print(
            "\nStopping test server..."
        )

        server.server_close()