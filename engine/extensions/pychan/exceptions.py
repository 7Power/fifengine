# coding: utf-8

class PyChanException(Exception):
	"""
	Base exception class for PyChan.
	All exceptions raised by PyChan derive from this.
	"""
	pass

class InitializationError(PyChanException):
	"""
	Exception raised during the initialization.
	"""
	pass

class RuntimeError(PyChanException):
	"""
	Exception raised during the run time - for example caused by a missing name attribute in a XML file.
	"""
	pass