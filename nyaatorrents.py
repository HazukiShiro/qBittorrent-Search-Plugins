#VERSION: 1.0
#AUTHORS: Shiro Hazuki (hazuki.shiro@gmail.com)
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
#
'NyaaTorrents plug-in for qBittorrent'

import re
import string
import urllib2
from urllib import urlencode

class nyaatorrents(object):
	url  = 'http://www.nyaa.eu'
	name = 'NyaaTorrents'

	# The 'music' category has 2 items because NyaaTorrents divides
	# it in 'Lossy Audio' (e.g. MP3) and 'Lossless Audio' (e.g. MKA).
	supported_categories = {
		'all'       : ['0_0'],
		'music'     : ['3_0','33_0'],
		'anime'     : ['1_0'],
		'software'  : ['6_0'],
		'pictures'  : ['4_0'],
		'books'     : ['2_0'],
	}

	out = [-1]*7
	(LINK,NAME,SIZE,SEEDS,LEECH,ENGINE_URL,DESCRIPTION) = range(0,7)

	MULTIPLIERS = {
		'B'   : 1,
		'KiB' : 1024,
		'MiB' : 1024**2,
		'GiB' : 1024**3,
		'TiB' : 1024**4,
	}

	def reset(self):
		self.out = [-1]*7
		self.out[self.ENGINE_URL] = self.url

	def put(self):
		print '|'.join([str(x) for x in self.out])
		self.reset()

	def getpageurl(self, what, cat, page):
		return '?' + urlencode((
			('page', 'search'),
			('cats', cat),
			('filter', '0'),
			('offset', page),
		)) + '&term=' + what

	def __init__(self):
		self.reset()

	def search(self, what, cat='all'):
		for current_category in self.supported_categories[cat]:
			last_page     = 0
			current_page  = 1
			nextpage      = self.getpageurl(what, current_category, current_page)

			while nextpage!=False:
				u = urllib2.urlopen(self.url + nextpage)

				html = ""
				for line in u:
					html += line.strip()
				u.close()

				html            = string.split(html, 'tr class="pages"')[1]
				pages, torrents = string.split(html, '</table')[0:2]
				torrents        = string.split(torrents, '<tr')[2:]

				# Searches for last page
				if last_page==0:
					match = re.search('offset=([0-9]+)">&gt;&gt;</a>', pages)
					if match!=None:
						last_page = int(match.group(1))

				for x in torrents[:1]+torrents[2:]:
					(
						infoUrlAndName,
						dummy,          # This is never used
						size,
						seed,
						leech
					) = string.split(x, '</td')[1:6]

					# Description link and torrent name
					match = re.search('<a href="(.+)">(.+)</a>', infoUrlAndName)
					if match==None:
						self.reset()
						continue
					(
						self.out[self.DESCRIPTION],
						self.out[self.NAME]
					) = (match.group(1).replace('&amp;','&'),match.group(2))

					# Replaces some HTML entities
					for i in range(33,48):
						self.out[self.NAME] = self.out[self.NAME].replace('&#{};'.format(i),chr(i))
					self.out[self.NAME] = self.out[self.NAME].replace('|','-')

					# Download link
					self.out[self.LINK] = self.out[self.DESCRIPTION].replace('torrentinfo','download')

					# Seeds
					match = re.search('>([0-9\.]+)', seed)
					if match==None:
						self.reset()
						continue
					self.out[self.SEEDS] = int(match.group(1))

					# Leech
					match = re.search('>([0-9\.]+)', leech)
					if match==None:
						self.reset()
						continue
					self.out[self.LEECH] = int(match.group(1))

					# Torrent size
					match = re.search('>([0-9\.]+) ([a-zA-Z]+)', size)
					if match==None:
						self.reset()
						continue
					tsize = float(match.group(1)) * self.MULTIPLIERS[match.group(2)]
					self.out[self.SIZE] = int(tsize) if tsize%1==0 else int(tsize)+1

					# Print the current torrent's information
					self.put()

				if current_page<last_page:
					current_page += 1
					nextpage      = self.getpageurl(what,current_category,current_page)
				else:
					nextpage = False
