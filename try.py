import urllib2
import requests
from bs4 import BeautifulSoup

url_UG = 'https://erp.iitkgp.ernet.in/ERPWebServices/curricula/specialisationList.jsp?stuType=UG'
url_dep = 'https://erp.iitkgp.ernet.in/ERPWebServices/curricula/'
url_download = 'https://erp.iitkgp.ernet.in/ERPWebServices/curricula/commonFileDownloader.jsp?fileFullPath='


db_UG={}
db={}

def download(url,name):
	f = urllib2.urlopen(url)
	with open(name, "wb") as code:
		code.write(f.read())

response_UG = requests.get(url_UG)
soup_UG = BeautifulSoup(response.text,'html.parser')

all_dep = soup_UG.find_all('a')
db_UG={}
for link in all_dep:
	db_UG[link.get('href')[45:]]=url_dep + link.get('href')

for item in db_UG:
	url = db_UG[item]
	response = requests.get(url)
	soup = BeautifulSoup(response.text,'html.parser')
	all_links = soup.find_all('a')  # find all links
	for link in all_links:
		if(type(link.get('onclick'))==unicode):  #links to electives not pdfs
			if(len(link.contents[0].contents)!=0):  #empty links that cannot be clicked
				db[link.contents[0].contents[0]]=url_download + link.get('onclick')[14:len(link.get('onclick'))-6]


#downloading all files
# for item in db:
# 	download(db[item],item+'.pdf')

