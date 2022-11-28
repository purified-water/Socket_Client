import concurrent.futures
import urllib.request
import socket


def addHTTP(urlInput):
    scheme = "http://"
    if urlInput.find(scheme) == -1:
        urlInput = scheme + urlInput
    return urlInput

def checkUrl(urlInput):
    #Split space character (multi connections)
    listUrlInput = urlInput.split(' ')

    if len(listUrlInput) > 1:
        return 4 #This return option multi connections
    else:
        #Add http header if missing
        urlInput = addHTTP(urlInput)
        #Parse the link into path and host
        urlParse = urllib.parse.urlparse(urlInput)
        #Initialize path
        path = urlParse.path

        #Define html
        if path == '' or path == '/index.html' or path == '/index.htm' or path == '/':
            return 1 

        # define folder
        elif path[-1] == '/':
            return 3 #Return folder request

        # define extension file
        elif path.find('.'):
            return 2 #Return other extension option
        '''
        Them truong hop cac file ext khac
        Them truong hop khong hop le
        '''
        return 0

def getLink(html):
    listLink = re.findall('"([^"]*)"', html)
    return listLink

def checkSTR(listLink):
    checkedList = []
    for i in listLink:
        if (i.find('.pdf') != -1) or (i.find('.doc') != -1) or (i.find('.txt') != -1) or (i.find('.ppt') != -1):
            checkedList.append(i)
    print(checkedList)
    return checkedList
#Case input link is html/htm file
def processHTML(urlInput):

    # format url
    url = urllib.parse.urlparse(urlInput)

    target_host = url.hostname
    target_path = url.path
    target_scheme = url.scheme
    #print in terminal link
    print('Host:%s\nPath:%s\nScheme:%s\n' %
          (target_host, target_path, target_scheme))

    # initialize port
    target_port = 80

    # create socket obj TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to host server
    client.connect((target_host, target_port))

    # create request to host server
    request = "GET / HTTP/1.1\r\nHost:%s\r\n\r\n" % (target_host)

    # send request
    client.sendall(request.encode())

    # initialized file name
    filename = str(target_host)
    listPart = filename.split('.')

    #Case if link has "www" then omit "www"
    if listPart[0] == 'www':
        filename = listPart[1] + '.html'
    else:
        filename = listPart[0] + '.html'

    # initialized file and write byte
    file = open(filename, "wb")

    # check type ( content-length or chunked )
    # return header of file
    header = checkType(client)

    #Execute if type is content length
    if header.find(b'Content-Length') != -1:
        readContentLength(file, client, 1)
    #Execute if type is chunked
    elif header.find(b'chunked') != -1:
        readChunked(file, client)

    client.close()

def processEXTFILE(urlInput):
    # format url
    url = urllib.parse.urlparse(urlInput)
    target_host = url.hostname
    target_path = url.path
    target_scheme = url.scheme
    print('Host:%s\nPath:%s\nScheme:%s\n' %
          (target_host, target_path, target_scheme))

    # initialize port
    target_port = 80

    # create socket obj
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to host server
    client.connect((target_host, target_port))

    # create request to host server
    request = "GET %s HTTP/1.1\r\nHost:%s\r\n\r\n" % (urlInput, target_host)

    # send request
    client.sendall(request.encode())

    # initialized file name
    filename = target_path.replace('/', '_')

    # initialized file
    file = open(filename, "wb")

    # check type ( content-length or chunked )
    # return header of file
    header = checkType(client)

    if header.find(b'Content-Length') != -1:
        readContentLength(file, client, 2)
    elif header.find(b'chunked') != -1:
        readChunked(file, client)
    else:
        print("File inst content-length or chunked")
        '''
        Add exception here
        '''

def processFOLDER(urlInput):
    url = urllib.parse.urlparse(urlInput)
    
    target_host = url.hostname
    target_path = url.path
    target_scheme = url.scheme

    print('Host:%s\nPath:%s\nScheme:%s\n' %
          (target_host, target_path, target_scheme))
    #support create folder
    pathPart = target_path.split('/')
    #get the name before the final /
    folderName = './' + pathPart[len(pathPart) - 2]
    #create folder to save files
    os.mkdir(folderName)

    print("Create folder successfully")

    print("Choose system to donwload folder : \n1. Default\n2. Multi Request")
    temp = int(input())
    if temp == 1:
        processFOLDER_default(target_host, urlInput, folderName)
    elif temp == 2:
        processFOLDER_multireq(target_host, urlInput, folderName)
    else:
        print("Syntax error")

def processFOLDER_default(target_host, urlInput, folderName):
    # initialize port
    target_port = 80

    # create socket obj TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to host server
    client.connect((target_host, target_port))

    # request HTML of folder
    requestHTML = "GET %s HTTP/1.1\r\nHost:%s\r\n\r\n" % (
        urlInput, target_host)

    # send request to get html
    client.sendall(requestHTML.encode())

    # recv html
    html = client.recv(20000)

    # return string in " " of html
    listLink = getLink(html.decode())

    # return the correct file of the listlink
    fileList = checkSTR(listLink)

    client.close()

    single_req(fileList,target_host,target_port,urlInput, folderName)

def processFOLDER_multireq(target_host, urlInput, folderName):
    # initialize port
    target_port = 80

    # create socket obj
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to host server
    client.connect((target_host, target_port))

    # request HTML of folder
    requestHTML = "GET %s HTTP/1.1\r\nHost:%s\r\n\r\n" % (
        urlInput, target_host)

    # send request to get html
    client.sendall(requestHTML.encode())

    # recv html
    html = client.recv(20000)

    # return string in " " of html
    listLink = getLink(html.decode())

    # return the correct file of the listlink
    fileList = checkSTR(listLink)

    multi_req(client, urlInput, fileList, target_host, folderName)
#Đang dùng mỗi socket cho 1 web
def processMULTI_CONNECT(urlInput):
    # split links into list of link
    listurl = urlInput.split(' ')
    
    for url in listurl:
        choice = checkUrl(url)
        if choice == 1:
            processHTML(url)
        elif choice == 2:
            processEXTFILE(url)
        elif choice == 3:
            processFOLDER(url)
#Create new socket every iterations
def single_req(fileList ,target_host ,target_port, urlInput, folderName):
    for i in fileList:
        # initialized new socket for each file in list
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        # connect to server
        client.connect((target_host,target_port))  

        requestFile = "GET %s%s HTTP/1.1\r\nHost:%s\r\n\r\n" %(urlInput,i,target_host)
        
        client.send(requestFile.encode())

        file = open(folderName[2:] + '/' + i,'wb')
        
        # check type ( content-length or chunked )
        # return header of file
        header = checkType(client)

        if header.find(b'Content-Length') != -1:
            readContentLength(file, client, 2)
        elif header.find(b'chunked') != -1:
            readChunked(file, client)
        else:
            print("File inst content-length or chunked")
        
        client.close()
#Create 1 socket to receive all
def multi_req(client, urlInput, fileList, target_host, folderName):
    # run the first to the end file of the list
    for i in fileList:
        # each loop send a request to the server
        requestFile = "GET %s%s HTTP/1.1\r\nHost:%s\r\nConnection: keep-alive\r\n\r\n" % (urlInput, i, target_host)
        client.sendall(requestFile.encode())

    # read a folder for 1 time
    readFolder_multireq(client, fileList, folderName)

'''
Chưa đúng ý thầy, xem lại thử
Này là đọc 1 lần xong tách ra
Ý thầy: đọc từng phần content length - chunked để xác định data từng cái
'''

def readFolder_multireq(client, fileList, folderName):
    message = bytes()
    chunk = bytes()
    #Read all
    while True:
        chunk = client.recv(20000)
        print("Dowloading file...")
        message += chunk

        # print(chunk)
        if not chunk:
            break
    #split
    part = message.split(b"HTTP")
    #Write each part
    index = 0
    for i in part:
        if i == b'':
            continue
        i = b'HTTP' + i
        f = open(folderName[2:] + '/' + fileList[index], 'wb')
        f.write(i)
        print("Download file %d success" % (index+1))
        index += 1

def readContentLength(file, client, mode):
    # message : hold all data
    message = bytes()
    # chunk : hold data per recv
    chunk = bytes()

    '''
    Check lại receive đủ content length
    '''
    
    while True:
        # recv data from server
        chunk = client.recv(20000)

        # mode 1 : file is html
        if mode == 1:
            print("Dowloanding file...")
            message += chunk
            # print(chunk)
            break

        # when recv = 0 then out the while
        if not chunk:
            break

        # mode 2 : file is extension file
        else:
            print("Dowloanding file...")
            message += chunk
            # print(chunk)

    # write file
    file.write(message)
    print("Download file sucessfully\n")

    # close file
    file.close()

def readChunked(file, client):
    message = bytes()
    while True:

        # read the len chunk in hex size
        lenChunkInHex = bytes()
        endLine = '\r\n'

        # read until \r\n in chunk
        while lenChunkInHex.find(endLine.encode()) == -1:
            lenChunkInHex += client.recv(1)

        # split the \r\n out of chunk
        size = len(lenChunkInHex) #size of length of chunk
        # omit r\n\
        lenChunkInHex = lenChunkInHex[:size-2].decode()

        # change the hex-len-chunk to base 10
        lenChunk = int(lenChunkInHex, 16)

        # check is end of file
        if lenChunk == 0:
            break

        print("Chunk length received: %d" % lenChunk)

        chunk = client.recv(lenChunk)
        #If client failed to receive the chunk length
        #receive the missing bytes
        while len(chunk) < lenChunk:
            chunk += client.recv(lenChunk - len(chunk))

        file.write(chunk)

        message += chunk
        #Receive \r\n (not used)
        passItem = client.recv(2)
#Get all header bytes
def checkType(client):

    endHead = False
    endPart = '\r\n\r\n' #end of head
    header = bytes()

    while True:

        if endHead == True:
            return header
        else:
            # if not -> read a byte until get the endPart
            buff = 1

        chunk = client.recv(buff)

        header += chunk

        if header.find(endPart.encode()) != -1:
            endHead = True



# Retrieve a single page and report the URL and contents
def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout = timeout) as conn:
        return conn.read()

# We can use a with statement to ensure threads are cleaned up promptly
#https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future 

def multiCONNECT(urlInput):
    addHTTP(urlInput)

    URLS = urlInput.split(' ')

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
        #For each earliest completed future instances
        for future in concurrent.futures.as_completed(future_to_url):
            print(future)
            #Get url of completed future instance
            urlInput = future_to_url[future]
            #Check if url is type content length or chunked
            choice = checkUrl(urlInput)
            
            try:
                if choice == 1:
                    processHTML(urlInput)
                elif choice == 2:
                    processEXTFILE(urlInput)
            except Exception as exc:
                print('%r generated an exception: %s' % (urlInput, exc))

if __name__ == '__main__':
    print('Enter host address:')
    urlInput = input()

    multiCONNECT(urlInput)

    print("\nsuccess\n")

