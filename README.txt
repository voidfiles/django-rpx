Handles site login and user registration using the rpxnow.com service..

this is work in rapid progress and not guaranteed to be API-stable or any such nonsense.

based off the following recipe: http://appengine-cookbook.appspot.com/recipe/accept-google-aol-yahoo-myspace-facebook-and-openid-logins/
by "brian ellin"

TODO: 
  * implement sign-in interface customisation and localisation: https://rpxnow.com/docs#sign-in_interface
  * implement the mapping api https://rpxnow.com/docs#mappings to ease integration
  
INSTALLATION:
  put 'rpx' in your installed apps. additionally, create a url path that serves up the rpx_response view in views.py.
  currently this app looks for the domain name in settings.HOST; that's the way that the site i built this in works but you may wish to inspect the HttpRequest or interrogate the django.contrib.sites app to find out the domain for generating the callback URL