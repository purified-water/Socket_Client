import socket

print("Input host addr ( www.example.com ) : ")
target_host = 'www.example.com'
content_length = b''
target_port = 80  


# create a socket object 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
# connect the client 
client.connect((target_host,target_port))  
# send some data 
request = "GET / HTTP/1.1\r\nHost:%s\r\n\r\n" % target_host
client.send(request.encode())  



filename = '%s_index.html' % target_host
f = open(filename , "wb")
# receive some data 
# tim so byte can receive trong nay content-length chunk transfer
response = b''
while True:
    chunk = client.recv(4096)  
    if len(response) == 0:
        break
    response = response + chunk

f.write(response)

http_response = repr(response)
http_response_len = len(http_response)

#Close client
client.close()


print(http_response)

#display the response
# gh_imgui.text("[RECV] - length: %d" % http_response_len)
# gh_imgui.text_wrapped(http_response)