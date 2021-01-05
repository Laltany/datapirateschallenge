import requests
from bs4 import BeautifulSoup
import jsonlines

def GetPage(url):

	request = requests.get(url)

	page = BeautifulSoup(request.text, 'html.parser')

	return page


def GetGenres(url):

	page = GetPage(url)

	td = page.findAll('input', {"name":"genres"})

	Genres = [Genre.get('value') for Genre in td]

	return Genres


def Crawler(url, genre, start):

	aux = []

	page = GetPage(url + '?genres='+ genre + '&start=' + start + '&count=250&sort=user_rating,asc') 

	movies = page.findAll('div', {"class":"lister-item-content"})


	for movie in movies:
		name = movie.find('h3', {'class': 'lister-item-header'}).a.text
		rating = movie.find('div',{'name': 'ir'}).text
		rating = rating.replace('\n', '')


		aux.append({'name': name, 'genre': genre, 'rating': rating})

	return aux
		

def SaveJsonl(movies):

	data_name = movies[0]['genre']

	with jsonlines.open(data_name + '.jsonl', mode='w') as writer:
		for movie in movies:
			writer.write(movie)

	

def GetMovies(url, Genres):
	movies = []
	for genre in Genres:
		for start in [0,251]:
			movies = movies + Crawler(url, genre, str(start))

		SaveJsonl(movies)
		movies.clear()
		

url = 'https://www.imdb.com/search/title/'

Genres = GetGenres(url)

GetMovies(url, Genres)
