import socket


   


def readChunk(response, f):
    #Đọc header thiếu (ban đầu 113) nên cộng thêm thành 357 ->đúng
    rep = bytes(response)
    TESTheader = b''

    TESTheader =  rep.split('\r\n\r\n')[0]

    
    print(len(TESTheader))

    response = client.recv(len(TESTheader))
    while True:
        response = client.recv(4096)  
        if len(response) == 0:
            break

        http_response = repr(response)
        http_response_len = len(http_response)
        print(http_response)
        f.write(response)
    f.close()

# input website name
#### code here
print("Enter host address (eg. www.example.com)\n")
target_host = input('')
print("Enter extension name (eg. html, pdf, doc...))\n")
extName = input('')


target_port = 80  # create a socket object 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

# connect the client 
client.connect((target_host,target_port))  


# send some data 
# request = "GET /index.html/ HTTP/1.1\r\nHost:%s\r\n\r\n" % target_host
request = "GET http://www-net.cs.umass.edu/wireshark-labs/Wireshark_Intro_v8.1.docx HTTP/1.1\r\nHost:%s\r\n\r\n" % target_host
head  = "HEAD http://www-net.cs.umass.edu/wireshark-labs/Wireshark_Intro_v8.1.docx HTTP/1.1\r\nHost:%s\r\n\r\n" % target_host


client.send(request.encode())  

# receive some data 
# tim so byte can receive trong nay content-length chunk transfer
# response = client.recv(4096)  




filename = target_host + '.' + extName
f = open(filename , "wb");
# f.write(response)
response = b''
readChunk(response, f)
print(head)
print(len(head))


client.close()