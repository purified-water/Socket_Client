import socket
import urllib.parse


FORMAT = "utf-8"
#Define delimeter for "Content-Length"
EOHeader_delimiter = b'\r\n\r\n'
content_length_field = b'Content-Length:'
#Resquest function
#Print the request to terminal
def printTerminal(response):
    http_response = repr(response)
    http_response_len = len(http_response)
    print(http_response)

class HTTP:

    @classmethod
    def getContentLength(cls, header):
        #Chay tung dong trong phan header (\r\n la xuong dong)
        for line in header.split(b'\r\n'):
            if cls.content_length_field in line:
                return int(line[len(cls.content_length_field):])
        return 0

    @classmethod
    def readData(cls, sock, endOfField):
        data = bytes()
        chunk = bytes()
        length = 0
        try:
            while not endOfField(length, chunk):
                chunk = sock.recv(4096)
                if not chunk:
                    break
                else:
                    data += chunk
                    length += len(chunk)
        except socket.timeout:
            pass
        return data
    
    @classmethod
    def seperateHeaderBody(cls, sock):
        #Tach header va body
        wholeData = bytes(cls.readData(sock))

        cls.header =  wholeData.split('\r\n\r\n')[0]
        cls.body = wholeData.split('\r\n\r\n')[1]
        return(cls.header, cls.body)

    #Check if end of header/content -> use for endOfField in readData method
    def EOHeader(self, length, data):
        return b'\r\n\r\n' in data

    def EOContent(self, length, data):
        '''
        TASKs to do: 
        + finish eocontent function -> this leads to condition function in readData function
        + condition in readData is a function passed as an argument
        '''
        
        return self.contentLength <= length

        
    



    def __init__(self, host, data):
        self.host = host
        self.data = data #
        self.header = bytes()
        self.contentLength = 0
        self.body = bytes()

    def receive(self, sock):
        self.data = self.readData(sock)
        self.header, self.body = self.seperateHeaderBody(sock)
        self.contentLength = self.getContentLength(header)
        


# def receive(response, lenHead, f):
#     response = client.recv(lenHead)
#     while True:
#         response = client.recv(4096)  
#         if len(response) == 0:
#             break

#         http_response = repr(response)
#         http_response_len = len(http_response)
#         print(http_response)
#         f.write(response)
#     f.close()





# input website name
#### code here
'''
print("Enter host address (eg. www.example.com)\n")
target_host = input('')
print("Enter extension name (eg. html, pdf, doc...))\n")
extName = input('')
'''

print("Enter host address (eg. www.example.com)\n")
urlInput = input('')
print("Enter extension name (eg. html, pdf, doc...))\n")
extName = input('')

# url = http://www.example.com/index.html
url = urllib.parse.urlparse(urlInput)

# host : www.example.com
target_host = url.hostname

# path : /index.html
target_path = url.path

#scheme : http
target_scheme = url.scheme


target_port = 80  # create a socket object 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

# connect the client 
client.connect((target_host,target_port))  


# send some data 
# request = "GET /index.html/ HTTP/1.1\r\nHost:%s\r\n\r\n" % target_host


# request = "GET http://www-net.cs.umass.edu/wireshark-labs/Wireshark_Intro_v8.1.docx HTTP/1.1\r\nHost:%s\r\n\r\n" % target_host
# header  = "HEAD http://www-net.cs.umass.edu/wireshark-labs/Wireshark_Intro_v8.1.docx HTTP/1.1\r\nHost:%s\r\n\r\n" % target_host


request = "GET %s HTTP/1.1\r\nHost:%s\r\n\r\n" %(target_path,target_host)
header  = "HEAD %s HTTP/1.1\r\nHost:%s\r\n\r\n" %(target_path,target_host)


client.send(request.encode(FORMAT))  

# receive some data 
# tim so byte can receive trong nay content-length chunk transfer
# response = client.recv(4096)  
#Open file with corresponding tyoe name


# filename = target_host + '.' + extName
filename = target_path.replace('/','_')


f = open(filename , "wb");

# f.write(response)
response = b''

#Call receive function
receive(response, len(header), f)


print(header)
print(len(header))


client.close()




