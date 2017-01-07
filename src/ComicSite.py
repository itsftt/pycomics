#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import sys
import re
import os

class ComicSite(object):
	opener = urllib2.build_opener()
	root = os.path.expanduser("~")
	os.chdir(root)

	def openTrackList(self):
		p = "%s-tracklist.txt"%self.path()
		os.system('open %s'%p)
		
	def trackList(self):
		p = "%s-tracklist.txt"%self.path()
		if os.path.exists(p):
			return map(str.strip, open(p).readlines())
		else:
			return []

	def execJs(self, s):
		import tempfile, commands
		fd, path = tempfile.mkstemp(suffix='.js')
		f = os.fdopen(fd, 'w')
		f.write(s)
		f.close()
		ret = commands.getoutput("/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Resources/jsc %s"%path)
		os.remove(path)
		return ret

	def path(self):
		return self.__class__.__name__

	def urlopen(self, url):
		for i in range(10):
			try:
				print url
				r = self.opener.open(url,timeout=5)
				return r
			except:
				print sys.exc_info()
				print '?', i , url
				pass

	def untag(self, s):
		return re.sub("<.*?>", "", s);

	def chdir(self, p):
		try:
			os.mkdir(p)
			os.chdir(p)
			return True
		except:
			os.chdir(p)
			return False
		
	def getPic(self, url, opts=''):
		for x in range(3):
			if os.system('/usr/local/bin/wget %s -c "%s"'%(opts, url)) == 0:
				break
	
	def comicPath(self, i):
		return

	def toUrl(self, url):
		return
	def getCid(self, url):
		return
	def getTitle(self, page):
		return
	def getVolumnsUrl(self, url, page, skip=0):
		return
	def getVolumn(self, url, force=True):
		return

	def getAll(self, url,skip=0,force=True):
		self.chdir(self.path())
		url = self.toUrl(url)
		page = self.urlopen(url).read()
		volumns = self.getVolumnsUrl(url, page, skip)
		cid = self.getCid(url)
		title = self.getTitle(page)
		self.chdir(title)
		ch = []
		for url in volumns:
			c = self.getVolumn(url, force)
			if c:
				ch.append(c)
		os.chdir('../..')
		return [(title, cid, c) for c in ch]
	
	def notify(self, updateList):
		import pkgutil
		if not pkgutil.find_loader('pync'):
			return
		try:
			import pync
			t = '  '.join(['%s-%s'%(n[0].split()[0],n[2]) for n in updateList])
			if type(t) == unicode:
				t = t.encode('utf8')
			pync.Notifier.notify(t, title=self.__class__.__name__, sound = 'ping', execute='open %s -a /Applications/Simple\ Comic.app/'%' '.join(map(self.comicPath, updateList)))
		except:
			import traceback
			traceback.print_exc()

	def getUpdate(self):
		updateList = filter(None, sum([self.getAll(i, -2, False) for i in self.trackList()], []))
		if len(updateList) > 0:
			self.notify(updateList)

def main():
	import comic8, dm5
	comic8.comic8().getUpdate()
	dm5.dm5().getUpdate()

if __name__ == '__main__':
	main()
