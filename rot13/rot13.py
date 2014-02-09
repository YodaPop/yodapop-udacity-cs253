import webapp2
import cgi

# form validation
alphabet = 'abcdefghijklmnopqrstuvwxyz'

# rot13 simple encryption
def rot13(s):
	r = ''
	for c in s:
		if c not in alphabet and c not in alphabet.upper():
			r += c
		else:
			index = alphabet.find(c)
			if index >= 0:
				index += 13
				if index >= len(alphabet):
					r += alphabet[index - len(alphabet)]
				else:
					r += alphabet[index]
				continue
			index = alphabet.upper().find(c)
			if index >= 0:
				index += 13
				if index >= len(alphabet):
					r += alphabet.upper()[index - len(alphabet)]
				else:
					r += alphabet.upper()[index]

	return r

# escape HTML
def escape_html(str):
	return cgi.escape(str, quote = True)

form="""
	<form method="post">
		<h2>Enter some text to ROT13:</h2>
		<textarea name="text" rows="15" cols="70">%(text)s</textarea>
		<br>
		<input type="submit">
	</form>
"""

class MainPage(webapp2.RequestHandler):

	def write_form(self, text=""):
		self.response.out.write(form % {"text":escape_html(text)})

	def get(self):
		self.write_form()

	def post(self):
		text = self.request.get('text')
		text = rot13(text)

		self.write_form(text)

application = webapp2.WSGIApplication([
	('/', MainPage),
], debug=True)
