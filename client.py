import socket, postfile, json, time, urllib, urllib2

"""

for test please enter the method 1 or 2
and if you choose 1 please enter the file name of the file containing the signature of the virus

"""



def deleteContent(pfile): # delete files content in case it contains malicious software
    pfile.seek(0)
    pfile.truncate()
"""
is this function we are retreiving the response of the scan done by virus total
as you can see the latency is quite poor so we need to sleep 30 seconds before asking for the response (and some time more).
the response comes in a json form
the resoure parameter is received from the scan request done earlier in checkvirustotalDB

"""



def retrievefromvirustotal(j):
    url = "https://www.virustotal.com/vtapi/v2/file/report"
    parameters = {"resource": j, "apikey": "61ee5459e495525126a8b8297f24fd6768ca4f38a0cbbc3435c96926c47fa14d"} # my api key at virustotal, resource is given from last func
    data = urllib.urlencode(parameters)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    json_ = response.read()
    j = json.loads(json_)
     # as long as the response code from virus total isnt '1' than the scan isnt done and we need to wait,
     # the long wait period is because we are using a free api key so we can only make 4 calls to virus total for each client.
     # if the wait time was shorter we will get an exception if the scan will take too long. (this is prevented)
    while j['response_code'] != 1:
        print 'Still Thinking...'
        time.sleep(30) # it takes virus toal a while to check the file so we will wait for response_code to be 1, meaning the review is ready
        response = urllib2.urlopen(req)
        json_ = response.read()
        j = json.loads(json_)
    return j['positives'] # returns the number of positive virus discoveries, if zero no viruses found, the file is clean and we can save it

"""
is this function we are sending the file received from the server to the virustotal servers
where it will be checked with their enormous database of viruses signatures.
this function will queue the scan in virustotal and will move to retrievefromvirustotal function for the response
when retrievefromvirustotal return it will return the result to the main function and there action will be taken considering the result
"""
def checkvirustotalDB(file):
    host = "www.virustotal.com"
    selector = "https://www.virustotal.com/vtapi/v2/file/scan"
    fields = [("apikey", "61ee5459e495525126a8b8297f24fd6768ca4f38a0cbbc3435c96926c47fa14d")] # my api key at virustotal
    file_to_send = open("mytext.txt", "rb").read()
    files = [("file", "mytext.txt", file_to_send)]
    json_ = postfile.post_multipart(host, selector, fields, files)
    j = json.loads(json_)
    return retrievefromvirustotal(j['scan_id']) # we are sending the scan_id parameter so we can get the correct response later

def checkforvirus(data, signature): # check with known in adavnace signature
    if signature in data:
        return True
    else:
        return False

def main():
    s = socket.socket()             # Create a socket object
    host = socket.gethostname()     # Get local machine name
    port = 60004                    # Reserve a port for your service.
    # 1 - check file for a known in adavance virus with a given signature, virus signature in a txt file, the name of the file will be given by the user
    # 2 - send file to check for viruses with the virus signature database of virustotal
    scanMethod = raw_input('Choose Type Of Defence:\nTo scan for known in advance virus signature type ---> 1\nTo scan for viruses with virustotal database type ---> 2\n')
    while scanMethod != '1' and scanMethod != '2': # if users input not equal to 1 or 2 try again
        print 'Wrong Input!\n'
        scanMethod = raw_input('Choose Type Of Defence:\n To scan for known in advance virus signature type ---> 1\n To scan for viruses with virustotal database type ---> 2\n')
    if scanMethod == '1': # in case we want to check for known in advance virus signature
        filename = raw_input("Enter the name of file that contains the virus signature:\n")
        f = open(filename,'rb')
        l = f.read(1024)
        signature = l # the virus signature is contained here
    s.connect((host, port)) # connect to server on port 60004
    s.send("Send me a file server!")
    with open('received_file', 'wb') as f: # this file will contain the file transferred from server in case it is clean (no virus found)
        print 'Scanning file for viruses' # alert user that the file is being checked
        infected = False # isInfected? boolean
        while True:
            #print('receiving data...')
            data = s.recv(1024) # receiving data from server in 1k chunks
            if scanMethod == '1': # known signature based
                infected = checkforvirus(data, signature) # scan for virus signature in every given chunk
            #print('data=%s', (data))
            if not data:
                break
            if infected: # if we found a virus signature in the file binary we will delete it and break from the scanning process
                deleteContent(f)
                break
            # write data to a file
            f.write(data)
        if scanMethod == '2': # virus total based
            infected = not checkvirustotalDB(f)
            if infected:
                deleteContent(f) # if virus total results tells us that the file may contain a virus' we will delete the content
    f.close()
    if infected:
        s.send("The file you sent contains a virus, delete it now!") # announce to server the file he is sending contains a malicious software
        print('The file received from server contains a virus and is now being deleted.') # alert user that the file received contains a virus an therefor erased
    else:
        print('The file is clean, and is now stored in AntiVirus folder') # alert user that the file was scanned and is now stored
    s.close()
    print('connection closed')

if __name__ == '__main__':
    main()