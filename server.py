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
        #print ("Got a request of: %s\n" % self.data)

        #self.request.sendall("OK")
        path = self.data.split()[1]
        method_type = self.data.split()[0]
        if method_type != 'GET':                                 #only GET will be handled !
            status_code = "HTTP/1.1 405 Method not allowed\r\n"
            content_type = "Content-type: text/html\r\n\r\n"
            content = "<html><head></head><body>"+"<h1><center>HTTP/1.1 405 Method not allowed</center></h1></body></html>\n"
            self.request.sendall(status_code)
            self.request.sendall(content_type)
            self.request.sendall(content)
            return

        if path[-1] == '/':
            Path = os.getcwd()+"/www"+path+"index.html"
        else:
            Path = os.getcwd()+"/www"+path

        #print ("Path is %s \n"%Path) /home/tuxin/Desktop/CMPUT404/Assignment1/CMPUT404-WEB-SERVER/www/../../../../../../../../../../../../etc/group
        #print ("path is %s \n"%path) /../../../../../../../../../../../../etc/group
        #print ("Path is %s \n"%Path)
        if ( os.path.exists(Path) == False or "../" in Path or "/.." in Path): #add "../ for the serc check"
        	#print ("path is %s \n"%path)
        	header = "HTTP/1.1 404 Not Found\r\n Content-type: text/html\r\n"
        	file_content ="<html><head></head><body>"+"<h1><center>HTTP/1.1 404 Page Not Found!</center></h1></body></html>\n"
        	self.request.sendall(header + "\r\n" + file_content)
        	return

        read_file = os.path.abspath(Path)


        myfile = open(read_file, 'r') #serve file in www
        file_content = ""
        for i in myfile:
        	file_content +=i
        myfile.close()
        mime_type = Path.split('.')[1] #after the  . is the mime type
        header = "HTTP/1.1 200 OK\r\n" + "Content-type: text/%s\r\n" %mime_type
        self.request.sendall(header + "\r\n" + file_content)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
