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

import urllib2, re, string
from urllib import urlencode

class torrentz(object):
	url = 'http://torrentz.eu'
	name = 'Torrentz'
	supported_categories = {'all': ''}

	def search(self, what, cat='all'):
		nextpage = "search?" + urlencode({'f': what})
		while nextpage != False:
			u = urllib2.urlopen("http://torrentz.eu/{0}".format(nextpage))
			c = ""
			for line in u:
				c += line.strip("\n")
			m = re.search("<div class=\"results\">(.+)</div><div class=\"help\">",c)
			c = m.group(1)
			l = string.split(c,"<dl>")[1:]
			temp = string.split(l[-1],"</dl>")
			l[-1] = temp[0]
			p = temp[1]
			nextpage = False
			m = re.search("<a href=\"/([a-zA-Z0-9\%\&\;\+\?\=]+)\">Next \&raquo\;</a>",p)
			if type(m)!=type(None):
				nextpage = m.group(1).replace("&amp;","&")
			pattern1 = "<dt(.*)><a href=\"/([a-zA-Z0-9]+)\">(.+)</a>"
			pattern2 = "<span class=\"s\">(.+)</span> <span class=\"u\">(.+)</span> <span class=\"d\">(.+)</span></dd>"
			temp = {
				"link"        : -1,
				"name"        : -1,
				"size"        : -1,
				"seeds"       : -1,
				"leech"       : -1,
				"engine_url"  : "http://torrentz.eu",
				"description" : -1
			}
			link = [
				"http://www.torrenthound.com/torrent/{0}",
				"http://h33t.com/download.php?id={0}",
				"http://torrage.com/torrent/{0}.torrent",
				"http://torcache.com/torrent/{0}.torrent",
				"http://zoink.it/torrent/{0}.torrent"
			]
			m = None
			for line in l:
				m = re.match(pattern1,line)
				temp["description"] = "{0}/{1}".format(temp["engine_url"],m.group(2))
				nomatch = True
				for x in link:
					temp["link"] = x.format(m.group(2))
					try:
						urllib2.urlopen(temp["link"])
						nomatch = False
						break
					except:
						pass
				if nomatch==True:
					continue
				temp["name"] = re.sub("<(b|B)>|</(b|B)>","",m.group(3))
				m = re.search(pattern2,line)
				temp["seeds"] = m.group(2).replace(",","")
				temp["leech"] = m.group(3).replace(",","")
				t = {"Gb":1024**3,"Mb":1024**2,"Kb":1024,"B":1,"b":1}
				n = re.search("([0-9,.]+) (.+)",m.group(1))
				try:
					s = int(float(n.group(1))*t[n.group(2)])
					temp["size"] = s
				except:
					pass
				print "{0}|{1}|{2}|{3}|{4}|{5}|{6}".format(temp["link"],temp["name"],temp["size"],temp["seeds"],temp["leech"],temp["engine_url"],temp["description"])
				temp = {
					"link"        : -1,
					"name"        : -1,
					"size"        : -1,
					"seeds"       : -1,
					"leech"       : -1,
					"engine_url"  : "http://torrentz.eu",
					"description" : -1
				}
			u.close()
