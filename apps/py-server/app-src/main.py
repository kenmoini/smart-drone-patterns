from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl, os

HOST = os.environ.get("PY_HTTP_SERVER_HOST", "0.0.0.0")
PORT = os.environ.get("PY_HTTP_SERVER_PORT", 7999)
DIRECTORY = os.environ.get("PY_HTTP_SERVER_DIRECTORY", "./")
tlsCert = os.environ.get("PY_HTTP_SERVER_TLS_CERT", "")
tlsKey = os.environ.get("PY_HTTP_SERVER_TLS_KEY", "")


if __name__ == "__main__":
    try:
        os.chdir(DIRECTORY)

        httpd = HTTPServer((HOST, int(PORT)), SimpleHTTPRequestHandler)

        if tlsCert != "" and tlsKey != "":
            print("Starting Simple HTTP Server on port " + str(PORT) + " and host " + str(HOST) + " with TLS cert " + str(tlsCert) + " and TLS key " + str(tlsKey))
            httpd.socket = ssl.wrap_socket(httpd.socket, 
                    keyfile=tlsKey, certfile=tlsCert, server_side=True)

        else:
            print("Starting Simple HTTP Server on port " + str(PORT) + " and host " + str(HOST))

        httpd.serve_forever()

    except KeyboardInterrupt:
        pass
        httpd.server_close()