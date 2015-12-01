import urllib2
import requests
from bs4 import BeautifulSoup

url_1 = 'https://erp.iitkgp.ernet.in/ERPWebServices/curricula/CurriculaSubjectsList.jsp?stuType=UG&splCode=EE'
url_2 = 'https://erp.iitkgp.ernet.in/ERPWebServices/curricula/commonFileDownloader.jsp?fileFullPath='
name = 'data.pdf'

def download(url,name):
	f = urllib2.urlopen(url)
	with open(name, "wb") as code:
		code.write(f.read())

response = requests.get(url_1)

soup = BeautifulSoup(response.text,'html.parser')
all_links = soup.find_all('a')  # find all links
db={}
for link in all_links:
	if(type(link.get('onclick'))==unicode):  #links to electives not pdfs
		if(len(link.contents[0].contents)!=0):  #empty links that cannot be clicked
			db[link.contents[0].contents[0]]=url_2 + link.get('onclick')[14:len(link.get('onclick'))-6]

for item in db:
	download(db[item],item+'.pdf')
