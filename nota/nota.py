import sys
from os import system, getenv, path, walk, stat, listdir

from utils import *

DEFAULT_CONFIG_FILE = path.join(getenv('HOME'), '.nota', 'config')

DEFAULTS = {
	'extensions':		['.note'],
	'latexmathml':		False,	# depends of latexmathml so off by default
	'latexmathmlurl':	None,	# no url as it's not used
	'header':			None,	# up to the user so off by default
	'toc':				True,	# no dependencies and useful, on by default
	'css':				None,	# needs css file so off
	'tidy':				False,	# needs html tidy utility so off
}

class NotaJob(object):
	
	def __init__(self, force_conversion=False, config_file=DEFAULT_CONFIG_FILE):
		self.force_conversion = force_conversion
		self.config_file = config_file
		self.files = []
		self.dirs = []
		self.opts = DEFAULTS
		self._load_config()

	def add_file(self, filename):
		self.files.append(filename)

	def add_dir(self, dirname):
		self.dirs.append(dirname)
	
	def convert_file(self, filepath):
		outfile = change_ext(filepath, "html")
		command = self._generate_command() % (filepath, outfile)
		system(command)
	
	def convert_dir(self, dirpath):
		for f in listdir(dirpath):
			f = path.join(dirpath, f)
			if path.basename(f).startswith('.'):
				continue
			if path.isdir(f):
				self.convert_dir(f)
			elif path.isfile(f):
				if path.splitext(f)[1] in self.opts['extensions']:
					if self.force_conversion or needs_conversion(f):
						print f
						self.convert_file(f)
	
	def execute(self):
		for dir in self.dirs:
			self.convert_dir(dir)
		for file in self.files:
			self.convert_file(file)
	
	def _generate_command(self):
		cmd = "pandoc "
		
		if self.opts['latexmathml']:
			if self.opts['latexmathmlurl'] == '':
				cmd += "--latexmathml "
			else:
				cmd += "--latexmathml=%s " % latexmathmlurl
		
		if self.opts['header']:
			cmd += "-H %s " % header
		
		if self.opts['toc']:
			cmd += "--toc "
		
		if self.opts['css']:
			cmd += "-c %s " % self.opts['css']
		
		cmd += "\"%s\" "			#the place for the input filename
		
		if self.opts['tidy']:
			cmd += "| tidy -qi "	# (q)uiet errors, and (i)ndent the html
		
		cmd += "> \"%s\"" 			# place for the output filename
		
		return cmd
	
	def _load_config(self):
		for line in open(self.config_file, 'r').readlines():
			if line[0] not in '#\n':
				var, val = [part.strip(" \n") for part in line.split("=")]
				try:
					self.opts[var]=val
					#print var, '=', val
				except:
					raise NotaError, "Option \"%s\" not recognised" % var
