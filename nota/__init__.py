from nota import NotaJob, DEFAULTS, DEFAULT_CONFIG_FILE

VERSION = '0.1'

def convert_file(filepath):
	job = NotaJob()
	job.add_file(filepath)
	job.execute()

def convert_dir(dirpath):
	job = NotaJob()
	job.add_dir(dirpath)
	job.execute()
