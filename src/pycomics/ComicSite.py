#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
import requests

isPy2 = sys.version_info < (3, 0)


class ComicSite(object):
    encoding = "utf-8"
    header = {
        "User-Agent": "Mozilla/5.0 Gecko/2010 Firefox/5",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-us,en;q=0.5",
        "Accept-Encoding": "deflate",
    }
    root = os.path.expanduser("~")
    os.chdir(root)

    def openTrackList(self):
        p = "%s-tracklist.txt" % self.path()
        if not os.path.exists(p):
            open(p, 'a').close()
        if sys.platform == 'darwin':
            os.system('open %s' % p)
        elif sys.platform == 'win32':
            os.system(p)

    def trackList(self):
        p = "%s-tracklist.txt" % self.path()
        if os.path.exists(p):
            return map(str.strip, open(p).readlines())
        else:
            return []

    def execJs(self, s):
        import subprocess
        import tempfile
        fd, path = tempfile.mkstemp(suffix='.js')
        f = os.fdopen(fd, 'w')
        if sys.platform == 'win32':
            s = s.replace('print', 'WScript.Echo')
        f.write(s)
        f.close()
        if sys.platform == 'darwin':
            jsc_cmd = ("/System/Library/Frameworks/JavaScriptCore.framework/"
                       "Versions/Current/Resources/jsc " + path)
            ret = subprocess.check_output(jsc_cmd, shell=True).decode('utf-8')
        elif sys.platform == 'win32':
            ret = ''.join(os.popen("cscript %s" % path).readlines()[3:]).strip()
        os.remove(path)
        return ret

    def path(self):
        return self.__class__.__name__

    def urlopen(self, url, opts=None):
        for i in range(10):
            try:
                headers = self.header.copy()
                if opts:
                    headers.update(opts)
                r = requests.get(url, headers=headers, timeout=5)
                r.encoding = self.encoding
                return r.text
            except:
                import traceback
                print('??', i, url)
                print(traceback.format_exc())
                import time
                time.sleep(.5)
                pass

    def untag(self, s):
        return re.sub("<.*?>", "", s)

    def chdir(self, p):
        if isPy2 and not type(p) == unicode:
            p = p.decode('utf-8')
        try:
            os.mkdir(p)
            os.chdir(p)
            return True
        except:
            os.chdir(p)
            return False

    def getPic(self, url, opts={}):
        if os.path.exists('/usr/local/bin/wget'):
            for x in range(3):
                if os.system(
                    '/usr/local/bin/wget %s -c "%s"' % (
                        ' '.join(map(lambda i: "%s %s" % i, opts.items())), url)) == 0:
                    break
        else:
            headers = None
            if '--referer' in opts:
                headers = {'Referer': opts['--referer']}
            open(url.rsplit('/', 1)[-1].split('?', 1)[0], 'wb').write(self.urlopen(url, headers))

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

    def getAll(self, url, skip=0, force=True):
        self.chdir(self.path())
        url = self.toUrl(url)
        page = self.urlopen(url)
        volumns = self.getVolumnsUrl(url, page, skip)
        cid = self.getCid(url)
        title = self.getTitle(page)
        self.chdir(title)

        ch = []
        for urlparam in volumns:
            c = self.getVolumn(urlparam, force)
            if c:
                ch.append(c)

        os.chdir('../..')

        for c in ch:
            yield (title, cid, c)

    def notify(self, updateList):
        import pkgutil
        if not pkgutil.find_loader('pync'):
            return
        try:
            import pync
            t = '  '.join(['%s-%s' % (n[0].split()[0], n[2]) for n in updateList])
            cmd = 'open %s -a /Applications/Simple\ Comic.app/' % ' '.join(
                map(self.comicPath, updateList)
            )
            if isPy2:
                t = t.encode('utf8')
                cmd = cmd.encode('utf8')
            pync.Notifier.notify(t, title=self.__class__.__name__, sound='ping', execute=cmd)
        except:
            import traceback
            traceback.print_exc()

    def getUpdate(self):
        updateList = [comic for i in self.trackList() for comic in self.getAll(i, -2, False)]
        if updateList:
            self.notify(updateList)


def main():
    import comic8
    import dm5
    comic8.comic8().getUpdate()
    dm5.dm5().getUpdate()


if __name__ == '__main__':
    main()
