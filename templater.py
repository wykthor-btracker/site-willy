#!/usr/bin/env python
# -*- coding: utf-8 -*-

#imports
import json
import os.path
#variables

#classes

#functions
def get_filepath(movie_id):
	root = os.path.dirname(os.path.realpath("__file__"))
	subdir = "pages"
	filename = movie_id+'.html'
	return os.path.join(root,subdir,filename)
	
def get_index():
	with open('index.html','r') as f:
		index = f.read()
	return(index)
	
def get_template():
	with open('template.html','r') as f:
		template = f.read()
	return(template)
	
def specific_template(temp,movie):
	temp = temp.replace("{title}",movie['title'][:-8])
	temp = temp.replace("{filme}",movie['title'][:-8])
	temp = temp.replace("{url}",movie['url'])
	temp = temp.replace("{sinopse}",movie['plot'])
	first = temp.find("<start>")+len("<start>")
	last = temp[first:].find("<end>")+first
	subtemp = temp[first:last]
	similar = ''
	for i in range(5):
		
	return temp

def create_page(temp,movie):
	filepath = get_filepath(movie['id'])
	with open(filepath,'w') as f:
		f.write(temp)

def get_line_template(index):
	first = index.find('<start>')+len('<start>')
	last = index[first:].find('<end>')+first
	return index[first:last]
	
def write_table(table,movies,template):
	table = table.replace(template,movies)
	return table
		
def get_pic_template(index):
	first = index.find('<td id = "template">')
	last = index[first:].find('</td>')+len('</td>')+first
	temp = index[first:last]
	return(temp)

def get_movie_list():
	with open('data.json','r') as f:
		m_list = json.load(f)
	for pos in range(len(m_list)):
		for key in m_list[pos]:
			if(type(m_list[pos][key]) == unicode):
				m_list[pos][key] = m_list[pos][key].encode('utf-8','ignore')
			elif(type(m_list[pos][key]) == list):
				for val in range(len(m_list[pos][key])):
					m_list[pos][key][val] = m_list[pos][key][val].encode('utf-8','ignore')
	return(m_list)

def prepare_template(temp,movie):
	temp = temp.replace('{id}',movie['id'])
	temp = temp.replace('{pic}',movie['pic'])
	return(temp)

def get_genres(m_list):
	genres = []
	for i in m_list:
		for u in i['genres']:
			if(not u in genres):
				genres.append(u)
	return(genres)

def sort_genres(m_list,genres):
	sorted_list = []
	for genre in genres:
		curr = []
		for movie in m_list:
			if genre in movie['genres']:
				if(not movie['id'] in curr):
					curr.append(movie['id'])
		sorted_list.append(curr)
	return(sorted_list)

#main
def main():
	m_list = get_movie_list()
	index = get_index()
	table_template = get_line_template(index)
	pic_template = get_pic_template(index)
	genres = get_genres(m_list)
	sorted_list = sort_genres(m_list,genres)
	table = ''
	links = []
	for u in range(15):
		g_list = ''
		found = 0
		i = -1
		size = len(m_list)
		while(True):
			i+=1
			if(i==len(m_list)):
				break			
			print(u,len(genres),i,len(m_list),found)
			if(genres[u] in m_list[i]['genres']):
				found+=1
				if(found == 10):
					break				
				g_list+=prepare_template(pic_template,m_list[i])
				spec_template = get_template()
				spec_template = specific_template(spec_template,m_list[i])
				create_page(spec_template,m_list[i])
				table_genre = table_template.replace("{genero}",genres[u])
				if(not genres[u] in links):
					links.append(genres[u])
				m_list.remove(m_list[i])
				i+=1
		table+=write_table(table_genre,g_list,pic_template)
	index = index.replace(table_template,table)
	for i in links:
		index = index.replace("url",i,2)
	with open('index.html','w') as f:
		f.write(index)
	return 0

if __name__ == '__main__':
	main()
#main#
