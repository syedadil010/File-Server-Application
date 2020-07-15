# HTTP-File-Server-Application
A HTTP server application that supports File Server.

It has the following additional features:

**Error Handling** : prevents the clients to read/write any file outside the file server working directory

**Secure Access** : each exception on the server side is translated to an appropriate status
code and human readable messages.

**Multi-Requests Support** : the server can handle multiple requests simultaneously.

- Two clients are writing to the same file.
 - One client is reading, while another is writing to the same file.
 - Two clients are reading the same file.

# Usage

httpfs is a simple file server.
**usage**: httpfs [-v] [-p PORT] [-d PATH-TO-DIR]

 -v Prints debugging messages.
 
 -p Specifies the port number that the server will listen and serve at.
 Default is 8080.
 
 -d Specifies the directory that the server will use to read/write requested files. Default is the current directory when launching the application
