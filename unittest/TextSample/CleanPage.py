
from lxml.html import fromstring
from lxml.html import tostring
import sys


from bs4 import BeautifulSoup as Soup





def parse_content(html_doc):
	soup = Soup(html_doc, 'html.parser')
	
	# for tag in soup():
	# 	for attribute in ["class", "id", "name", "style"]:
	# 		del tag[attribute]
	soup = remove_attrs(soup)
	
	return soup.get_text()


def remove_attrs(soup, whitelist=tuple()):
	for tag in soup.findAll(True):
		for attr in [attr for attr in tag.attrs if attr not in whitelist]:
			print(tag[attr])
			del tag[attr]

	return soup



if __name__ == "__main__":
	print("--19970225--")
	print(parse_content(sys.stdin))
	






