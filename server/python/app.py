import webapp2, operator, time, base64
from random import randint, choice
from datetime import datetime
from Crypto.Cipher import AES

challengeTemplate = '''If you could just {0} that would be great..Your Id is also {1}

send the result to /answer via POST with URL Form encoded parameters: the answers called payload and a contact parameter with your email called 'contact' and the same for the id so that I can know that it's you
Integer answers only please. Do it in whatever language you please.

OH!.. and by the way.. in under 2 seconds please

At the end you have the password of all passwords. 

i.e. 'payload'=<answer>,'contact'=<email>,'id'=<id>'''

answerTemplate = '''Hey!!
congrats! 
This is the sort of things that we do all day.
If you enjoyed this and you believe technical people should have a place to shine 
without having to resort to shitty management jobs, then Qamine wants to know about you.

The password is: I AM FUCKING AWESOME BECAUSE I LOVE TO CODE

Please send me (jaime@qamine.com) the password because I'm honestly not tracking whos trying the exercise.
Would love to talk to you.
								
Please also send me the code that you used to pass this (as well as your github account).
(don't send me CVs.. Send me code!)
'''

# Handle requests to /challenge
class ChallengePageHandler(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		challenge = Challenge.random()
		self.response.write(challengeTemplate.format(challenge.Text, challenge.Id))

# Handle requests to /answer
class AnswerPageHandler(webapp2.RequestHandler):
	def post(self):
		self.response.headers['Content-Type'] = 'text/plain'
		try:
			payload = self.request.get('payload')
			if not payload: self.response.write('No payload! <apu voice>please try again</apu voice>'); return 
				
			contact = self.request.get('contact')
			if not contact: self.response.write('No contact! <apu voice>please try again</apu voice>'); return 
				
			id = self.request.get('id')
			if not id: self.response.write('No Id! <apu voice>please try again</apu voice>'); return 
			
			
			id=AESUtils.decrypt(id)
			
			
			timestamp = int(id.split(":")[0])
			timestampNow = int(time.mktime(datetime.now().timetuple()))
			
			if (timestampNow - timestamp) > 2:
				self.response.write('Toke too long man! <apu voice>please try again</apu voice>')
				return

			if payload != id.split(":")[1]:
				self.response.write('Wrong result it should be {0}! <apu voice>please try again</apu voice>'.format(id.split(":")[1]))
				return
			
			self.response.write(answerTemplate)
		except: self.response.write('Wrong data. <apu voice>please try again</apu voice>')
		
		

# A class representing a Challenge
class Challenge:
	Types = [
				('divide {0} by {1}', operator.div), 
				('multiply {0} times {1}', operator.mul),
				('add {0} to {1}', operator.add), 
				('subtract {0} to {1}', operator.sub)
			] 
	

	@staticmethod
	def random():	
		challenge = Challenge();
		
		randomType = choice(Challenge.Types) # Select one challenge type
		randInts = [randint(0, 9999), randint(0, 9999)]
		
		challenge.Text = randomType[0].format(randInts[0], randInts[1])
		challenge.Result = reduce(randomType[1], randInts)
		if (randomType[1] == operator.sub): challenge.Result *= -1
		
		timestamp = str(int(time.mktime(datetime.now().timetuple())))
		id = timestamp + ':' + str(challenge.Result)
		
		challenge.Id = AESUtils.encrypt(id)

		return challenge
		
class AESUtils:
	@staticmethod
	def encrypt(data):
		cipher = AES.new("QAMINE IS AWESOM", AES.MODE_ECB)
		data += (16 - len(data) % 16) * "~" # padding with zeros
		return cipher.encrypt(data).encode("hex")
	
	@staticmethod
	def decrypt(data):
		cipher = AES.new("QAMINE IS AWESOM", AES.MODE_ECB)
		return cipher.decrypt(data.decode("hex")).rstrip("~")
	
	
		
WSGIApplication = webapp2.WSGIApplication([
    ('/challenge', ChallengePageHandler),
	('/answer', AnswerPageHandler),
], debug=True)