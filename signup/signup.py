import webapp2
import re

# Constant regular expressions for validation
USER_RE     =   re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE     =   re.compile(r"^.{3,20}$")
EMAIL_RE    =   re.compile(r"^[\S]+@[\S]+\.[\S]+$")

# Validate username
def valid_username(username):
	return USER_RE.match(username)

# Validate password
def valid_password(password):
	return PASS_RE.match(password)

# Verify password
def valid_verify(password, verify):
	if password != verify:
		return None
	return True

# Validate email (optional)
def valid_email(email):
	if email:
		return EMAIL_RE.match(email)
	else:
		return True

form="""
	<form method="post">
		<h2>Signup</h2>
		<div style="float:left; text-align:right; width:130px; font-weight:bold;
padding-top:3px; padding-right:3px;">
			<label style="display:block; height:24px;" for="username">Username</label>
			<label style="display:block; height:24px;" for="password">Password</label>
			<label style="display:block; height:24px;" for="verify">Verify Password</label>
			<label style="display:block; height:24px;" for="email">Email (Optional)</label>
		</div>
		<div style="float:left">
			<input style="display:block" id="username" name="username" type="text" value="%(username)s">
			<input style="display:block" id="password" name="password" type="password" value="">
			<input style="display:block" id="verify" name="verify" type="password" value="">
			<input style="display:block" id="email" name="email" type="text" value="%(email)s">
		</div>
		<div style="float:left; font-weight:bold; padding-top:3px;
padding-left:3px">
			<div style="color:red; height:24px;">%(username_error)s</div>
			<div style="color:red; height:24px;">%(password_error)s</div>
			<div style="color:red; height:24px;">%(verify_error)s</div>
			<div style="color:red; height:24px;">%(email_error)s</div>
		</div>
		<div style="clear:both"></div>
		<input type="submit">
	</form>
"""

class MainPage(webapp2.RequestHandler):

	def write_form(self, username="", username_error="", password_error="", 
					verify_error="", email="", email_error=""):
		self.response.out.write(form % {
			"username"          :   username,
			"username_error"    :   username_error,
			"password_error"    :   password_error,
			"verify_error"      :   verify_error,
			"email"             :   email,
			"email_error"       :   email_error
		})

	def get(self):
		self.write_form()

	def post(self):
		username        =   self.request.get('username')
		username_error  =   valid_username(username)
		password        =   self.request.get('password')
		password_error  =   valid_password(password)
		verify          =   self.request.get('verify')
		verify_error    =   valid_verify(password, verify)
		email           =   self.request.get('email')
		email_error     =   valid_email(email)

		# Check for errors
		if (not username_error or not password_error or not verify_error or not
				email_error):
			# Set error messages
			if not username_error:
				username_error = "That's not a valid username"
			else:
				username_error = ""
			if not password_error:
				password_error = "That wasn't a valid password"
			else:
				password_error = ""
			if not verify_error:
				verify_error = "The passwords don't match"
			else:
				verify_error = ""
			if not email_error and email:
				email_error = "That's not a valid email address"
			else:
				email_error = ""

			# Write to form
			self.write_form(username, username_error, password_error,
					verify_error, email, email_error)
		else:
			# Redirect to Welcome Page
			self.redirect('/welcome?username=' + username)

class WelcomePage(webapp2.RequestHandler):

	def get(self):
		username = self.request.get('username')
		self.response.out.write('<h2>Welcome, ' + username)

application = webapp2.WSGIApplication([
	('/'        ,   MainPage),
	('/welcome' ,   WelcomePage),
], debug=True)
