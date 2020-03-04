# pyCHPP
pyCHPP is a python framework created to use the API provided by the online game Hattrick (www.hattrick.org).

## Usage

### First connection
    # Set consumer_key and consumer_secret provided for your app by Hattrick
    consumer_key = ''
    consumer_secret = ''
    
    # Initialize CHPP object
    chpp = CHPP(consumer_key, consumer_secret)
    
    # Get url, request_token and request_token_secret to request API access
    # You can set callback_url and scope
    auth = chpp.get_auth(callback_url='www.mycallbackurl.com', scope='')
    
    # auth['url'] contains the url to which the user can grant the application access to the Hattrick API
    # Once the user has entered their credentials, a code is returned by Hattrick (directly or to the given callback url)
    
    # Get access token from Hattrick
    # access_token['key'] and access_token['secret'] have to be stored in order to be used later by the app
    access_token = chpp.get_access_token(request_token=auth['request_token'],
                                         request_token_secret=auth['request_token_secret'],
                                         code=code,
                                         )

### Further connection
    # Once you have obtained access_token for a user
    # You can use it to call Hattrick API
    chpp = CHPP(consumer_key, consumer_secret, access_token['key'], access_token['secret'])
    
    # Now you can use chpp methods to get datas from Hattrick API
    # For example :
    user = chpp.get_current_user()