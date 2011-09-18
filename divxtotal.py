#VERSION: 1.1
#AUTHORS: Shiro Hazuki (hazukishiki@mail.com), cdgg (cdgg.cdgg@gmail.com)
#
#                    GNU GENERAL PUBLIC LICENSE
#                       Version 3, 29 June 2007
#
#                   <http://www.gnu.org/licenses/>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

import urllib2, re
from urllib import urlencode

class divxtotal(object):
	url = 'http://divxtotal.com'
	name = 'DivxTotal'
	supported_categories = {'all': '', 'movies': 'peliculas', 'tv': 'series', 'music': 'musica', 'software': 'programas'}

	def __init__(self):
		self.supported_categories = {'all': '', 'movies': 'peliculas', 'tv': 'series', 'music': 'musica', 'software': 'programas'}

	def out(self):
		print ""

	def search(self, what, cat='all'):
		urldata = {
		'busqueda': what
		}
		nextpage = "buscar.php?" + urlencode(urldata)
		while nextpage != False:
			u = urllib2.urlopen("http://divxtotal.com/" + nextpage)

			temp = {
				"link" : -1,
				"name" : -1,
				"size" : -1,
				"seeds" : -1,
				"leech" : -1,
				"engine_url" : "http://divxtotal.com",
				"description" : -1
			}
			nextpage = False
			content = ""
			for line in u.readlines():
				content += line.strip()
			for x in re.split("<li class=\"section_item2?\">",content)[1:-1]:

				# Begin name, link, description
				m = re.match('<p class="seccontnom">(.+)<p class="seccontgen"',x)
				n = re.search("<a href=\"(.+)/torrent/([0-9]+)/(.+)\"(.+)>(.+)</a>",m.group(1))
				temp["description"] = "http://divxtotal.com/" + re.search("<a href=\"(.+)/\"(.+)>(.+)</a>",m.group(1)).group(1) + "/"
				temp["link"] = "http://divxtotal.com/download.php?id={0}".format(
					n.group(2)
				)
				temp["name"] = n.group(5)
				# End name, link, description

				# Begin size
				m = re.search('<p class="seccontfetam">(.+)</p></li>', x)
				if type(re.search("^[0-9\-]+$",m.group(1)))==type(None):
					t = {"GB":1024**3,"MB":1024**2,"KB":1024,"B":1}
					n = re.search("([0-9\.]+) (.+)",m.group(1))
					s = int(float(n.group(1))*t[n.group(2)])
					temp["size"] = s
				# End size

				# Begin category
				m = re.search('<p class="seccontgen">(.+)</p><p class="seccontfetam', x)
				n = re.search("<a href=\"(.+)/\"(.+)</a>",m.group(1)).group(1)
				if cat=="all" or n==self.supported_categories[cat]:
					print_this = True
				# End category

				if print_this:
					print "{0}|{1}|{2}|{3}|{4}|{5}|{6}".format(temp["link"],temp["name"],temp["size"],temp["seeds"],temp["leech"],temp["engine_url"],temp["description"])
					print_this = False

			m = re.search("<a href='([A-z0-9\-\&\=\+\?\.]+)'>Siguiente >>", re.split("<div class=\"pagination\">",content)[-1])
			if type(m)!=type(None):
				nextpage = m.group(1)
