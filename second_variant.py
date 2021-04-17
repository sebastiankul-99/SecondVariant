import requests, json
from collections import defaultdict
from math import sqrt
import copy

posts_info = json.loads(requests.get("https://jsonplaceholder.typicode.com/posts").content)
users_info = json.loads(requests.get("https://jsonplaceholder.typicode.com/users").content)


def concat_files(users_inf, posts_inf):
	'''  Function to combine users and posts info into one file '''
	concatenated_info = copy.deepcopy(users_inf)
	for user in concatenated_info:
		user['posts'] = []
	for post in posts_inf:
		for user in concatenated_info:
			if user['id'] == post['userId']:
				user['posts'].append({'title': post['title'], 'body': post['body']})
				break
	return concatenated_info


def num_of_posts(concatenated_info):
	''' Function to count number of posts for each user. Function returns list of strings '''
	names_list = []
	for user in concatenated_info:
		names_list.append(user['name'] + " napisał(a) " + str(len(user['posts'])) + " postów")
	return names_list


def check_unique(posts):
	''' Function to check unique post's titles. Function returns list of common titles '''
	num_of_titles = defaultdict(int)
	for post in posts:
		num_of_titles[post['title']] += 1
	common_titles_list = []
	for key, val in num_of_titles.items():
		if val > 1:
			common_titles_list.append(key)
	return common_titles_list


def find_dist(x1, y1, x2, y2):
	''' Function to calculate distance between two users '''
	distance = (float(x1)-float(x2))**2+(float(y1)-float(y2))**2
	return sqrt(distance)


def find_nearest(users_in):
	''' Function to find nearest neighbour for each user. Return dictionary of users as keys and their nearest neighbour as values'''
	nearest_neighbour = {}
	min_dist_val = 999999999999
	neighbour_name = ""
	for user in users_in:
		for neighbour in users_in:
			if user['id'] != neighbour['id']:
				act_dist_val = find_dist(user['address']['geo']['lat'], user['address']['geo']['lng'], neighbour['address']['geo']['lat'], neighbour['address']['geo']['lng'])
				if min_dist_val > act_dist_val:
					min_dist_val = act_dist_val
					neighbour_name = neighbour['name']
		nearest_neighbour[user['name']] = neighbour_name
		min_dist_val = 999999999999
		neighbour_name = ""
	return nearest_neighbour


if __name__ == '__main__':
    concat_info = concat_files(users_info, posts_info)
    sample = json.dumps(concat_info[1], indent=2)
    print(sample)
    num_of_posts = num_of_posts(concat_info)
    print(num_of_posts)
    common_titles = check_unique(posts_info)
    print(common_titles)
    neighbours = find_nearest(users_info)
    for key, val in neighbours.items():
	    print(key, " : ", val)