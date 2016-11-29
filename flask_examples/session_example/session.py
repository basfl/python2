from flask import Flask
from flask import request ,session
from flask import render_template
from flask import redirect,url_for
app=Flask(__name__)
app.secret_key="A0Zr98j/3yX R~XHH!jmN]LWX/,?RT"
@app.route("/")
def index():
    if "username" in session:
        s="username is "+session["username"];
        return(s);
    return("login failed");
@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=='POST':
        session["username"]=request.form["username"];
        return redirect((url_for("index")));
    return (render_template("start.html"));

if __name__=="__main__":
            app.debug=True;
            app.run();
