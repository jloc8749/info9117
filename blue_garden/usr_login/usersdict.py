#make dict of users
usr_dict = {}#change
def usrdict():#these names!!
    with open('users','r') as u:
        for each in u:
            usrname, usrpass = each.split()
            usr_dict[usrname] = usrpass
        #return usrdict
    
def authuser(nombre,llave):
    usrdict()
    if nombre in usr_dict:
        if usr_dict[nombre] == llave:
            return True    
        
def newuser(nombre,llave):
    usrdict()
    with open('users','a') as u:
        if nombre not in usr_dict:
            #u.write(nombre + ' ' + llave + '/n') #appending to the same line..
            print (nombre + ' ' + llave, file=u)
            
        
    
