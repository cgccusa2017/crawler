
# from bs4 import BeautifulSoup as Soup
import requests

class Crawler():

	def crawl(self, url):

		'''
		:param self
		:param url: the content in a single url
		:return links: set of url links found in url_content
		:return text: strings of all text (not include links)

		This function opens an url (request), return the text and links if no error encountered.
		'''

		# max_wait = 60

		# if empty url string
		if not url:
			return set([]), ""

		# open the url, may have many exceptions
		response = requests.get(url, timeout=60)
		code = response.status_code

		if code == requests.codes.ok:
			return code, response.text

		# # Retry url: keep requesting the url until exceed the time limit
		# if code in ErrorCode.retry_code:
		# 	time = 0
		# 	while time < max_wait and code in ErrorCode.retry_code:
		# 		sys.sleep(1)
		# 		response = requests.get(url)
		# 		code = response.status_code
		# 		time += 1
		#
		# 		if time == max_wait:
		# 			return None

		# Otherwise, return None
		return code, None



url = 'http://www.python.org/'
print(Crawler().crawl(url))

'''
	Args:
		- url_content: the content in a single url

	Return:
		- links: set of url links found in url_content
		- text: strings of all text (not include links)

	def crawl(self, url_content):

		
		if not url_content:
			return [], ""

		links = set()
		text = ""

		text = Soup(url_content, 'html.parser')
		for a in text.find_all('a'):
			links.add(a['href'])
			del a['href']

		#print(text)
		#content = re.sub(r'^https?:\/\/.*[\r\n]*', '', url_content, flags=re.MULTILINE)
		#for line in content:
		#	text += ''.join(line.strip().split('\n'))

		return links, text

# string="text1\ntext2\nhttp://url.com/bla1/blah1/\ntext3\ntext4\nhttp://url.com/bla2/blah2/\ntext5\ntext6"

# print(Crawler().crawl(string))


'''
