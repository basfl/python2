from flask import Flask
from flask import request
from flask import render_template
from flask import redirect,url_for
app=Flask(__name__)
@app.route("/")
def get_index():
    return("hi");
@app.route("/project",methods=["POST","GET"])
def get_project():
    if request.method=='POST':
        p=request.form["project"];
        return redirect((url_for("proj_name",name=p)));
        #return(p);
     
    return(render_template("project.html"));
@app.route("/project/<name>")
def proj_name(name):
    s="project name is **"+name;
    return(s);

if __name__=="__main__":
    app.debug=True;
    app.run();
    
