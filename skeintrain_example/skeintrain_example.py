import json



class BaseTransform():
	
	yield_callback = None
	""" Base transform module """
	def __init__(self):
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
	info = { 'name':'GCodeCombineTransform',
			 'description':'Combines gcode layers',
			 'input_atom':"<type 'str'>", 
			 'input_min': 2,
			 'input_max': 2,
			 'output_atom':"<type 'str'>",
			 'output_min':1,
			 'output_max':1 }
	""" Combines 2 Gcode files """
	data = None

	def __init__(self):	
		self.data = []	
		print "init"
		
	def setup(self, inDict):
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
		print 'GCodeCombine interrogate'
		return json.dumps(self.info)
	
	def queue(self,atom_type, atom ):
		print 'insert an atom of something in the work queue'
		if self.info == None : 
			print 'failsauce' 
			return -6
		if self.info['input_atom'] != atom_type:
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
			self.yield_callback(self.info['output_atom'], '\n'.join(self.data))
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

def yielder(atom_type, atom):
	print 'atom type: ' + repr(atom_type)
	print 'atom: ' + repr(atom)	
	
if __name__ == "__main__":
	print 'doing a main thing here man'
	
	step =  BaseTransform()
	print BaseTransform

	print "interrogate"
	print LineCombineTransform.interrogate()
	
	step2 = LineCombineTransform()

	step2.setup({'yield_callback':yielder})
	print 'setup done'
	
	step2.queue("<type 'str'>","bla blah blah")
	step2.queue("<type 'str'>","car cala claw")
	
