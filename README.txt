*********************
NB - doesn't work yet
*********************

most urgent TODO - implement an authentication backend as per http://docs.djangoproject.com/en/dev/topics/auth/#authentication-backends

Handles site login and user registration using the rpxnow.com service..

this is work in rapid progress and not guaranteed to be API-stable or any such nonsense.

based off the following recipe: http://appengine-cookbook.appspot.com/recipe/accept-google-aol-yahoo-myspace-facebook-and-openid-logins/
by "brian ellin"

TODO: 
  * implement sign-in interface customisation and localisation: https://rpxnow.com/docs#sign-in_interface
  * implement the mapping api https://rpxnow.com/docs#mappings to ease integration
  * tests (tricky - mocking out the RPX server before i understand how it works...)
  * documentation of conf settings
  
INSTALLATION:
  * put the code in a directory called 'rpx' somewhere in your path and pyt 'rpx' in your installed apps. additionally, create a url path that serves up the rpx_response view in views.py.
  * you will also need to put the RPXNOW_API_KEY, RPXNOW_REALM and optionally RPX_TRUSTED_PROVIDERS into your settings.py
  * you will also need to add rpx to your authentication providers list
  AUTHENTICATION_BACKENDS = (
    'rpx.backends.RpxBackend',
    'django.contrib.auth.backends.ModelBackend',
  )
  
  * you might want to include the rpx template tags in your site code somewhere to provide a login link. the embedded iframe version is not yet integrated - the popup/link-out version is provided
  
