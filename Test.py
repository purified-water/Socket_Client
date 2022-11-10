import socket

def readChunk(response, f):
    while True:
        response = client.recv(4096)  
        if len(response) == 0:
            break
        f.write(response)

target_host = "www.web.stanford.edu" 

target_port = 80  # create a socket object 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

# connect the client 
client.connect((target_host,target_port))  

# send some data 
# request = "GET /index.html/ HTTP/1.1\r\nHost:%s\r\n\r\n" % target_host
request = "GET http://web.stanford.edu/class/cs224w/slides/01-intro.pdf HTTP/1.1\r\nHost:%s\r\n\r\n" % target_host
client.send(request.encode())  

# receive some data 
# tim so byte can receive trong nay content-length chunk transfer
# response = client.recv(4096)  




filename = target_host + '.pdf'
f = open(filename , "wb");
# f.write(response)
response = b''
readChunk(response, f)

http_response = repr(response)
http_response_len = len(http_response)



print(http_response)