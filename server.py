#!/usr/bin/env python3
"""
smurf - a simple markdown surfer

Authors:
    Mitesh Shah <mitesh@oxal.org>

Repository:
    https://github.com/oxalorg/smurf
"""
from http.server import SimpleHTTPRequestHandler, HTTPServer
from http import HTTPStatus
import shutil
import posixpath
import os
import argparse
import sys
import urllib
import html
import io
import subprocess
from string import Template


class SmurfRequestHandler(SimpleHTTPRequestHandler):
    md_ext = (".html",)

    def send_head(self):
        # Logic
        # check if a file exists on actual path
        # if so serve the static file
        # if not
        #   then check if trailing slash exists
        # if not then redirect
        # if it does
        #   then find the following path 
        #   path.html path/index.html
        path = self.translate_path(self.path)
        f = None
        parts = urllib.parse.urlsplit(self.path)
        print(parts)
        print(parts.path[1:-1])
        if os.path.isfile(path):
            # serve the file
            pass
        elif os.path.isfile(parts.path[1:-1] + ".html"):
            # server the file
            path = parts.path[1:-1] + ".html"
        elif not parts.path.endswith('/'):
            # redirect browser - doing basically what apache does
            self.send_response(HTTPStatus.MOVED_PERMANENTLY)
            new_parts = (parts[0], parts[1], parts[2] + '/', parts[3],
                         parts[4])
            new_url = urllib.parse.urlunsplit(new_parts)
            self.send_header("Location", new_url)
            self.end_headers()
            return None
        elif os.path.isdir(path):
            for index in ["index" + ext for ext in self.md_ext]:
                # if an html file named "index" or last path url is available in
                # a directory, display that instead of the default
                # directory listing
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
                # if os.path.exists()
            else:
                return
                # return self.list_directory(path)
        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return None
        base, ext = posixpath.splitext(path)
        ctype = self.guess_type(path)
        try:
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", ctype)
            #fs = os.fstat(f.fileno())
            #self.send_header("Content-Length", str(fs[6]))
            #self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.end_headers()
            f.seek(0)
            return f
        except:
            f.close()
            raise

    def list_directory(self, path):
        try:
            list = os.listdir(path)
        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND,
                            "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())

        try:
            displaypath = urllib.parse.unquote(
                self.path, errors='surrogatepass')
        except UnicodeDecodeError:
            displaypath = urllib.parse.unquote(path)
        displaypath = html.escape(displaypath, quote=False)
        enc = sys.getfilesystemencoding()
        title = 'Directory listing for %s' % displaypath

        # form the content response i.e. index of the directory
        r = []
        r.append('<ul>')
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            r.append('<li><a href="%s">%s</a></li>' % (urllib.parse.quote(
                linkname, errors='surrogatepass'), html.escape(
                    displayname, quote=False)))
        r.append('</ul>')
        r = BASE_TEMPLATE.substitute(content='\n'.join(r), css=CSS, title=title)
        encoded = r.encode(enc, 'surrogateescape')

        # transform the encoded content to a file like object
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return f


def cli():
    parser = argparse.ArgumentParser(
        description="a simple markdown surfer",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('dir', help="folder to serve", nargs='?', default=os.getcwd())
    args = parser.parse_args()

    if not os.path.isdir(args.dir):
        print(args.dir, " is not a valid directory")
        sys.exit(1)

    os.chdir(args.dir)


def main():
    cli()
    server_address = ('0.0.0.0', 3434)
    httpd = HTTPServer(server_address, SmurfRequestHandler)
    print("Starting server at http://localhost:3434")
    try:
        httpd.serve_forever()
    except:
        httpd.shutdown()
        httpd.server_close()


if __name__ == '__main__':
    main()

