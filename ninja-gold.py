from flask import Flask, render_template, redirect, session, request
import random
import time

app = Flask(__name__)
app.secret_key = "secret"

@app.route("/")
def index():
    if not "gold" in session:
        session["gold"] = 0    
    return render_template("index.html")

@app.route("/process_money", methods=["POST"])
def process_money():
    if not "prize" in session:
        session["prize"] = 0
    if not "activities" in session:
        session["activities"] = []
    session["class"] = "green"
    place = request.form["place"]
    
    if place == "farm":
        session["prize"] = random.randrange(10,21)
    elif place == "cave":
        session["prize"] = random.randrange(5,11)
    elif place == "house":
        session["prize"] = random.randrange(2,6)
    elif place == "casino":
        if random.randrange(0,2) == 1:
            session["prize"]= random.randrange(0,51)
        else:
            session["prize"] = (random.randrange(0,51)) * -1
    session["gold"] += session["prize"]
    session["activities"].append(create_activity(session["prize"], place))
    return redirect("/")

def create_activity(gold, place):
    activity = ""
    localtime = time.asctime( time.localtime(time.time()) )
    if gold >= 0:
       activity = "Earned "+ str(gold) + " golds from " + place +"! ("+localtime+")"  
       session["class"] = "green"    
    else:
        activity = "Entered a casino and lost " + str(gold*-1) + " golds... Ouch... ("+localtime+")"
        session["class"] = "red"
    return activity



@app.route("/clear")
def clear():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)