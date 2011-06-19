#VERSION: 1.00
#AUTHORS: cdgg (cdgg.cdgg@gmail.com), Shiro Hazuki (hazukishiki@mail.com)
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

class divxtotal(object):
  url = 'http://divxtotal.com'
  name = 'DivxTotal'
  supported_categories = {'all': '', 'movies': 'peliculas', 'tv': 'series', 'music': 'musica', 'software': 'programas'}
  
  def __init__(self):
    self.supported_categories = {'all': '', 'movies': 'peliculas', 'tv': 'series', 'music': 'musica', 'software': 'programas'}
  
  def search(self, what, cat='all'):
    nextpage = "buscar.php?busqueda={0}".format(what)
    while nextpage != False:
      u = urllib2.urlopen("http://divxtotal.com/{0}".format(nextpage))
      temp = {
        "link" : -1,
        "name" : -1,
        "size" : -1,
        "seeds" : -1,
        "leech" : -1,
        "engine_url" : "http://divxtotal.com"
      }
      flag = 0
      pos = 0
      nextpage = False
      o = 0
      for line in u:
        if pos==2:
          m = re.search("<a href='(.+)'>Siguiente >>",line)
          if type(m)!=type(None):
            nextpage = m.group(1)
            break
        if pos==1 and line.strip()=="</ul>":
          pos = 2
        if flag==0:
          m = re.search("<li class=\"section_item([0-9]*)\">",line)
          if type(m)!=type(None):
            flag = 1
            pos = 1
        else:
          if line.strip()=="</li>":
            flag = 0
            if o==1:
              print "{0}|{1}|{2}|{3}|{4}|{5}".format(temp["link"],temp["name"],temp["size"],temp["seeds"],temp["leech"],temp["engine_url"])
              o = 0
            temp = {
              "link" : -1,
              "name" : -1,
              "size" : -1,
              "seeds" : -1,
              "leech" : -1,
              "engine_url" : "http://divxtotal.com"
            }
          else:
            m = re.search("<p class=\"(.{9,13})\">(.+)</p>",line)
            if m.group(1)=="seccontnom":
              n = re.search("<a href=\"(.+)/torrent/([0-9]+)/(.+)\"(.+)>(.+)</a>",m.group(2))
              temp["link"] = "http://divxtotal.com/download.php?id={0}".format(
                n.group(2)
              )
              temp["name"] = n.group(5)
            elif m.group(1)=="seccontfetam":
              if type(re.search("^[0-9-]+$",m.group(2)))==type(None):
                t = {"GB":1024**3,"MB":1024**2,"KB":1024,"B":1}
                n = re.search("([0-9.]+) (.+)",m.group(2))
                s = int(float(n.group(1))*t[n.group(2)])
                temp["size"] = s
            elif m.group(1)=="seccontgen":
              n = re.search("<a href=\"(.+)/\"(.+)</a>",m.group(2)).group(1)
              if cat=="all" or n==self.supported_categories[cat]:
                o = 1
      u.close()
