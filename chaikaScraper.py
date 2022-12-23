import requests
from bs4 import BeautifulSoup
import os
import json
import time
import shutil
from random import randint

forbiddenChar = ["/", "\\", ":", "?", "*", "|", "<", ">"]
substituteChar = "_"

def main():
	downloadPath = input("Insert the path where the files will be downloaded:\n")
	createDonwloadPath(path=downloadPath)
	createLogs()
	urls = getChaikaLinks()
	alreadyScrapedId = getScraped()
	for url in urls:
		archiveId = url.split("/")[-3]
		if archiveId not in alreadyScrapedId:
			print("Downloading the following id: " + archiveId)
			jsonUrl = "https://panda.chaika.moe/api?archive=" + archiveId
			createTempFolder()
			jsonContent, mangaTitle = getTitle(jsonUrl)
			mangaTitle = cleanTitle(mangaTitle)
			fileDownloadPath = createDonwloadPath(downloadPath, mangaTitle)
			if fileDownloadPath != None:
				jsonPath = os.path.join(fileDownloadPath, "info.json")
				with open(jsonPath, "wb") as f:
					f.write(jsonContent)
				archiveContent = requests.get(url).content
				archiveContentPath = os.path.join(fileDownloadPath, mangaTitle) + ".zip"
				with open(archiveContentPath, "wb") as f:
					f.write(archiveContent)
				with open(".\\scraped.txt", "a") as f:
					f.write(archiveId)
					f.write("\n")
			else:
				with open("logs.txt", "a") as f:
					f.write(archiveId)
					f.write("\n")
		time.sleep(getRandomInt())

def createDonwloadPath(path=None):
	if not os.path.exists(path):
		os.mkdir(path)

def getRandomInt():
	return randint(3, 12)

def createLogs():
	if not os.path.exists(".\\scraped.txt"):
		with open("scraped.txt", "w") as f:
			f.write("\n")
			f.close()
	if not os.path.exists(".\\logs.txt"):
		with open(".\\logs.txt", "w") as f:
			f.write("\n")
			f.close()

def getChaikaLinks():
	r = requests.get("https://panda.chaika.moe/search/?title=&tags=&filecount_from=&filecount_to=&posted_from=&posted_to=&source_type=&reason=&uploader=&category=&filesize_from=&filesize_to=&sort=public_date&asc_desc=desc&gen-ddl=")
	chaikaLinks = r.content.decode("utf-8").split("\n")
	print("Found a total of " + str(len(chaikaLinks)) + " links in chaika")
	return chaikaLinks

def getScraped():
	with open("scraped.txt", "r") as f:
		ids = f.readlines()
		ids = [archiveId.rstrip() for archiveId in ids]
	print("Found a total of " + str(len(ids)) + " already scraped urls")
	return ids

def createTempFolder():
	if not os.path.exists(".\\temp"):
		os.mkdir(".\\temp")

def getTitle(url):
	r = requests.get(url)
	with open(".\\temp\\info.json", "wb") as f:
		f.write(r.content)
		f.close()
	jsonFile = open(".\\temp\\info.json", encoding="utf8")
	jsonData = json.load(jsonFile)
	title = jsonData["title"]
	print("found the follwing title: " + title)
	return r.content, title

def cleanTitle(t):
	charList = list(t)
	counter = 0
	for char in charList:
		if char in forbiddenChar:
			charList[counter] = substituteChar
		counter += 1
	t = "".join(charList)
	return t

def createDonwloadPath(p, title):
	downloadPath = os.path.join(p, title)
	if not os.path.exists(downloadPath):
		os.mkdir(downloadPath)
	else:
		print("Path already exists, the archive won't be downloaded, but it will be logged")
		return None
	return downloadPath


if __name__ == "__main__":
	main()