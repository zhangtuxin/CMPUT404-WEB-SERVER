#  coding: utf-8
import SocketServer,os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()


        print ("Got a request of: %s\n" % self.data)

        #self.request.sendall("OK")


        path = self.data.split()[1]
        method_type = self.data.split()[0]
        if method_type != 'GET':
            status_code = "HTTP/1.1 405 Method not allowed\r\n"
            content = "Content-type: text/html\n\n"+\
			"<html><head></head><body>"+\
			"<h1><center>HTTP/1.1 405 Method not allowed</center></h1></body></html>\n"
            self.request.sendall(status_code)
            self.request.sendall(content)
            return

        # check the path to get full path to files
        if path[-1] == '/':
            fullPath = os.getcwd() + "/www" + path + "index.html"
        # this elif is for security test
        elif "../" in path:
            header = "HTTP/1.1 404 Not Found\n"
            fileStr = "Content-type: text/html\n\n"+\
			"<html><head></head><body>"+\
			"<h1><center>HTTP/1.1 404 Page Not Found</center></h1></body></html>\n"
            self.request.sendall(header + "\r\n" + fileStr)
            return
        else:
            fullPath = os.getcwd() + "/www" + path

        # get the local path
        localPath = os.path.normpath(fullPath)

        # update fileStr and header
        try:
            # read the file and update fileStr
            theFile = open(localPath, 'r')
            fileStr = theFile.read()
            theFile.close()

            # update header
            docType = fullPath.split('.')[-1]
            header = "HTTP/1.1 200 OK\r\n" + \
                     "Content-Type: text/" + docType + ";charset=UTF-8\r\n"

        # Raised IOError when the built-in open() function fails
        except IOError:
            header = "HTTP/1.1 404 Not Found\n"
            fileStr ="Content-type: text/html\n\n"+\
			"<html><head></head><body>"+\
			"<h1><center>HTTP/1.1 404 Page not found</center></h1></body></html>\n"

        # display the page
        self.request.sendall(header + "\r\n" + fileStr)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
