import requests
from CrawlerApp import LoginModule
from CrawlerApp.Settings import CrawlerSettings
from CrawlerApp import TextProcessor


class Crawler:
	"""
	This class handles crawling website.
	"""
	def __init__(self, session=None):

		# Session for accessing database
		if not session: 
			self.session = requests.Session()
		else:
			self.session = session

		# Text processor
		self.tp = TextProcessor.TextProcessor()

	def __del__(self):
		"""
        Close the db session when done.
        """
		self.session.close()


	def default_crawler_setter(self, crawler_settings):
		"""
		This function sets the header of the session, or other crawler settings if needed.
		"""
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

		# If empty url string, return.
		if not target_url:
			return target_url, -1, None

		# Check if the original url is valid.
		target_url = self.tp.is_valid_url("", target_url)
		if target_url is None:
			return target_url, -1, None

		# Add function to get cookies (LoginModule, github_login), and set session cookies.
		if crawler_settings and crawler_setter:
			self.session = crawler_setter(self.session, crawler_settings)
		else:
			self.default_crawler_setter(crawler_settings)
			
		# If the url needs login information.
		if need_login:
			# return the cookies of specific website
			cookies = LoginModule.get_cookies(target_url, crawler_settings)
			self.session.cookies = cookies

		# Open the url, return None if status_code != 200
		try:
			response = self.session.get(target_url, timeout=max_timeout)
		except requests.exceptions.SSLError:
			response = self.session.get(target_url, timeout=max_timeout, verify=False)


		# warnings.simplefilter('ignore',InsecureRequestWarning)
		status_code = response.status_code

		# Update the url if redirected to other url.
		if response.history and response.history[0].status_code in CrawlerSettings.get_redirect_code():
			target_url = response.url
			
		# Only return the url, status code and text if successfully to open the url.
		if status_code == requests.codes.ok:
			return target_url, status_code, response.text

		return target_url, -1, None



if __name__ == "__main__":
	url = 'http://www.github.com/'
	url, code, content = Crawler().crawl(url)
	print("==============main method==============")
	print(url)

