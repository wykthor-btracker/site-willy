#imports
from imdb import IMDb as imdb
import json
#imports#

#variables

#variables#

#classes

#classes#

#function
def parse_genres(lists):
	flist = []
	ia = imdb()
	fdict = lists
	for i in fdict:
		info = ia.get_movie(int(i['id']),'main')
		i['genres'] = info['genres']
	return(fdict)
#function#

#main
def main(args):
	populate_genres(parse_genres())
	return 0
#main#
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
