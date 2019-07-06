import urllib2
import BeautifulSoup
import re
import smtplib, ssl
import getpass

Newlines = re.compile(r'[\r\n]\s+')
def getClassInfo(): #gets input from the user about their courses that are filled
    campus = raw_input("What campus do you attend? O or V?").upper()
    numOfClasses = input("how many classes are full? Enter a numerical val such as 6:  ")
    info = [campus];
    for i in range(6):
        info.append(raw_input("what course are full? EX CPSC 111 101: [area course section]  ").upper())
    return info
def getSSCInfo(url): # scrapes the UBC course catalog to see if there are any open spots
    # given a url, get page content
    data = urllib2.urlopen(url).read()
    # parse as html structured document
    bs = BeautifulSoup.BeautifulSoup(data, convertEntities=BeautifulSoup.BeautifulSoup.HTML_ENTITIES)
    # kill javascript content
    for s in bs.findAll('script'):
        s.replaceWith('')
    # find body and extract text
    txt = bs.find('body').getText('\n')
    # remove multiple linebreaks and whitespace
    return Newlines.sub('\n', txt)
def setUp(): #collects user's email
    print("Hello, This was built to help you know when your courses are filled.\n")
    email  = raw_input("please enter your email:")

    cond = True
    while cond:
        econd = raw_input("is this email correct: " + email + "(Y or N)").upper()
        if(econd == "Y"):
            cond = False
            return email
        elif(econd == "N"):
            email  = raw_input("please reenter your email:")
        else:
            print("invalid input")
#--------------------------------------------------------------------------------------------------------------
usersEmail = setUp()
usersInfo = getClassInfo()
port = 465  # For SSL
password = getpass.getpass('Password:')
# Create a secure SSL context
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("my@gmail.com", password)
ClassFull = True
campus = usersInfo[0]
urls = []
for i in range(1,usersInfo.len()):
    if campus == "V":
        urls.append("https://courses.students.ubc.ca/cs/courseschedule?tname=subj-section&course="+usersInfo[i][usersInfo[i].find(' ')+1:usersInfo[i].find(' ')+4]+"&section="+usersInfo[i][-3:]+"&campuscd=UBC&dept="+usersInfo[i][0:usersInfo[i].find(' ')]+"&pname=subjarea")
    if campus == "O":
        urls.append("https://courses.students.ubc.ca/cs/courseschedule?tname=subj-section&course="+usersInfo[i][usersInfo[i].find(' ')+1:usersInfo[i].find(' ')+4]+"&section="+usersInfo[i][-3:]+"&campuscd=UBCO&dept="+usersInfo[i][0:usersInfo[i].find(' ')]+"&pname=subjarea")
while ClassFull:
    for j in range(0,urls.len()):
        if "Total Seats Remaining:\n0" not in getSSCInfo(urls[j]):
            ClassFull = False
            server.sendmail("senderemail@gmail.com", "myemail@gmail.com", usersInfo[j+1]) + "has an empty spot")
