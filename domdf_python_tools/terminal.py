#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  terminal.py
"""
Useful functions for terminal-based programs
"""
#
#  Copyright © 2014-2019 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  get_terminal_size, _get_terminal_size_windows, _get_terminal_size_tput and _get_terminal_size_linux
# 		from https://gist.github.com/jtriley/1108174
#  		Copyright © 2011 jtriley
#
#  Parts of the docstrings based on the Python 3.8.2 Documentation
#  Licensed under the Python Software Foundation License Version 2.
#  Copyright © 2001-2020 Python Software Foundation. All rights reserved.
#  Copyright © 2000 BeOpen.com . All rights reserved.
#  Copyright © 1995-2000 Corporation for National Research Initiatives . All rights reserved.
#  Copyright © 1991-1995 Stichting Mathematisch Centrum . All rights reserved.
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# stdlib
import os
import platform
import shlex
import struct
import subprocess
import sys


def clear():
	"""
	Clear the display
	
	works for Windows and UNIX, but does not clear Python Interpreter
	
	:return:
	"""
	
	return os.system('cls' if os.name == 'nt' else 'clear')
	

def br():
	"""
	Prints a line break
	"""
	
	print("")



def interrupt():
	"""
	Print what to do to abort the script; dynamic depending on OS
	Useful when you have a long-running script that you might want t interrupt part way through
	"""
	
	print(f"(Press Ctrl-{'C' if os.name == 'nt' else 'D'} to quit at any time.)")


def overtype(*objects, sep=' ', end='', file=sys.stdout, flush=False):
	"""
	Print `objects` to the text stream `file`, starting with "\r", separated by `sep` and followed by `end`.
	`sep`, `end`, `file` and `flush`, if present, must be given as keyword arguments

	All non-keyword arguments are converted to strings like ``str()`` does and written to the stream,
	separated by `sep` and followed by `end`.

	If no objects are given, ``overtype()`` will just write "\r".

	TODO: This does not currently work in the PyCharm console, at least on Windows

	:param objects:
	:param sep: String to separate the objects with, by default " "
	:type sep: str
	:param end: String to end with, by default nothing
	:type end: str
	:param file: An object with a ``write(string)`` method; default ``sys.stdout``
	:param flush: If true, the stream is forcibly flushed.
	:type flush: bool
	:return:
	"""
	
	object0 = f"\r{objects[0]}"
	objects = (object0, *objects[1:])
	print(*objects, sep=sep, end=end, file=file, flush=flush)


def get_terminal_size():
	"""
	Get width and height of console
	
	Works on linux,os x,windows,cygwin(windows)
	
	Originally retrieved from: http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
	
	:return: tuple_xy
	"""
	
	current_os = platform.system()
	tuple_xy = None
	if current_os == 'Windows':
		tuple_xy = _get_terminal_size_windows()
		if tuple_xy is None:
			tuple_xy = _get_terminal_size_tput()
		# needed for window's python in cygwin's xterm!
	if current_os in ['Linux', 'Darwin'] or current_os.startswith('CYGWIN'):
		tuple_xy = _get_terminal_size_linux()
	if tuple_xy is None:
		print("default")
		tuple_xy = (80, 25)      # default value
	return tuple_xy


def _get_terminal_size_windows():
	try:
		from ctypes import windll, create_string_buffer
		# stdin handle is -10
		# stdout handle is -11
		# stderr handle is -12
		h = windll.kernel32.GetStdHandle(-12)
		csbi = create_string_buffer(22)
		res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
		if res:
			(buf_x, buf_y, cur_x, cur_y, wattr,
			 left, top, right, bottom,
			 maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
			size_x = right - left + 1
			size_y = bottom - top + 1
			return size_x, size_y
	except:
		pass


def _get_terminal_size_tput():
	# get terminal width
	# src: http://stackoverflow.com/questions/263890/how-do-i-find-the-width-height-of-a-terminal-window
	try:
		cols = int(subprocess.check_call(shlex.split('tput cols')))
		rows = int(subprocess.check_call(shlex.split('tput lines')))
		return cols, rows
	except:
		pass


def _get_terminal_size_linux():
	def ioctl_GWINSZ(fd):
		try:
			import fcntl
			import termios
			cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
			return cr
		except:
			pass
	cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
	if not cr:
		try:
			fd = os.open(os.ctermid(), os.O_RDONLY)
			cr = ioctl_GWINSZ(fd)
			os.close(fd)
		except:
			pass
	if not cr:
		try:
			cr = (os.environ['LINES'], os.environ['COLUMNS'])
		except:
			return None
	return int(cr[1]), int(cr[0])


if __name__ == "__main__":
	size_x, size_y = get_terminal_size()
	print('width =', size_x, 'height =', size_y)
