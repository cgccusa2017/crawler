
import requests
from CrawlerApp import LoginModule
from CrawlerApp.Settings import CrawlerSettings
from CrawlerApp import TextProcessor

class Crawler:
	def __init__(self, session=None):
		if not session:
			self.session = requests.Session()
		else:
			self.session = session

		self.tp = TextProcessor.TextProcessor()

	def __del__(self):
		self.session.close()


	def default_crawler_setter(self, crawler_settings):
		self.session.headers = CrawlerSettings.get_default_headers()
		

	def crawl(
			self,
			target_url,
			crawler_settings=None,
			crawler_setter=None,
			need_login=None,
			max_timeout=60):
		"""
		This function opens an url (request), return the code and text if no error encountered.
		:param self
		:param target_url: the content in a single url
		:param crawler_settings: a dictionary contains header {}, form_data {}
		:param crawler_setter
		:param need_login
		:param max_timeout
		:return target_url: update the url if redirect happened, otherwise original url
		:return code: indicate success or fail when try to open the url
		:return text: all text inside the url
		"""

		# if empty url string
		if not target_url:
			return target_url, -1, None

		# check if the original url is valid
		target_url = self.tp.is_valid_url("", target_url)
		if target_url is None:
			return target_url, -1, None

		# add function to get cookies (LoginModule, github_login), and set session cookies
		if crawler_settings and crawler_setter:
			self.session = crawler_setter(self.session, crawler_settings)
		else:
			self.default_crawler_setter(crawler_settings)
			

		if need_login:
			# return the cookies of specific website
			cookies = LoginModule.get_cookies(target_url, crawler_settings)
			self.session.cookies = cookies

		# open the url, may have many exceptions
		response = self.session.get(target_url, timeout=max_timeout)
		status_code = response.status_code

		if response.history and response.history[0].status_code in CrawlerSettings.get_redirect_code():
			target_url = response.url
			#print(target_url)

		if status_code == requests.codes.ok:
			return target_url, status_code, response.text

		return target_url, -1, None



if __name__ == "__main__":
	url = 'http://www.github.com/'
	url, code, content = Crawler().crawl(url)
	print("==============main method==============")
	print(url)

