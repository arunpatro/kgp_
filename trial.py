import urllib2
import requests
from bs4 import BeautifulSoup

url_PG = 'https://erp.iitkgp.ernet.in/ERPWebServices/curricula/specialisationList.jsp?stuType=PG'
url_PG = 'https://erp.iitkgp.ernet.in/ERPWebServices/curricula/specialisationList.jsp?stuType=PG'
url_dep = 'https://erp.iitkgp.ernet.in/ERPWebServices/curricula/'
url_download = 'https://erp.iitkgp.ernet.in/ERPWebServices/curricula/commonFileDownloader.jsp?fileFullPath='

db_PG={}
db_PG={}
db_el={}
db={}
ele_PG=[]
ele_PG=[]

#to download one file
def download(url,name):
	f = urllib2.urlopen(url)
	with open(name, "wb") as code:
		code.write(f.read())

#accumulating all PG curriculums for all Departments/Stream
response_PG = requests.get(url_PG)
soup_PG = BeautifulSoup(response_PG.text,'html.parser')
all_dep = soup_PG.find_all('a')
for link in all_dep:
	db_PG[link.get('href')[45:]]=url_dep + link.get('href')


#accumulating all PG courses for each Department
for item in db_PG:
	url = db_PG[item]
	response = requests.get(url)
	soup = BeautifulSoup(response.text,'html.parser')
	all_links = soup.find_all('a')  # find all links
	for link in all_links:
		if(type(link.get('onclick'))==unicode):  #links to depths not electives
			if(len(link.contents[0].contents)!=0):  #empty links that cannot be clicked
				db[link.contents[0].contents[0]]=url_download + link.get('onclick')[14:len(link.get('onclick'))-6]
		elif(type(link.get('onclick'))!=unicode):
			ele_PG.append(url_dep + link.get('href'))

for item in ele_PG:
	response = requests.get(item)
	soup = BeautifulSoup(response.text,'html.parser')
	all_links = soup.find_all('a')  # find all links
	for link in all_links:
		db_el[link.contents[0].contents[0]]=url_download + link.get('onclick')[14:len(link.get('onclick'))-6]

# #downloading all files
# for item in db:
# 	download(db[item],item+'.pdf')
