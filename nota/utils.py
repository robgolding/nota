from os import path

class NotaError(Exception): pass

def change_ext(name, newext):
	if newext[0] == '.':
		newext = newext[1:]
	return "%s.%s" % (path.splitext(name)[0], newext)

def needs_conversion(filepath):
	if path.exists(_change_ext(filepath,"html")) \
		and (stat(filepath).st_ctime <= stat(_change_ext(filepath,"html")).st_ctime):
			return False
	else:
		return True
