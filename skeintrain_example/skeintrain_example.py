import json
import re
#logging.basicConfig(format="%(funcName)s %(message)s")

class BaseTransform():
	""" Example Base Transform Class"""	
	
	# -- Yield is required 
	yield_callback = None
	""" Base transform module """
	def __init__(self):
		""" Python init function"""
		print 'init base transform'

	def setup(self, inDict):
		""" setup function takes a dict of objects to 
		use in setup/control """
		if not 'yield_callback' in inDict:
			print 'no yield callback set'
			return -4 #TODO: better return policy later
		else:
			self.yield_callback = inDict['yield_callback']
			print 'set yield callback of ' + repr(self.yield_callback) 
		return 0
	
	def interrogate():
		print 'return base info on what this takes/gives'

	def queue(self,atom ):
		print 'insert an atom of something in the work queue'

	def cleanup(self):
		print 'cleanup. May foe a yeild of in the middle of processing, and a close of that processing is available/possible'


class LineCombineTransform(BaseTransform):
	""" Line Combine Transform. Example Transform Engine"""
	info = { 'name':'LineCombineTransform',
			 'description':'Combines gcode layers',
			  #TOOD: add 'setup' to indicate dict values for setup 
			 'input': { 
				 'atom':"<type 'str'>", 
				 'min': 2, 'max': 2, },
			 'output' : { 
				'atom':"<type 'str'>",
				'min':1, 'max':1 },
		}
	data = None

	def __init__(self):	
		self.data = []	
		
	def setup(self, inDict):
		""" Sets up a Transform for a run."""
		self.data = [] 
		if 'yield_callback' in inDict:
			print 'foo'
			self.yield_callback = inDict['yield_callback']
#			print 'set yield callback of ' + repr(self.yield_callback) 
		else :
			'no yield callback set'
			return -4 #TODO: better return policy later
		print "LineCombineTransform setup complete"
		return 0

	@classmethod
	def interrogate(self):
		return json.dumps(self.info)
	
	def queue(self,atom_type, atom ):
		print 'insert an atom of something in the work queue'
		if self.info == None : 
			print 'failsauce' 
			return -6
		if self.info['input']['atom'] != atom_type:
			return 'atom mismatch'
			return -5
		print 'appending' + repr(atom)
		self.data.append(atom)
	
		if(self.yield_callback == None):
			print "no yield callback Registered"
			return -7 #TODO: decide on a better return policy
		elif (self.can_yield() ):
			print 'yielded'
			print 'yeilding to: ', repr(self.yield_callback)
			self.yield_callback(self.info['output']['atom'], '\n'.join(self.data))
			return 0 
		return 0

	def can_yield(self):
		if len(self.data) >= 2:
			return True
		return False

	# parent does this, don't forget
	#def register_yield_callback(self, yield_callback):

	def cleanup(self):
		print 'cleanup. May force a yeild of in the middle of processing, and a close of that processing is available/possible'


class RegexTransform(BaseTransform):
	""" Line Combine Transform. Example Transform Engine"""
		#TOOD: add 'setup' to indicate dict values for setup 
	info = { 'name':'RegexTransform',
		'description':'Runs a regular expression',
		'input': { 
			 'atom':"<type 'str'>", 
			 'min': 1, 'max': None, },
		 'output' : { 
			'atom':"<type 'str'>",
			'min':1, 'max':None },
		}
	regexDict = {}

	def __init__(self):	
		pass
	
	def setup(self, inDict):
		""" Sets up a Transform for a run."""
		if 'yield_callback' in inDict:
			print 'foo'
			self.yield_callback = inDict['yield_callback']
#			print 'set yield callback of ' + repr(self.yield_callback) 
		else :
			print 'no yield callback set'
			return -4 #TODO: better return policy later

		if 'regex_sub' in inDict:
			self.regexDict = inDict['regex_sub'];
		
		print "RegexTransform setup complete"
		return 0

	@classmethod
	def interrogate(self):
		return json.dumps(self.info)
	
	def queue(self,atom_type, atom ):
		print 'insert an atom of something in the work queue'
		if self.info == None : 
			print 'failsauce' 
			return -6
		if self.info['input']['atom'] != atom_type:
			return 'atom mismatch'
			return -5
		if(self.yield_callback == None):
			print "no yield callback Registered"
			return -7 #TODO: decide on a better return policy
		print 'yielded'
		print 'yeilding to: ', repr(self.yield_callback)
		print self.regexDict['out']
		print self.regexDict['in']
		print atom
		output = re.sub(self.regexDict['in'],self.regexDict['out'], atom)
		self.yield_callback(self.info['output']['atom'],output )		
		return 0


	# parent does this, don't forget
	#def register_yield_callback(self, yield_callback):

	def cleanup(self):
		print 'cleanup. May force a yeild of in the middle of processing, and a close of that processing is available/possible'

def yielder(atom_type, atom):
	print 'atom type: ' + repr(atom_type)
	print 'atom: ' + repr(atom)	
	
if __name__ == "__main__":
	print 'main '

	# -- Example of a Base Transform base class	
	step =  BaseTransform()
	print "BaseTransform " + repr(step) 

	# -- Example of a combine 2 atoms class
	print "interrogate"
	print LineCombineTransform.interrogate()
	
	step2 = LineCombineTransform()

	step2.setup({'yield_callback':yielder})
	print 'setup done'
	
	step2.queue("<type 'str'>","bla blah blah")
	step2.queue("<type 'str'>","car cala claw")

	#example of a transorm one atom class
	step3 = RegexTransform()
	step3.setup({'yield_callback':yielder, 'regex_sub':{'in':'[bc]','out':'z'}})

	step3.queue(str(type("str")), "car car car")
