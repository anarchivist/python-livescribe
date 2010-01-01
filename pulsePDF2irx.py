#!/usr/bin/env python
# encoding: utf-8
#Created by  on 2008-02-27.

# Copyright (C) 2008 Graham I Cummins
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA 02111-1307 USA
#

docstring='''This version of the script expects to use pstoedit version 3.45 '''

import os, re


PSTOEDIT = '"c:\\Program Files\\pstoedit\\pstoedit.exe"'
XMLDECLARATION = '''

<stroke layer="0" linestyle="solid" pensize="3" color="#000000">2.97 8.632 0
'''

def convert(bfn):
	os.system('%s -f mpost %s %s' % (PSTOEDIT, bfn+'.pdf', bfn+'.mp'))
	lines=open(bfn+'.mp').readlines()
	os.unlink(bfn+'.mp')
	pages = []
	lsplit = re.compile("\s*--\s*")
	drawing = False
	for l in lines:
		if 'beginfig' in l:
			pages.append([])
			drawing=False
			continue
		if l.startswith('draw '):
			drawing=True
			pages[-1].append([])
			l=l.lstrip('draw ')
		if drawing:
			drawing = not(l.strip().endswith(';'))
			l=lsplit.split(l.strip("\t\r\n- ;"))
			pages[-1][-1].extend(map(eval, l))

	return pages


def getPageSize(p):
	w=10
	h=10
	for s in p:
		for pt in s:
			if pt[0]>w:
				w=pt[0]
			if pt[1]>h:
				h=pt[1]
	w+=20
	h+=20
	return (w, h)


def writeirx(pages, fn):
	f=open(fn, 'wb')
	f.write('<?xml version="1.0" encoding="utf-8"?>\n')
	f.write('<notes><version><number>1.0</number><orgnization>iRex Technologies</orgnization></version><screen><units>px</units><dpi>160</dpi></screen>\n<pages>\n')
	for page in pages:
		w, h = getPageSize(page)
		f.write('<page id="auto" backgroundcolor="#000000"><orientation>0</orientation><height>%i</height><width>%i</width><strokes>\n' % (h,w))
		for stroke in page:
			f.write('<stroke layer="0" linestyle="solid" pensize="3" color="#000000">')
			for pt in stroke:
				f.write('%.2f %.2f 0\n' % (pt[0], h-pt[1]))
			f.write('</stroke>\n')
		f.write('</strokes></page>\n')
	f.write('</pages></notes>\n')
	f.close()


if __name__=='__main__':
	import sys
	if len(sys.argv)<2:
		print 'usage: pulsePDF2irx.py fname.pdf'
		sys.exit()
	fname = sys.argv[1]

	bfn=os.path.splitext(fname)[0]
	pages = convert(bfn)
	writeirx(pages, bfn+'.irx')


