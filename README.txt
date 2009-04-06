This app is functioning. 

Handles site login and user registration using the rpxnow.com service..

Based off the following recipe: http://appengine-cookbook.appspot.com/recipe/accept-google-aol-yahoo-myspace-facebook-and-openid-logins/
by "brian ellin" of rpxnow.com

TODO: 
  * Could really use a test suite. Help is welcome with the intricacies of mocking out this kind of messy redirect/AJAX service. (automated browser, sure, but how do I mock out the rpxnow service itself?)
  * Implement sign-in interface customisation and localisation: https://rpxnow.com/docs#sign-in_interface
  * Optionally implement the mapping api https://rpxnow.com/docs#mappings to ease integration?
  
INSTALLATION:
  * Put the code in a directory called 'rpx' somewhere in your path and put 'rpx' in your installed apps. additionally, create a url path that serves up the rpx_response view in views.py.
  * You will also need to put the RPXNOW_API_KEY, RPXNOW_REALM and optionally RPX_TRUSTED_PROVIDERS into your settings.py (RPXNOW_REALM isn't well documented on the rpxnow site, but it's the subdomain of rpxnow.com that handles your HTTP callback - e.g. if http://possumpalace-blog.rpx.now is th destination of the link in your provided rpxnow snippet, your realm is "possumpalace-blog".
  * You will also need to add rpx to your authentication providers list
  AUTHENTICATION_BACKENDS = (
    'rpx.backends.RpxBackend',
    'django.contrib.auth.backends.ModelBackend',
  )
  * You might want to include the rpx template tags in your site code somewhere to provide a login link. Their embedded iframe version is not yet templated up. - the popup/link-out version is provided.
  
