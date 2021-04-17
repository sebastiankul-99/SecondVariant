import second_variant
import unittest
import copy


class TestSecondVariant(unittest.TestCase):
	combined = second_variant.concat_files(second_variant.users_info, second_variant.posts_info)
	posts = second_variant.posts_info
	users = second_variant.users_info

	def test_concat_files(self):
		''' Testing the concat_files function from second_variant module.'''
		all_posts = 0
		for x in self.combined:
			all_posts += len(x['posts'])
		self.assertEqual(all_posts, 100) # because total number of posts is 100.
		for x in self.combined:
			self.assertEqual(len(x['posts']), 10) # each user has 10 posts in posts json file

		for post in self.posts:
			post_id = int(post['id']) % 10
			if post_id ==0:
				post_id = 9
			else:
				post_id -= 1
			self.assertEqual(self.combined[int(post["userId"])-1]['posts'][post_id]['title'], post['title'])
			self.assertEqual(self.combined[int(post["userId"]) - 1]['posts'][post_id]['body'], post['body'])

	def test_num_of_posts(self):
		''' Testing the num_of_posts function from second_variant module.'''
		num_of_posts = second_variant.num_of_posts(self.combined)
		self.assertEqual(len(num_of_posts), 10) # because total number of users is 10. That's the reason of checking len (list)
		self.assertEqual(num_of_posts[3], self.combined[3]['name'] + ' napisał(a) 10 postów')
		self.assertEqual(num_of_posts[2], self.combined[2]['name']+' napisał(a) 10 postów')
		combined = copy.deepcopy(self.combined)
		combined[2]['posts'].append({"title": "testing", 'body': 'testing'})
		combined[3]['posts'].pop()
		num_of_posts = second_variant.num_of_posts(combined)
		self.assertEqual(num_of_posts[2], combined[2]['name']+' napisał(a) 11 postów')
		self.assertEqual(num_of_posts[3], combined[3]['name'] + ' napisał(a) 9 postów')

	def test_check_unique(self):
		''' Testing the check_unique function from second_variant module.'''
		self.assertEqual(len(second_variant.check_unique(self.posts)), 0) # there aren't common titles, so the len(list) shoud be 0
		posts_inf = copy.deepcopy(self.posts) # without deepcopy, this test method would interrupt the first test method
		posts_inf[0]['title'] = posts_inf[1]['title']
		posts_inf[2]['title'] = posts_inf[3]['title']
		title_list = list()
		title_list.append(posts_inf[0]['title'])
		title_list.append(posts_inf[2]['title'])
		returned_titles_list = second_variant.check_unique(posts_inf)
		self.assertNotEqual(len(returned_titles_list), 0)
		self.assertEqual(returned_titles_list, title_list)

	def test_find_nearest(self):
		''' Testing the find_nearest function from second_variant module.'''
		users = copy.deepcopy(second_variant.users_info)
		users[0]['address']['geo']['lat'] = "-2000000.21"
		users[0]['address']['geo']['lng'] = "-2000000.21"
		neighbours = second_variant.find_nearest(self.users)
		changed_neighbours = second_variant.find_nearest(users)
		self.assertNotEqual(next(iter(neighbours.values())), next(iter(changed_neighbours.values())))
		users[0]['address']['geo']['lat'] = users[1]['address']['geo']['lat']
		users[0]['address']['geo']['lng'] = users[1]['address']['geo']['lng']
		changed_neighbours = second_variant.find_nearest(users)
		self.assertEqual(next(iter(changed_neighbours.values())), users[1]['name'])


if __name__ == '__main__':
	unittest.main()
