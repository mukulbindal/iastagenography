from django.shortcuts import render
from django.http.response import HttpResponse

from bs4 import BeautifulSoup
import urllib
import requests
# import wget
import time
import os
import shutil
from mimetypes import guess_type


def save_photos(request):

	try:
		delete_photos()
	except:
		print("Failed")
	# return HttpResponse("Hello")
	id_=request.GET.get("id")
	id_ = int(id_)
	range_ = int(request.GET.get("range"))
	url = "https://erp.psit.in/assets/img/Simages/"+str(id_)+".jpg"
	print("Creating Directory")
	try:
		os.mkdir("Photos")
		print("created successfully...")
	except:
		print("Directory already present")
	for i in range(range_):
		r = requests.get("https://erp.psit.in/assets/img/Simages/"+str(id_+i)+".jpg")
		with open("./Photos/"+str(id_+i)+".jpg","wb") as f:
			f.write(r.content)
			f.close()
			#print("Saved",id_+i)

	shutil.make_archive("photos",'zip',"Photos")
	with open("photos.zip","rb") as f:
		response = HttpResponse(f , content_type=guess_type("photos.zip")[0])
		response['Content-length']=len(response.content)

		return response

def delete_photos():
	shutil.rmtree("Photos")
	os.remove("photos.zip")




def get_anime_list(request):

	page = '''
	<form method = "get" action = "/listofurl/">
	Enter page url <input type = "text" placeholder = "Enter here..." name = "link"></input><br><br><br>
	Enter start range <input type = "text" placeholder = "Enter here..." name = "start"><br><br><br>
	Enter end range <input type = "text" placeholder = "Enter here..." name = "end"><br><br><br>

	<input type = "submit" value = "Submit"></input>
	</form>
	'''
	return HttpResponse(page)

hdr = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
def getlink(url):
	print(url)
	r = requests.get(url)
	soup = BeautifulSoup(r.content,'html.parser')

	l = soup.find_all('span')
	download = l[3].parent['href']

	r2 = requests.get(download)

	soup2 = BeautifulSoup(r2.content,'html.parser')
	l = soup2.find_all('a')
	download_link = l[1]['href']

	# print(download_link)

	download_link = download_link.replace(" " , "%20")
	return download_link
	




def listofurl(request):
	try:
		page = request.GET.get('link')

		start = int(request.GET.get('start'))
		end = int(request.GET.get('end'))

		if 'episode' not in page.lower():
			link = page.replace("category/","")
			link+="-episode-1"
			page = link

		
		link = page.split("-")
		link.pop()
		link = "-".join(link)
		page = ""
		for i in range(start , end+1):
			try:
				next_link = getlink(link +"-"+ str(i))
				page+="<a href = '"+next_link+"'>Episode "+str(i)+"</a><br>"
			except:
				break
		return HttpResponse(page) if page!="" else HttpResponse("Error")
	except:
		return HttpResponse("Invalid Input")

