import copy

google_bot_user_agent = str("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")
default_browser_user_agent = ""



headers = {
	"User-Agent": google_bot_user_agent,
	"Referer": "http://www.google.com/",
	"Accept-Encoding": "gzip, deflate, sdch",
	"Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,fr;q=0.2"
}

HEADERS = {
	"User-Agent": "",
	"Referer": "",
	"Accept-Encoding": "",
	"Accept-Language": "",
}


class CrawlerSettings:
	@staticmethod
	def get_default_headers():
		tmp_heapers = copy.deepcopy(HEADERS)
		tmp_heapers['User-Agent'] = default_browser_user_agent
		tmp_heapers['Referer'] = "https://www.google.com"
		return tmp_heapers

	@staticmethod
	def get_post_form():
		return {}

	@staticmethod
	def get_redirect_code():
		return {301, 302, 307}
