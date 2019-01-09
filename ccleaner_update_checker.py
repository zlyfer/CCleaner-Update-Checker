from bs4 import BeautifulSoup
import requests
import pefile
import os

browser_path = r'chrome'
ccleaner_path = r'C:\Program Files\CCleaner\CCleaner64.exe'
ccleaner_url = r'https://filehippo.com/de/download_ccleaner'
isolate_string1 = r'Download CCleaner '
isolate_string2 = r' for PC Windows - FileHippo.com'
isolate_dstring1 = r'        <a class="program-header-download-link green button-link active long download-button"'
isolate_dstring2 = r"""            onclick="_gaq.push(['_trackEvent', 'Download', 'Download, DM Disabled', 'ccleaner']);"""


def get_latest():
    version = 'Error'
    download = 'Error'
    record = False
    session = requests.session()
    response = session.get(ccleaner_url).text
    soup = BeautifulSoup(response, "html.parser")
    content = soup.get_text("\n").split("\n")
    for line in content:
        if isolate_string1 in line and isolate_string2 in line:
            version = line.replace(isolate_string1, '').replace(isolate_string2, '')
    for line in response.split("\n"):
        if isolate_dstring2 in line:
            record = False
        if record:
            download = line.replace('            href="', '').replace('"', '')
        if isolate_dstring1 in line:
            record = True
    return [version, download]


def get_installed():
    pe = pefile.PE(ccleaner_path)
    version = pe.FileInfo[0].StringTable[0].entries[b'FileVersion']
    version = version.decode('utf-8')
    version = version.replace(' ', '').replace(',', '.')
    return version


print("Please wait, fetching versions..")
installed = get_installed()
os.system('cls')
print("Installed version: %s" % installed)
data = get_latest()
latest = data[0]
download = data[1]
print("Latest version:    %s" % latest)

if installed != latest:
    print("Update available. Press any key to open the download page..")
    input("The url that will be opened is: %s" % download)
    os.system("%s %s" % (browser_path, download))
else:
    print("Your version is up to date.")
