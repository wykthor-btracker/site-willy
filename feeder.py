#imports
from unicodedata import normalize
from requests import get
from imdb import IMDb as imdb
from HTMLParser import HTMLParser
#imports

#variables
url = "https://www.google.com.br/search?q="
keys = []
#variables

#classes
class MyHTMLParser(HTMLParser):
	def init(self):
		self.div = 0
		self.att = 0
		self.found = 0
		self.data = ''
	def handle_starttag(self, tag, attrs):
		if(tag=="div"):
			self.div = 1
		if(('class','th') in attrs):
			self.att = 1
		elif(('class','g') in attrs):
			self.att = 0
	def handle_data(self, data):
		if(self.div == 1 and self.att == 1 and 'https' in data):
			self.data = data
	def handle_endtag(self,tag):
		if(tag=="div"):
			self.tag = 0	
	def spit(self):
		return(self.data)
#classes
#functions
def get_keys(name,keys):
	ia = imdb()
	result = ia.search_movie(name)
	result = result[0]
	keys = [result['title'],result['year'],result.movieID,str(ia.get_movie_plot(result.movieID)['data']['plot'][0])]
	return(keys)
	
def get_trailer_url(keys,url):
	url+='+'.join(keys[0].split(' '))+str(keys[1])
	return(url)
#functions

#main
def main(args):
	url = "https://www.google.com.br/search?q="
	keys = []
	name = 'Toxic Avenger'
	keys = get_keys(name,keys)
	url = get_trailer_url(keys,url)
	r = get(url)
	text = normalize('NFKD', r.text).encode('utf-8','ignore')
	a = MyHTMLParser()
	a.init()
	a.feed(text)
	keys.append(a.spit())
	return 0
#main
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
