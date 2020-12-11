import sys, os, platform
from http.server import HTTPServer, BaseHTTPRequestHandler

import lib.systems.windows as windows
import lib.systems.linux as linux


lockdown = None
if platform.system() == 'Windows':
    lockdown = windows.WindowsLockdown()
elif platform.system() == 'Linux':
    lockdown = linux.LinuxLockdown()


class S(BaseHTTPRequestHandler):
        

    def do_GET(self):
        if 'remove_restricted=true' in self.path:
            lockdown.remove_restricted_files()
        try:
            print(self.path)
            path = self.path.split('?')[0]
            if path.endswith('.html'):
                f = open(os.getcwd() + path)

                self.send_response(200)

                self.send_header('Content-type', 'text-html')
                self.end_headers()

                self.wfile.write(f.read().encode('utf-8'))
                f.close()
                return
        except IOError:
            self.send_error(404, 'file not found')


def run():
    httpd = HTTPServer(('localhost', 8000), S)
    httpd.serve_forever()

run()
