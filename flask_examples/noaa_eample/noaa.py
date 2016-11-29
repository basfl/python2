from flask import Flask
from flask import request ,session
from flask import render_template
from flask import redirect,url_for
from flask import session as login_session
import random,string
from noaaweather import weather
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
#CLIENT_ID=json.loads(open("client_secrets.json","r").read())["web"]["client_id"]

app=Flask(__name__)
app.secret_key="A0Zr98j/3yX R~XHH!jmN]LWX/,?RT"
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output
@app.route("/login")
def showLogin():
    state="".join(random.choice(string.ascii_uppercase+string.digits)for x in xrange(32))
    
    login_session["state"]=state;
    #return(login_session["state"]);
    return (render_template("login.html"));
@app.route("/weather/<zip>")
def get_weather(zip):
    sfWeather=weather.noaa();
    sfWeather.getByZip(zip);
    
    a=sfWeather.temperature.apparent.value
    w=""+str(a);
    d={"current weather is ":w,"future is":2};
    return (render_template("rslt.html",result=d));
    #return(w);
@app.route("/zip",methods=["POST","GET"])
def get_zip():
    if request.method=='POST':
        zipCode=request.form["zip"];
        return redirect((url_for("get_weather",zip=zipCode)));
        return (zipCode);
        
    return (render_template("start.html"));

if __name__=="__main__":
            app.debug=True;
            app.run();
        
