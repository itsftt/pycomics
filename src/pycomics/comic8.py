#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import requests
from .ComicSite import ComicSite


class comic8(ComicSite):

    def __init__(self):
        jsfile = self.urlopen('http://www.comicbus.com/js/comicview.js')
        self.js = (jsfile.replace('window.open', 'return baseurl+url;//')
                         .replace('if(getCookie', '//'))
        self.encoding = "cp950"

    def toUrl(self, url):
        if type(url) == int:
            return 'http://www.comicbus.com/html/%d.html' % url
        elif not url.startswith('http'):
            return 'http://www.comicbus.com/html/%s.html' % url
        else:
            return url

    def comicPath(self, i):
        return '"%s/%s/%s/%s-%s"' % (self.root, self.path(), i[0], i[1], i[2])

    def getTitle(self, page):
        return self.untag(
            re.search(u'<title>(.*?)漫畫,(.*?)</title>', page, re.DOTALL)
            .group(1)).strip().replace('\r', '').replace('\n', '')

    volumnJs = '''var y=46;function lc(l){if(l.length!=2 ) return l;var az="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";var a=l.substring(0,1);var b=l.substring(1,2);if(a=="Z") return 8000+az.indexOf(b);else return az.indexOf(a)*52+az.indexOf(b);}function su(a,b,c){var e=(a+'').substring(b,b+c);return (e);}
function nn(n){return n<10?'00'+n:n<100?'0'+n:n;}
function ss(a,b,c,d){var e=a.substring(b,b+c);return d==null?e.replace(/[a-z]*/gi,""):e;}
function mm(p){return (parseInt((p-1)/10)%10)+(((p-1)%10)*3)}'''

    def getVolumn(self, url, force=True):
        def nn(n):
            return '00%d' % n if n < 10 else ('0%d' % n if n < 100 else n)

        def ss(a, b, c, d=None):
            e = a[int(b):int(b) + int(c)]
            return re.sub("[a-z]*", '', e) if not d else e

        def mm(p):
            return ((p - 1) / 10) % 10 + ((p - 1) % 10) * 3

        if '-' in url:
            ti = int(url.split('.')[-2].split('-')[-1])
        elif '_' in url:
            ti = int(url.split('.')[-2].split('_')[-1])
        ch = url.split('=')[-1].strip()
        f = 50

        if not self.chdir('%d-%s' % (ti, ch)) and not force:
            os.chdir('..')
            return

        page = requests.get(url).text
        picsjs = re.search('var chs=.*break; }}', page)
        if not picsjs:
            cs = re.search("cs='([^']*)", page).group(1)

            cc = len(cs)
            c = ss(cs, cc - f, f)
            for i in range(cc // f):
                if ss(cs, i * f, 4) == ch:
                    c = ss(cs, i * f, f, f)
                    ci = i
                    break
            ps = int(ss(c, 7, 3))

            e = 0
            for p in range(1, ps + 1):
                url = 'http://img%s.6comic.com:99/%s/%d/%s/%s_%s.jpg' % (
                    ss(c, 4, 2), ss(c, 6, 1), ti, ss(c, 0, 4), nn(p), ss(c, mm(p) + 10, 3, f))
                self.getPic(url)
        else:
            picsjs = (picsjs.group(0)
                      .replace("ge('TheImg').src = ", "for(p=1;p<=ps;p++){print(")
                      .replace("jpg';", "jpg')};"))
            for url in self.execJs(self.volumnJs + 'var ch=%s;' % ch + picsjs).split('\n'):
                self.getPic(url)
        os.chdir('..')
        return ch

    def getCid(self, url):
        return url.split('.')[-2].split('/')[-1]

    def getVolumnsUrl(self, url, page, skip=0):
        chs = re.findall("cview.'([^.]*).html',([0-9]*),([0-9]).", page)
        v = [c for c in chs if int(c[0].split('-')[-1]) < 8000]
        s = [c for c in chs if int(c[0].split('-')[-1]) > 7999]

        for no, catid, copyright in v[skip:] + s[skip:]:
            yield self.execJs(self.js + "\nprint(cview('%s',%s,%s));" % (no, catid, copyright))


if __name__ == '__main__':
    c = comic8()
    c.getUpdate()
