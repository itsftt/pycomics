#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
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
		return re.search('<h1 class="new_h2">(.*?)</h1>',page).group(1)

	def getVolumnsUrl(self, url, page, skip=0):
		volumns = re.findall('<a class="tg" href="/(.*?)/" title=".*?">([^<]*?)</a>',page)[::-1]
		return map(lambda (c, n): (c, "%s-%s"%(n.replace('&nbsp;', ' ').split('漫画 ')[-1].strip(), c)), volumns[skip:])

	def comicPath(self, i):
		return '"%s/%s/%s/%s"'%(self.root, self.path(), i[0], i[2])

	def getVolumn(self, (cid, name), force=True):
		if not self.chdir(name) and not force:
			os.chdir('..')
			return
		i = 1
		urls = []
		while True:
			url = 'http://www.dm5.com/%s-p1/chapterfun.ashx?cid=%s&page=%d&key=&language=1&gtk=6'%(cid,cid[1:],i)
			req = urllib2.Request(url)
			req.add_header('Referer', 'http://www.dm5.com/%s/'%cid)
			page = self.urlopen(req).read()
			u = self.execJs("print (%s)"%page).split(',')
			if len(u) > 1:
				i += len(u)
				urls += u
				for url in u:
					self.getPic(url, {'--referer': 'http://www.dm5.com/%s/'%cid,
					'-O': url.rsplit('/',1)[-1].split('?')[0] })
			else:
				if u[0] not in urls:
					urls.append(u[0])
					url = u[0]
					self.getPic(url, {'--referer': 'http://www.dm5.com/%s/'%cid,
					'-O': url.rsplit('/',1)[-1].split('?')[0] })
				break
		os.chdir('..')
		return name

if __name__ == '__main__':
	dm5().getUpdate()
