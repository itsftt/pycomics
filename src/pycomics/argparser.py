import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-o", help="Open track list", metavar="dm5/comic8")
parser.add_argument("-u", help="Update comics in track list", action="store_true")
parser.add_argument("-d", help="Download comic (default skip=0)", metavar="url skip", nargs='+')
args = parser.parse_args()
