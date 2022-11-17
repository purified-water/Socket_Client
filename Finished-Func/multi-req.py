import socket
import re

def getLink(html):
    listLink = re.findall('"([^"]*)"',html)
    return listLink


def checkSTR(listLink):
    checkedList = []
    for i in listLink:
        if i.find('.pdf') != -1:
            checkedList.append(i)
    print(checkedList)
    return checkedList


def multiReq(checkedList):
    checkedListLen = []
    for i in checkedList:
        requestFile = "HEAD http://web.stanford.edu/class/cs224w/slides/%s HTTP/1.1\r\nHost:%s\r\n\r\n" %(i,target_host)
        client.send(requestFile.encode())
        




target_host = "web.stanford.edu" 
target_port = 80  # create a socket object 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  


# connect the client 
client.connect((target_host,target_port))  


# send some data 
# request = "GET /index.html/ HTTP/1.1\r\nHost:%s\r\n\r\n" % target_host

requestHTML = "GET http://web.stanford.edu/class/cs224w/slides/ HTTP/1.1\r\nHost:%s\r\n\r\n" %target_host


client.send(requestHTML.encode())

#ERROR: Randomly receive request bytesz
html = client.recv(20000)
f = open('index.html' , 'wb')
f.write(html)

listLink = getLink(html.decode())

print(listLink)

checkedList  = checkSTR(listLink)



client.close()