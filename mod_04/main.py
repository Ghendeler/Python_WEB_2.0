import json
import mimetypes
import pathlib
import socket
import urllib.parse
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == "/":
            self.send_html_file("index.html")
        elif pr_url.path == "/contact":
            self.send_html_file("contact.html")
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file("error.html", 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        with open(f".{self.path}", "rb") as file:
            self.wfile.write(file.read())

    def do_POST(self):
        data = self.rfile.read(int(self.headers["Content-Length"]))
        self.send_via_socket(data)
        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()

    def send_via_socket(self, data):
        ip = "127.0.0.1"
        port = 5000
        server_address = (ip, port)

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.connect(server_address)

        client_socket.sendto(data, server_address)
        print(f"Send data: {data.decode()}")

        client_socket.close()


def save_message(message):
    if pathlib.Path("storage/contact.json").is_file():
        with open("storage/contact.json", "r") as fh:
            contact_me = json.load(fh)
    with open("storage/contact.json", "w+") as fh:
        data_parse = urllib.parse.unquote_plus(message.decode())
        data_dict = {
            key: value for key, value in [el.split("=") for el in data_parse.split("&")]
        }
        dt = str(datetime.now())
        if "contact_me" in dir():
            contact_me[dt] = data_dict
        else:
            contact_me = {dt: data_dict}
        json.dump(contact_me, fh, indent=2)


def run_socket():
    ip = "127.0.0.1"
    port = 5000
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (ip, port)
    sock.bind(server_address)
    try:
        while True:
            data, address = sock.recvfrom(1024)
            print(data.decode())
            save_message(data)
            print(f"Received data: {data.decode()}")
    except KeyboardInterrupt:
        print("Destroy server")
    finally:
        sock.close()


def run(server_class=HTTPServer, handler_class=HttpHandler):
    sock_thread = Thread(target=run_socket, args=())
    sock_thread.start()
    server_address = ("", 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == "__main__":
    run()
