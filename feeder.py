#imports
from unicodedata import normalize
from requests import get
from imdb import IMDb as imdb
from HTMLParser import HTMLParser
import json
#imports

#variables
#variables

#classes
class Picture_Parser(HTMLParser):
	def init(self):
		self.div = 0
		self.att = 0
		self.found = 0
		self.data = ''
		self.attrs = []
	def handle_starttag(self,tag,attrs):
		if (tag=="div"):
			self.div = 1
		try:
			for i in attrs:
				if('src' in i and self.found <2):
					self.data = i[1]
					self.found +=1
		except:
			pass
	def handle_endtag(self,tag):
		if(tag=="div"):
			self.tag = 0
	def spit(self):
		return(self.data)
		
class Yt_Url_HTMLParser(HTMLParser):
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
		if(self.div == 1 and self.att == 1 and 'https://www.youtube.com/watch?v=' in data and self.found == 0):
			self.data = data
			self.found = 1
	def handle_endtag(self,tag):
		if(tag=="div"):
			self.tag = 0	
	def spit(self):
		return(self.data)
#classes
#functions
def populate_json(keys):
	json_str = json.dumps(keys)
	with open('data.json','a') as f:
		json.dump(json_str,f)
def parse_list(filename):
	names = []
	with open(filename) as f:
		names=f.read().split('\n')
	return(names)
	
def get_keys(name,keys):
	ia = imdb()
	result = ia.search_movie(name)
	result = result[0]
	keys = {'title':str(result['title'].encode('ascii','ignore')),'year':result['year'],'id':result.movieID,'plot':str(ia.get_movie_plot(result.movieID)['data']['plot'][0]).encode('ascii','ignore')}
	keys['title'] += ' trailer'
	return(keys)
	
def get_resource_url(keys,url):
	url+='+'+'+'.join(keys['title'].split(' '))+'+'+str(keys['year'])
	return(url)
def get_poster_url(keys):
	url = "http://www.google.com/images?q=site:http://www.impawards.com"
#functions

#main
def main(args):
	keys = []
	names = []
	name = ''
	names = parse_list('input.txt')
	for item in names:
		url = "https://www.google.com.br/search?q="
		name = item
		keys = get_keys(name,keys)
		url = get_resource_url(keys,url)
		r = get(url)
		text = normalize('NFKD', r.text).encode('ascii','ignore')
		a = Yt_Url_HTMLParser()
		a.init()
		a.feed(text)
		keys['url']=a.spit()
		url = "http://www.google.com/images?q=site:http://www.impawards.com"
		url = get_resource_url(keys,url)
		r = get(url)
		text = normalize('NFKD', r.text).encode('ascii','ignore')
		a = Picture_Parser()
		a.init()
		a.feed(text)
		keys['pic'] = a.spit()
		for item,key in keys.iteritems():
			print(key,item)		
		populate_json(keys)
	return 0
#main
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
