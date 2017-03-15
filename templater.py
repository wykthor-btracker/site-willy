#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#fileheader
#imports
import json
#variables

#classes

#functions
def get_index():
	with open('index.html','r') as f:
		index = f.read()
	return(index)
	
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
	pic_template = get_pic_template(index)
	genres = get_genres(m_list)
	sorted_list = sort_genres(m_list,genres)
	g_list = ''
	for i in range(5):
		g_list+=prepare_template(pic_template,m_list[i])
	print(g_list)
	return 0

if __name__ == '__main__':
	main()
#main#
