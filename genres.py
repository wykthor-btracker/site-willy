#imports
from imdb import IMDb as imdb
import json
#imports#

#variables

#variables#

#classes

#classes#

#function
def parse_genres():
	flist = []
	ia = imdb()
	with open('data.json','r') as f:
		fdict = json.load(f)
	for i in fdict:
		info = ia.get_movie(int(i['id']),'main')
		info = info['genres']
		for u in info:
			if(not u.encode('utf-8','ignore') in flist):
				flist.append(u.encode('utf-8','ignore'))
	return(flist)
def populate_genres(flist):
	with open('genres.txt','w') as f:
		for i in flist:
			f.write(i+'\n')
#function#

#main
def main(args):
	populate_genres(parse_genres())
	return 0
#main#
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
