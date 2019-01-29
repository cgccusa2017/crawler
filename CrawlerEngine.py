import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
from urllib.parse import urlparse
from urllib.parse import urljoin
import Settings


class Crawler(object):
	def __init__(self, root_url, session_limit=3):
		self.seen_page = set()
		self.visited_page = set()
		self.counter = 0
		self.s = requests.Session()
		self.s.headers = Settings.headers
		self.update_session()

		self.root_url = root_url
		self.netloc = urlparse(root_url).netloc
		self.session_limit = session_limit  # limit request per session

	def update_session(self):
		self.s = requests.Session()
		self.s.headers = Settings.headers

	def get_bs_obj(self, url=None, only_a=False):
		if not url:
			url = self.root_url
		
		if self.counter % self.session_limit == 0:
			self.update_session()

		r = self.s.get(url)
		if not r.ok:
			# invalid request
			return None
		self.visited_page.add(url)
		self.counter += 1
		html = r.content
		if only_a:
			only_a_tags = SoupStrainer("a")
			if self.netloc == 'www.wsj.com':
				parser = "lxml"
			else:
				parser = "html.parser"

			return BeautifulSoup(html, parser, parse_only=only_a_tags)
		else:
			return BeautifulSoup(html, "html.parser")

	def get_all_links(self, url_in):
		links = set([])
		bs_obj = self.get_bs_obj(url_in, only_a=False)

		if bs_obj is None:
			return links
		# print(url_in,bsObj.title.string)
		results = bs_obj.find_all("a")
		for r in results:
			try:
				url = r['href']
				o = urlparse(url)
				if o.netloc == '':
					url = urljoin(self.root_url, url)
				if o.scheme == '':
					url = urljoin('http://', url)

				o = urlparse(url)
				if url.startswith("#"):
					pass
				elif url.startswith("javascript:"):
					pass
				else:
					if o.netloc != '' and o.netloc != self.netloc:
						pass
					elif o.netloc == '':
						if "@" in o.path:
							pass
					else:
						if url not in self.seen_page:
							links.add(url)
							self.seen_page.add(url)
			except KeyError:
				pass

		return list(links)

	def process_full_site(self):
		pass


if __name__ == '__main__':
	root = "https://www.ft.com/content/77d5a928-0a5b-11e8-bacb-2958fde95e5e"
	c = Crawler(root)
	bsObj = c.get_bs_obj()
