#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import re
from ComicSite import *

class dm5(ComicSite):
	ComicSite.opener.addheaders.append(('Cookie', 'isAdult=1'))

	def toUrl(self, url):
		if url.startswith('http'):
			return url
		else:
			return 'http://www.dm5.com/%s/'%url

	def getCid(self, url):
		return url.strip('/').split('/')[-1]

	def getTitle(self, page):
		return re.search('var DM5_COMIC_MNAME="(.*?)"', page).group(1)

	def getVolumnsUrl(self, url, page, skip=0):
		volumns = re.findall('<li><a href="/(m[0-9]*)/"[^>]*?>([^<]*?)<', page)[::-1]
		return map(lambda (c, n): (c, "%s-%s"%(n.replace('&nbsp;', ' ').split()[0].strip(), c)), volumns[skip:])

	def comicPath(self, i):
		return '"%s/%s/%s/%s"'%(self.root, self.path(), i[0], i[2])

	def getVolumn(self, (cid, name), force=True):
		if not self.chdir(name) and not force:
			os.chdir('..')
			return
		page = self.urlopen('http://www.dm5.com/%s/'%cid).read()
		CID = re.search('DM5_CID=([0-9]*);', page).group(1)
		MID = re.search('DM5_MID=([0-9]*);', page).group(1)
		DT = re.search('DM5_VIEWSIGN_DT="([^"]*)"', page).group(1)
		SIGN = re.search('DM5_VIEWSIGN="([^"]*)"', page).group(1)
		pcount = int(re.search('DM5_IMAGE_COUNT=([0-9]*);', page).group(1))

		p = 1
		while p<=pcount:
			params = urllib.urlencode({'cid':CID, 'page':p, 'key':'', 'language':'1', 'gtk':'6', '_cid':CID, '_mid':MID, '_dt':DT, '_sign':SIGN})
			url = 'http://www.dm5.com/%s/chapterfun.ashx?%s'%(cid, params)
			req = urllib2.Request(url)
			req.add_header('Referer', 'http://www.dm5.com/%s/'%cid)
			page = self.urlopen(req).read()
			u = self.execJs("print (%s)"%page).split(',')
			for url in u:
				self.getPic(url, {'--referer': 'http://www.dm5.com/%s/'%cid,
				'-O': url.rsplit('/',1)[-1].split('?')[0] })
			p += len(u)
		os.chdir('..')
		return name

if __name__ == '__main__':
	dm5().getUpdate()
