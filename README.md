# pycomics
A simple comic downloader for http://www.dm5.com/ and http://www.comicbus.com/

Support Mac and Windows.

Installation
------------

```
pip install git+https://github.com/itsftt/pycomics.git
```
or

```
git clone git://github.com/itsftt/pycomics.git
cd pycomics
python setup.py install
```

Usage
-----

```
$pycomics -h
usage: pycomics [-h] [-o dm5/comic8] [-u] [-d url skip [url skip ...]]

optional arguments:
  -h, --help            show this help message and exit
  -o dm5/comic8         Open track list
  -u                    Update comics in track list
  -d url skip [url skip ...]
                        Download comic (default skip=0)
```
