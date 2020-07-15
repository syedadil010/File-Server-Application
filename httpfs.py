import socket
import os
from os import path
from threading import Lock
import shutil
# Create a TCP/IP socket
verbose=False
inputString1 = input()
inputString = inputString1.replace("]","")
#print(inputList)
inputList = inputString.rsplit(" ")
indexPort = [i for i, elem in enumerate(inputList) if '-p' in elem]
indexDirectory = [i for i, elem in enumerate(inputList) if '-d' in elem] 
#print(indexPort)
if("-v" in inputString):
  verbose=True
  print("Debugging Messages: " +"\n \n"
        "200 OK: Successful GET Request."+"\n"
        "201 OK: Successful POST Request."+"\n"
        "400 Bad Request: A malformed request."+"\n"
        "403 Forbidden: Server has denied access to the resource."+"\n"
        "404 Not Found: Server cannot retrieve the page that was requested."+"\n"
        )
  
#port = 10000
#path = 'C:\\Users\\Nikunj\\Directory2'
if("-p" in inputString):
  port = inputList[indexPort[0]+1]
else:
  port = 10000
if("-d" in inputString):
  path1 = inputList[indexDirectory[0]+1]
else:
  path1 = 'C:\\Users\\syeda\\PycharmProjects\\CNA3\\python\\dir'

#print(port)
#print(path1)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('localhost', int(port))
print ('starting up on %s port %s' % server_address)
print("Directory= ", path1)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print ('waiting for a connection\n')
    connection, client_address = sock.accept()
    try:
        print ( 'connection from', client_address)
        # Receive the data in small chunks and retransmit it
        while True:
          data = connection.recv(10000)
          if(verbose==True):
            print ('received "%s"' % data)
          d=data.decode('UTF-8')
#            print(d)
          lock = Lock()
          lock.acquire()
          dSplit = d.rsplit("*_#")
          dSplit2 = dSplit[0].rsplit("/")
          ffile=''
          content=''
          if data :
              print(dSplit[0].count("/")>=1)
              if(dSplit[0].count("\\")>=1 or dSplit[0].count(".")>1):
                content = "HTTP/1.0 403 Forbidden\r\n Server has denied access to the resource."
                if(verbose==True):
                    print(content)
                print('sending List of data back to the client')
                connection.sendall(bytes(content, 'UTF-8'))
              else:
                if("." in dSplit2[1] and "Accept" not in d and "Content-Type" not in d):
                 f1 = (path1.replace('\\\\','\\') + "\\"+dSplit2[1]).replace("'","") 
                elif("." not in dSplit2[1] and "Accept" in d and "Content-Type" not in d):
                 AcceptIndex = [i for i, s in enumerate(dSplit) if 'Accept' in s]
                 AcceptList0 = dSplit[AcceptIndex[0]]
                 Accept = AcceptList0.rsplit(":")
                 A = ""
                 if("TEXT" in Accept[1]):
                    A = "txt"
                 elif("HTML" in Accept[1]):
                    A = "html"
                 elif("XML" in Accept[1]):
                    A = "xml"
                 elif("JSON" in Accept[1]):
                    A = "json" 
                 f1 = (path1.replace('\\\\','\\') + "\\"+dSplit2[1]).replace("'","") +"."+A
                elif("." not in dSplit2[1] and "Accept" not in d and "Content-Type" in d):
                  conTypeIndex = [i for i, s in enumerate(dSplit) if 'Content-Type' in s]
                  ContentTypeList0 = dSplit[conTypeIndex[0]]
                  contentType = ContentTypeList0.rsplit("/")
                  cType = ""
                  if("plain" in contentType[1]):
                      cType = "txt"
                  elif("html" in contentType[1]):
                      cType = "html"
                  elif("xml" in contentType[1]):
                      cType = "xml"
                  elif("json" in contentType[1]):
                      cType = "json"
                  f1 = (path1.replace('\\\\','\\') + "\\"+dSplit2[1]).replace("'","") +"."+cType 
#                lock.acquire()
                if(dSplit2[1] == "" and "GET" in dSplit2[0] and 'Accept' not in d and 'Content-Type' not in d):                  
                    files = []
#                    print(files)
                    for r, d, f in os.walk(path1):
                        for file in f:
                            #if '.txt' in file:
                                files.append(os.path.join(file))
                    for f in files:
                        strffile = str(len(ffile))
                        ffile=ffile+"\n"+f
                        if(ffile==""):
                           content="HTTP/1.0 404 Not Found\r\n No files are found in the directory."
                        else:
                           content= "HTTP/1.0 200 OK \r\n Content-Length: "+strffile+"\r\n" + ffile
                    if (verbose == True):
                        print(content)
                    print ('sending List of data back to the client')
                    connection.sendall(bytes(content, 'UTF-8'))
                elif(dSplit2[1] == "" and "GET" in dSplit2[0] and 'Accept' in d):  
                    print("Inside GET/ and Accept in d")
                    files = []
                    AcceptIndex = [i for i, s in enumerate(dSplit) if 'Accept' in s]
#                    print(AcceptIndex)
                    AcceptList0 = dSplit[AcceptIndex[0]]
#                    print(AcceptList0)
                    Accept = AcceptList0.rsplit(":")
#                    print(Accept)
                    A = ""
                    if("TEXT" in Accept[1]):
                       A = ".txt"
                    elif("HTML" in Accept[1]):
                       A = ".html"
                    elif("XML" in Accept[1]):
                       A = ".xml"
                    elif("JSON" in Accept[1]):
                       A = ".json"
                    for r, d, f in os.walk(path1):
                        for file in f:
                            if A in file:
                                files.append(os.path.join(file))

                    for f in files:
                        ffile=ffile+"\n"+f
                        strffile = str(len(ffile))
                        print(ffile)
                    if(ffile==""):
                       content="HTTP/1.0 404 Not Found\r\n No files are found in the directory."
                    else:
                       content= " \r\n HTTP/1.0 200 OK \r\n Content-Length: " +strffile+"\r\n Content-Type: Application/"+Accept[1]+"\r\n" +ffile   
                    print ('sending List of data back to the client')
                    connection.sendall(bytes(content, 'UTF-8'))
                elif(dSplit2[1] == "" and "GET" in dSplit2[0] and 'Content-Type' in d):        
                    files = []
                    conTypeIndex = [i for i, s in enumerate(dSplit) if 'Content-Type' in s]
                    ContentTypeList0 = dSplit[conTypeIndex[0]]
                    contentType = ContentTypeList0.rsplit("/")
                    cType = ""
                    if("plain" in contentType[1]):
                        cType = ".txt"
                    elif("html" in contentType[1]):
                        cType = ".html"
                    elif("xml" in contentType[1]):
                        cType = ".xml"
                    elif("json" in contentType[1]):
                        cType = ".json"
                    for r, d, f in os.walk(path1):
                          for file in f:
                              if cType in file:
                                  files.append(os.path.join(file))

                    for f in files:
                        ffile=ffile+"\n"+f
                        strffile = str(len(ffile))
                    if(ffile==""):
                        content="HTTP/1.0 404 Not Found\r\n No files are found in the directory."
                    else:
                        content= " \r\n HTTP/1.0 200 OK \r\n Content-Length: " +strffile+"\r\n Content-Type: Application/"+contentType[1]+"\r\n" +ffile   
                    print ('sending List of data back to the client')
                    connection.sendall(bytes(content, 'UTF-8')) 
                elif(dSplit2[1] != "" and "GET" in dSplit2[0] and path.exists(f1) == False):
                    content="HTTP/1.0 404 Not Found\r\n No files are found in the directory." 
                    print ('sending data back to the client')
                    connection.sendall(bytes(content, 'UTF-8')) 
                elif(dSplit2[1] != "" and "GET" in dSplit2[0] and path.exists(f1) == True):
                  if("."in dSplit2[1]):
                    dSplit3 = dSplit2[1].rsplit(".")
                    f1 = (path1.replace('\\\\','\\') + "\\"+dSplit2[1]).replace("'","")
                    f2=open(f1, "r")
                    f = f2.read()
                    strffile = str(len(f))
                    content =" \r\n HTTP/1.0 200 OK \r\n Content-Length: " +strffile+"\r\n Content-Type: Application/"+dSplit3[1]+"\r\n" +f
                  elif("." not in dSplit2[1] and 'Content-Type' in d):
                    conTypeIndex = [i for i, s in enumerate(dSplit) if 'Content-Type' in s]
                    ContentTypeList0 = dSplit[conTypeIndex[0]]
                    contentType = ContentTypeList0.rsplit("/")
                    cType = ""
                    if("plain" in contentType[1]):
                       cType = "txt"
                    elif("html" in contentType[1]):
                       cType = "html"
                    elif("xml" in contentType[1]):
                       cType = "xml"
                    elif("json" in contentType[1]):
                       cType = "json"
                    f1 = (path1.replace('\\\\','\\') + "\\"+dSplit2[1]).replace("'","") + "." + cType.replace("\r\n","")
                    f2=open(f1, "r")
                    f = f2.read()
                    strffile = str(len(f))
                    content =" \r\n HTTP/1.0 200 OK \r\n Content-Length: " +strffile+"\r\n Content-Type: Application/"+contentType[1]+"\r\n" +f
                  elif("." not in dSplit2[1] and 'Accept' in d):
                    AcceptIndex = [i for i, s in enumerate(dSplit) if 'Accept' in s]
                    AcceptList0 = dSplit[AcceptIndex[0]]
                    Accept = AcceptList0.rsplit(":")
                    A = ""
                    if("TEXT" in Accept[1]):
                       A = "txt"
                    elif("HTML" in Accept[1]):
                       A = "html"
                    elif("XML" in Accept[1]):
                       A = "xml"
                    elif("JSON" in Accept[1]):
                       A = "json"
                    f1 = (path1.replace('\\\\','\\') + "\\"+dSplit2[1]).replace("'","") + "." + A.replace("\r\n","")
                    f2=open(f1, "r")
                    f = f2.read()
                    strffile = str(len(f))
                    content =" \r\n HTTP/1.0 200 OK \r\n Content-Length: " +strffile+"\r\n Content-Type: Application/"+Accept[1]+"\r\n"
                  if(verbose==True):
                      print(content)
                  print ('sending data back to the client')
                  if("Content-Disposition" in d and "inline" in d):
#                    content = content + "\r\nContent-Disposition: inline \r\n"+f
                    connection.sendall(bytes(content, 'UTF-8'))
                  elif("Content-Disposition" in d and "attachment" in d and "filename" not in d):
                    shutil.copy(f1,"C:\\Users\\syeda\\Downloads")
                    
                    content = content + "\r\n File Downloaded Successfully!"
                    connection.sendall(bytes(content, 'UTF-8'))
                  elif("Content-Disposition" in d and "attachment" in d and "filename" in d):
                    attachmentFileName = d.rsplit('filename=')
                    newLink = "C:\\Users\\syeda\\Downloads"+"\\"+attachmentFileName[1].replace('"','')
#                    print(newLink)
                    shutil.copy(f1,newLink)
                    content = content + "\r\nFile Downloaded Successfully with name "+ attachmentFileName[1].replace('"','')
                    connection.sendall(bytes(content, 'UTF-8'))
                  else:
                    connection.sendall(bytes(f1+content, 'UTF-8'))
#                lock.release
#                lock.acquire()
                if("POST" in d):
                  dSplit = d.rsplit("*_#")
                  dSplit2 = dSplit[0].rsplit("/")
                  dSplit3 = dSplit2[1].rsplit(".")
                  if("."in dSplit2[1]):
                    f1 = (path1.replace('\\\\','\\')+"\\"+dSplit2[1]).replace("'","")
#                    print(f1)
                    if(path.exists(f1) == True and ("overwrite=true" in d or "overwrite" not in d)):
                      f=open(f1, "w+")
                      f.write(dSplit[1])
                      f.close() 
                      strffile = str(len(dSplit[1]))
                      content = " \r\n HTTP/1.0 201 OK \r\n Content-Length: " +strffile+"\r\n Content-Type: Application/"+dSplit3[1]+"\r\nFile created Successfully"
                    elif(path.exists(f1) == True and "overwrite=false" in d):
                      content = "File already exists and You chose not to Overwrite."
                    elif(path.exists(f1) == False):
                      f=open(f1, "w+")
                      f.write(dSplit[1])
                      f.close()
                      strffile = str(len(dSplit[1]))
                      content = " \r\n HTTP/1.0 201 OK \r\n Content-Length: " +strffile+"\r\n Content-Type: Application/"+dSplit3[1]+"\r\nFile created Successfully"
                    if(verbose==True):
                        print(content)
                    print ('sending data back to the client')
                    connection.sendall(bytes(content, 'UTF-8'))
                  if("." not in dSplit2[1] and 'Content-Type' in d):
                    conTypeIndex = [i for i, s in enumerate(dSplit) if 'Content-Type' in s]
#                    print(conTypeIndex)
                    ContentTypeList0 = dSplit[conTypeIndex[0]]
#                    print(ContentTypeList0)
                    contentType = ContentTypeList0.rsplit("/")
#                    print(contentType)
                    cType = ""
                    if("plain" in contentType[1]):
                       cType = "txt"
                    elif("html" in contentType[1]):
                       cType = "html"
                    elif("xml" in contentType[1]):
                       cType = "xml"
                    elif("json" in contentType[1]):
                       cType = "json"
                    f1 = (path1.replace('\\\\','\\')+"\\"+dSplit2[1]).replace("'","")+"."+cType
#                    print(f1)
                    if(path.exists(f1) == True and ("overwrite=true" in d or "overwrite" not in d)):
                      f=open(f1, "w+")
                      f.write(dSplit[1])
                      f.close() 
                      strffile = str(len(dSplit[1]))
                      content = " \r\n HTTP/1.0 201 OK \r\n Content-Length: " +strffile+"\r\n Content-Type: Application/"+contentType[1]+"\r\nFile created Successfully"
                    elif(path.exists(f1) == True and "overwrite=false" in d):
#                      print("Inside ELIF: ")
                      content = "File already exists and You chose not to Overwrite."
                    elif(path.exists(f1) == False):
                      f=open(f1, "w+")
                      f.write(dSplit[1])
                      f.close() 
                      strffile = str(len(dSplit[1]))
                      content = " \r\n HTTP/1.0 201 OK \r\n Content-Length: " +strffile+"\r\n Content-Type: Application/"+contentType[1]+"\r\nFile created Successfully"
                    if(verbose==True):
                        print(content)
                    print ('sending data back to the client')
                    connection.sendall(bytes(content, 'UTF-8'))
                  if("." not in dSplit2[1] and 'Accept' in d):
                    AcceptIndex = [i for i, s in enumerate(dSplit) if 'Accept' in s]
#                    print(AcceptIndex)
                    AcceptList0 = dSplit[AcceptIndex[0]]
#                    print(AcceptList0)
                    Accept = AcceptList0.rsplit(":")
#                    print(Accept)
                    A = ""
                    if("TEXT" in Accept[1]):
                       A = "txt"
                    elif("HTML" in Accept[1]):
                       A = "html"
                    elif("XML" in Accept[1]):
                       A = "xml"
                    elif("JSON" in Accept[1]):
                       cType = "json"
                    f1 = (path1.replace('\\\\','\\')+"\\"+dSplit2[1]).replace("'","")+"."+A
#                    print(f1)
                    if(path.exists(f1) == True and ("overwrite=true" in d or "overwrite" not in d)):
                      f=open(f1, "w+")
                      f.write(dSplit[1])
                      f.close()    
                      strffile = str(len(dSplit[1]))
                      content = " \r\n HTTP/1.0 201 OK \r\n Content-Length: " +strffile+"\r\n Content-Type: Application/"+Accept[1]+"\r\nFile created Successfully"
                    elif(path.exists(f1) == True and "overwrite=false" in d):
#                      print("Inside ELIF: ")
                      content = "File already exists and You chose not to Overwrite."
                    elif(path.exists(f1) == False):
                      f=open(f1, "w+")
                      f.write(dSplit[1])
                      f.close() 
                      strffile = str(len(dSplit[1]))
                      content = " \r\n HTTP/1.0 201 OK \r\n Content-Length: " +strffile+"\r\n Content-Type: Application/"+Accept[1]+"\r\nFile created Successfully"
                    if(verbose==True):
                        print(content)
                    print ('sending data back to the client')
                    connection.sendall(bytes(content, 'UTF-8'))
          else:
                break
          lock.release()
            
    finally:
        # Clean up the connection
        
        connection.close()