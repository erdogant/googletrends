import time
import http.client as httplib
import datetime

# %%
def internet(url='www.google.com', sleepinsec=60, verbose=3):
    # Check whether connection is still alive.
    counter=1
    status=False

    while status==False:
        conn = httplib.HTTPConnection(url, timeout=5)
        try:
            conn.request("HEAD", "/")
            conn.close()
            status=True
        except:
            print('[check_connection] [ERROR] [%s] No internet connection? Trying again in 60 sec.. [attempt %s]' %(datetime.now().strftime('%d-%m-%Y %H:%M'), counter))
            status=False
            time.sleep(sleepinsec)
            counter = counter + 1

    if counter>1:
        if verbose>=3: ('[check_connection] [%s] Internet connection re-established after after %s attempts.' % (datetime.now().strftime('%d-%m-%Y %H:%M'), counter))
    return(status)
