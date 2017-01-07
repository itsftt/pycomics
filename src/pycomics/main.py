#!/usr/bin/env python
# -*- coding: utf-8 -*-

def main():
	from argparser import args, parser
	from dm5 import dm5
	from comic8 import comic8
	dm5 = dm5()
	comic8 = comic8()
	
	if args.u:
		dm5.getUpdate()
		comic8.getUpdate()
	elif args.o:
		if dm5.path() == args.o:
			dm5.openTrackList()
		elif comic8.path() == args.o:
			comic8.openTrackList()
	elif args.d:
		i = 0
		while i < len(args.d):
			c = dm5 if 'dm5' in args.d[i] else comic8
			if i+1 < len(args.d)  and args.d[i+1][-1:].isdigit():
				c.getAll(args.d[i], int(args.d[i+1]))
				i += 1
			else:
				c.getAll(args.d[i])
			i += 1
	else:
		parser.print_help()
		parser.exit()


if __name__ == '__main__':
	main()
