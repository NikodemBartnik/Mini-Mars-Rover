import socket            

s = socket.socket()        
port = 12345               

s.bind(('', port))        
print ("socket binded to %s" %(port))
 
s.listen(5)    
print ("socket is listening")           
 

print('waiting')
c, addr = s.accept()    

while True:
   
    print ('Got connection from', addr )
 
    # send a thank you message to the client. encoding to send byte type.
    print(c.recv(50))
    c.send('Thank you for connecting'.encode())
    # Close the connection with the client
    #c.close()