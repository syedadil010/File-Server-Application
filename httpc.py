import socket
import argparse
import sys
import threading
import time
from threading import Thread

def getheaders(a):
    headers = {}
    headstr=''
    for i, v0 in enumerate(a):
        if v0 is '-' and a[i + 1] is ('h' or 'H') and a[i+2] is ' ':
            i = i + 1
            isKey = True
            key = ""
            value = ""
            for v1 in a[i + 2:]:
                iscolon = False
                if v1 is ' ':
                    break
                if v1 is ':':
                    isKey = False
                    iscolon = True
                if isKey:
                    key = key + v1
                if not isKey and not iscolon:
                    value = value + v1
            if(key.__contains__('\"')):
                key=key.strip('\"')
            if(value.__contains__('\"')):
                value=value.strip('\"')
            headers[key] = value
    return headers
def createstr(headers):
    headstr=''
    len1=len(headers.keys())
    i=1
    for a in headers.keys():
        if(i==len1):
            headstr = headstr + a + ':' + headers[a]
        else:
            headstr=headstr+a+':'+headers[a]+'\r\n'
        i=i+1
    return headstr

def run_client(host, port,inputString):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect((host, port))
        print("Type any thing then ENTER. Press Ctrl+C to terminate")
#       while True:
           # line = sys.stdin.readline(1024)
        headers = createstr(getheaders(inputString))
        inputList1 = inputString.rsplit(" ")
        if("POST" in inputString):
            inputListD = inputString.rsplit("-d")
            inputListInlineData = inputListD[1].split('"')
        if("POST" in inputString and "-d" in inputString and "-h" in inputString):
          line = inputList1[1]+"*_#"+ inputListInlineData[1]+"*_#"+headers
        elif("POST" in inputString and "-d" not in inputString and "-h" in inputString):
          line = inputList1[1]+"*_#"+headers
        elif("POST" in inputString and "-d" in inputString and "-h" not in inputString):
          line = inputList1[1]+"*_#"+ inputListInlineData[1]
        elif("GET" in inputString and "-h" not in inputString):
          line = inputList1[1]+"*_#"+ ""
        elif("GET" in inputString and "-h" in inputString):
          line = inputList1[1] +"*_#"+headers
        else:
            print("Please Enter a Valid Request.")
        
        if("overwrite=true" in inputString):
           line = line + "*_#" + "overwrite=true"
        elif("overwrite=false" in inputString):
           line = line + "*_#" + "overwrite=false"
        print(line)
        request = line.encode("utf-8")
        conn.sendall(request)
        # MSG_WAITALL waits for full request or error
        response = conn.recv(10000)
        print("Server Replied: ", response.decode("utf-8"))
    finally:
        conn.close()

# Usage: python echoclient.py --host host --port port
print("Press 1 for Running the code Normally.\r\n""Press 2 for Running Multithreaded Test Cases.")
inputMulti = input()
if(inputMulti == "1"):
    inputString = input()
    inputList1 = inputString.rsplit(" ")
    hostndPort = inputList1[2].rsplit("/")
    host = hostndPort[0]
    port = hostndPort[1]
    headers={}
    if("POST" in inputString):      
      inputList2 = inputString.rsplit('"')
    #  print(inputList2)
      PostAndFile = inputList1[1].rsplit("/")
      fileName = PostAndFile[1]
      if("-d" in inputString and "-h" in inputString):
         inputListD = inputString.rsplit("-d")
         inputListInlineData = inputListD[1].split('"') 
         headers=createstr(getheaders(inputString))
      elif("-d" in inputString and "-h" not in inputString):
           inputListD = inputString.rsplit("-d")
           inputListInlineData = inputListD[1].split('"') 
    #       print(inputListInlineData)
    #       print(inputListInlineData[1])
      elif("-d" not in inputString and "-h" in inputString):
          headers=createstr(getheaders(inputString))
          print(headers)
      else:
          print("Nothing!!")
    elif("GET" in inputString):
      print(inputList1)
      if("-h" in inputString):
        headers=createstr(getheaders(inputString))
        print(headers)          
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="server host", default="localhost")
    parser.add_argument("--port", help="server port", type=int, default=10000)
    args = parser.parse_args()
    run_client(host,int(port),inputString)
elif(inputMulti == "2"):
    
    threads = input("Enter no. of threads: ")
    print("Press 1 for making Multiple clients are 'Reading' the same file\r\nPress 2 for making Multiple clients are 'Writing' the same file\r\n\r\nPress 3 for making Multiple clients are 'Writing' and Reading at the same time\r\n")
    choice = input()
    if(choice=="3"):
        getthreads=int(input("Enter number of GET threads: "))
        getthreadlist=[]
        for a in range(0,getthreads):
            temp=input("Enter your GET command: ")
            getthreadlist.append(temp)
        postthreads = int(input("Enter number of POST threads: "))
        postthreadlist = []
        for a in range(postthreads):
            temp=input("Enter your POSTcommand: ")
            getthreadlist.append(temp)
        # inputString = 'httpc GET/foo localhost/10000 -h Content-Type:Application/html -h Content-Disposition:inline'
        # inputStringpost ='httpc POST/foo localhost/10000 -d "Anything you would like to print here" overwrite=true -h Content-Type:Application/html'
        host = 'localhost'
        port = 8080
        for a in getthreadlist:
            Thread(target=run_client, args=(host, port,a)).start()
    elif(choice == "1"):
        inputString = 'httpc GET/choo localhost/10000 -h Content-Type:Application/html -h Content-Disposition:inline'
        inputList1 = inputString.rsplit(" ")
        host = 'localhost'
        port = 8080
        headers = createstr(getheaders(inputString))
        for i in range(0, int(threads)):
            Thread(target=run_client, args=(host, port, inputString)).start()
    elif(choice == "2"):
        inputString = 'httpc POST/goo localhost/10000 -d "Anything you would like to print here" overwrite=true -h Content-Type:Application/html'
        inputList1 = inputString.rsplit(" ")
        inputListD = inputString.rsplit("-d")
        inputListInlineData = inputListD[1].split('"')
        host = 'localhost'
        port = 8080
        headers = createstr(getheaders(inputString))
        for i in range(0, int(threads)):
            Thread(target=run_client, args=(host, port, inputString)).start()
    else:
        print("Incorrect choice")

