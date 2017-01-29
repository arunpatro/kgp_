import urllib2
import requests
from bs4 import BeautifulSoup
import glob
import sys
import json

print 'starting	'
url_UG = 'https://erp.iitkgp.ernet.in/ERPWebServices/curricula/specialisationList.jsp?stuType=UG'
url_PG = 'https://erp.iitkgp.ernet.in/ERPWebServices/curricula/specialisationList.jsp?stuType=PG'
url_dep = 'https://erp.iitkgp.ernet.in/ERPWebServices/curricula/'
url_download = 'https://erp.iitkgp.ernet.in/ERPWebServices/curricula/commonFileDownloader.jsp?fileFullPath='


db_UG={}
db_PG={}
db_UG_el={}
db_PG_el={}
db_UG_depth={}
db_PG_depth={}
ele_UG=[]
ele_PG=[]
db={}

def save(dic, name):
	with open(name + ".json", "w") as outfile:
		json.dump(dic, outfile)


#accumulating all UG curriculums for all Departments/Stream
response_UG = requests.get(url_UG)
soup_UG = BeautifulSoup(response_UG.text,'html.parser')
all_dep = soup_UG.find_all('a')
for link in all_dep:
	try:
		db_UG[link.get('href')[45:]]=url_dep + link.get('href')
	except Exception as e:
		print e

#accumulating all PG curriculums for all Departments/Stream
response_PG = requests.get(url_PG)
soup_PG = BeautifulSoup(response_PG.text,'html.parser')
all_dep = soup_PG.find_all('a')
for link in all_dep:
	try:
		db_PG[link.get('href')[45:]]=url_dep + link.get('href')
	except Exception as e:
		print e


#accumulating all UG courses for each Department
for item in db_UG:
	url = db_UG[item]
	while True:
		try:
			response = requests.get(url)
			pass
		except Exception as e:
			print 'trying again'
			continue
		break
	soup = BeautifulSoup(response.text,'html.parser')
	all_links = soup.find_all('a')  # find all links
	for link in all_links:
		if(type(link.get('onclick'))==unicode):  #links to electives not pdfs
			if(len(link.contents[0].contents)!=0):  #empty links that cannot be clicked
				try:
					db_UG_depth[link.contents[0].contents[0].encode('ascii','ignore')]=url_download + link.get('onclick')[14:len(link.get('onclick'))-6].encode('ascii','ignore')
					sys.stdout.write('\rUG Depth Collected: {0}'.format(len(db_UG_depth)))
					sys.stdout.flush()
				except Exception as e:
					print 'error', link
					raise e
		elif(type(link.get('onclick'))!=unicode):
			ele_UG.append(url_dep + link.get('href'))

print ''

#accumulating all PG courses for each Department
for item in db_PG:
	url = db_PG[item]
	while True:
		try:
			response = requests.get(url)
			pass
		except Exception as e:
			print 'trying again'
			continue
		break
	soup = BeautifulSoup(response.text,'html.parser')
	all_links = soup.find_all('a')  # find all links
	for link in all_links:
		if(type(link.get('onclick'))==unicode):  #links to electives not pdfs
			if(len(link.contents[0].contents)!=0):  #empty links that cannot be clicked
				db_PG_depth[link.contents[0].contents[0].encode('ascii','ignore')]=url_download + link.get('onclick')[14:len(link.get('onclick'))-6].encode('ascii','ignore')
				sys.stdout.write('\rPG Depth Collected: {0}'.format(len(db_PG_depth)))
				sys.stdout.flush()
		elif(type(link.get('onclick'))!=unicode):
			ele_PG.append(url_dep + link.get('href'))

print ''

print 'Common Depth Courses: ' , len(set(db_UG_depth) & set(db_PG_depth))
print 'Total Depth Courses: ' , len(set(db_UG_depth) | set(db_PG_depth))

#saving depths
save(db_UG_depth,'ug_depths')
save(db_PG_depth,'pg_depths')
db=dict(db_UG_depth, **db_PG_depth)
save(db,'all_depths')
print 'saved all depths'

#accumulating all the UG Electives
for item in ele_UG:
	while True:
		try:
			response = requests.get(item)
		except Exception as e:
			print 'Trying eleUG', item
			continue
		break
	soup = BeautifulSoup(response.text,'html.parser')
	all_links = soup.find_all('a')  # find all links
	for link in all_links:
		while True:
			try:
				db_UG_el[link.contents[0].contents[0].encode('ascii','ignore')]=url_download + link.get('onclick')[14:len(link.get('onclick'))-6].encode('ascii','ignore')
				sys.stdout.write('\rUG Electives Collected: {0}'.format(len(db_UG_el)))
				sys.stdout.flush()
			except Exception as e:
				print 'trying again eleug'
				continue
			break
print ''

#accumulating all the PG Electives
for item in ele_PG:
	while True:
		try:
			response = requests.get(item)
		except Exception as e:
			print 'Trying elePG', item
			continue
		break
	soup = BeautifulSoup(response.text,'html.parser')
	all_links = soup.find_all('a')  # find all links
	for link in all_links:
		db_PG_el[link.contents[0].contents[0].encode('ascii','ignore')]=url_download + link.get('onclick')[14:len(link.get('onclick'))-6].encode('ascii','ignore')
		sys.stdout.write('\rPG Electives Collected: {0}'.format(len(db_PG_el)))
		sys.stdout.flush()

print ''


print 'Common Elective Courses: ' , len(set(db_UG_el) & set(db_PG_el))
print 'Total Elective Courses: ' , len(set(db_UG_el) | set(db_PG_el))

#saving electives
save(db_UG_el,'ug_electives')
save(db_PG_el,'pg_electives')
db2 = dict(db_UG_el, **db_PG_el)
save(db2,'all_electives')
print 'saved all ele'

save(dict(db,**db2),'all_courses')
print 'saved everything'