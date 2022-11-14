import socket
import urllib.parse

class HTTP:

    @classmethod
    def request(cls, host, resource, ip, port, extension):
        if extension != 'html' and extension != 'htm' and extension != '':
            request = "GET %s HTTP/1.1\r\nHost:%s\r\n\r\n" %(target_path,target_host)
            header  = "HEAD %s HTTP/1.1\r\nHost:%s\r\n\r\n" %(target_path,target_host)
        else:
            request = "GET / HTTP/1.1\r\nHost:%s\r\n\r\n" %target_host
            header = "HEAD / HTTP/1.1\r\nHost:%s\r\n\r\n" %target_host
        client = cls(host, resource)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp:
            tcp.connect((ip, port))

            client.send(tcp, request)
            client.receive(tcp, extension)

        return client


    @classmethod
    def getContentLength(cls, header):
        #Chay tung dong trong phan header (\r\n la xuong dong)
        for line in header.split(b'\r\n'):
            if content_length_field in line:
                return int(line[len(content_length_field):])
        return 0

    @classmethod
    def readData(cls, sock, endOfField, extension):
        data = bytes()
        chunk = bytes()
        length = 0
        try:
            while not endOfField(length, chunk):
                chunk = sock.recv(4096)
                if not chunk:
                    break
                if extension == 'html' or extension == 'htm':
                    data += chunk
                    length += len(chunk)
                    break
                else:
                    data += chunk
                    length += len(chunk)
                    print(chunk)
        except socket.timeout:
            pass
        return data
    
    @classmethod
    def seperateHeaderBody(cls, sock):
        #Tach header va body
        try:
            index = sock.index(EOHeader_delimiter)
        except:
            return (sock, bytes())
        else:
            index += len(EOHeader_delimiter)
            return (sock[:index], sock[index:])

    #Check if end of header/content -> use for endOfField in readData method
    def EOHeader(self, length, data):
        return b'\r\n\r\n' in data

    def EOContent(self, length, data):    
        return self.contentLength <= length

    def send(self, sock, request):
        sock.sendall(request.encode())

    def __init__(self, host, data):
        self.host = host
        self.data = data #
        self.header = bytes()
        self.contentLength = 0
        self.body = bytes()

    def receive(self, sock, extension):
        self.data = self.readData(sock, self.EOHeader, extension)
        self.header, self.body = self.seperateHeaderBody(self.data)
        self.contentLength = self.getContentLength(self.header)
        if extension != 'html' and extension != 'htm' and extension != '':
            self.body += self.readData(sock, self.EOContent, len(self.body))

        return (self.header, self.body)
        
def writeFile(message):
    if target_path == '':
        filename = 'index.html'
    else:
        filename = target_path.replace('/','_') + '.' + extName

    f = open(filename , "wb");


    f.write(message)
    print("\nWRITE SUCCESSFULLY!!\n")
    f.close()

if __name__ == "__main__":
    #Format
    FORMAT = "utf-8"

    #Define delimeter for "end of Header" and "Content-Length" 
    EOHeader_delimiter = b'\r\n\r\n'
    content_length_field = b'Content-Length:'

    #Create socket object
    target_port = 80 

    #Input from user
    print("Enter host address (eg. http://www.example.com/index.html)")
    urlInput = input('')
    print("Enter extension name (eg. html, pdf, doc...)")
    extName = input('')

    #Format the url using urllib
    # url = http://www.example.com/index.html
    url = urllib.parse.urlparse(urlInput)
    # host : www.example.com
    target_host = url.hostname
    # path : /index.html
    target_path = url.path
    #scheme : http
    target_scheme = url.scheme
    
    #Print info
    print('Host:%s\nPath:%s\nScheme:%s\n'% (target_host,target_path,target_scheme))
    
    #Send request and receive
    response = HTTP.request(target_host, target_path, target_host, target_port, extName)

    #Write to file from received response
    writeFile(response.body)


###TEST LINK
'''
http://example.com/
http://web.stanford.edu/class/cs224w/slides/01-intro.%20pdf
http://web.stanford.edu/dept/its/support/techtraining/techbriefing-media/Intro_Net_91407.ppt
http://www-net.cs.umass.edu/wireshark-labs/Wireshark_Intro_v8.1.docx
http://web.stanford.edu/class/cs231a/project.html
http://gaia.cs.umass.edu/wireshark-labs/alice.txt
'''


    






