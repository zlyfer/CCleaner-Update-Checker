from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pefile

def check_update(version):
    url = 'http://www.piriform.com/ccleaner/update?v=' + version
    isolate = "    piriform.constants.productUpdate.version = '"
    driver = webdriver.PhantomJS()
    driver.get(url)
    wait = WebDriverWait(driver, 7)
    print ("Getting latest version..")
    try:
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'page-foot ')))
    except:
        print ("Couldn't get latest version.")
        return False
    data = driver.page_source
    open('ccleaner_update_checker.dat', 'w').write(data)
    data = open('ccleaner_update_checker.dat', 'r').readlines()
    for latest_v in data:
        if isolate in latest_v:
            latest_v = latest_v.replace(isolate, '')
            latest_v = latest_v.replace("';", '')
            break
    driver.quit
    return latest_v

def get_current():
    print ("Getting current version..")
    pe = pefile.PE(r'C:\Program Files\CCleaner\CCleaner64.exe')
    current_v = pe.FileInfo[0].StringTable[0].entries[b'FileVersion']
    current_v = current_v.decode('utf-8')
    current_v = current_v.replace(' ', '').replace(',', '.')
    return current_v

current_v = get_current()
print ("Current version: %s" % current_v)
latest_v = check_update(current_v)
if latest_v != current_v and latest_v != False:
    print ("Update available: %s -> %s" % (current_v, latest_v))
elif latest_v == current_v:
    print ("You have the latest update: %s" % latest_v)