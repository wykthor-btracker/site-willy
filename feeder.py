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
		try:
			if('src' in attrs[1][0] and 'alt' in attrs[3][0] and 'http' in attrs[1][1] and self.found == 0):
					self.data = attrs[1][1]
					print("Added:"+attrs[1][1])
					self.found = 1
			else:
				pass
		except:
			pass
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
			self.data = data.replace('watch?v=','embed/')
			self.found = 1
	def handle_endtag(self,tag):
		if(tag=="div"):
			self.tag = 0	
	def spit(self):
		return(self.data)
#classes
#functions
def populate_json(keys):
	curr = []
	try:
		with open('data.json','r') as f:
			curr = json.load(f)
			for i in curr:
				if not i in keys:
					keys.append(i)
	except:
		pass
	with open('data.json','w') as f:
		json.dump(keys,f)

def parse_genres(lists):
	flist = []
	ia = imdb()
	fdict = lists
	for i in fdict:
		info = ia.get_movie(int(i['id']),'main')
		i['genres'] = info['genres']
	return(fdict)

def parse_list(filename):
	names = []
	with open(filename) as f:
		names=f.read().split('\n')
	return(names)
	
def get_keys(name,keys):
	ia = imdb()
	print(name)
	try:	
		result = ia.search_movie(name)
		result = result[0]
		keys = {'title':result['title'].encode('utf-8','ignore'),'year':result['year'],'id':result.movieID,'plot':ia.get_movie_plot(result.movieID)['data']['plot'][0].encode('utf-8','ignore')}
		keys['title'] += ' trailer'	
		print("OK")
	except:
		print("Something went wrong with "+name)
		keys = {'title':'null','id':'-1','plot':'null','year':'null'}
	return(keys)
	
def get_resource_url(keys,url):
		url+='+'+'+'.join(keys['title'].split(' '))+'+'+str(keys['year'])
		return(url)
#functions

#main
def main(args):
	errors = 0
	movies = 0
	keys = []
	lists = []
	names = []
	name = ''
	names = parse_list('input.txt')
	for item in names:
		url = "https://www.google.com.br/search?q="
		name = item
		keys = get_keys(name,keys)
		url = get_resource_url(keys,url)
		if(keys['id']!='-1'):
			movies+=1
			r = get(url)
			text = normalize('NFKD', r.text).encode('ascii','ignore')
			a = Yt_Url_HTMLParser()
			a.init()
			a.feed(text)
			keys['url']=a.spit()
			url = "http://www.google.com/images?q=poster+"
			url = get_resource_url(keys,url)
			r = get(url)
			text = normalize('NFKD', r.text).encode('ascii','ignore')
			a = Picture_Parser()
			a.init()
			a.feed(text)
			keys['pic'] = a.spit()
			lists.append(keys)
		else:
			errors+=1
	lists = parse_genres(lists)
	populate_json(lists)
	print("Total movies added:"+str(movies))
	print("Total errors:"+str(errors))
	return 0
	
#main
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
