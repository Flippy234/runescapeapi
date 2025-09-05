from flask import Flask, render_template, request
import requests

app = Flask(__name__)


API_URL = 'https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player='

SKILLS = [
    "Overall", "Attack", "Defence", "Strength", "Hitpoints", "Ranged",
    "Prayer", "Magic", "Cooking", "Woodcutting", "Fletching", "Fishing",
    "Firemaking", "Crafting", "Smithing", "Mining", "Herblore",
    "Agility", "Thieving", "Slayer", "Farming", "Runecrafting",
    "Hunter", "Construction"
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"].strip()
        return show_stats(username)
    return render_template("index.html")

@app.route("/stats/<username>")
def show_stats(username):
    response = requests.get(API_URL + username)

    if response.status_code != 200:
        return render_template("index.html", error="Player not found.")

    data = response.text.split("\n")
    stats_dict = parse_stats(data)

    skills = list(stats_dict.keys())
    levels = [stats_dict[s]["level"] for s in skills]

    return render_template(
        "stats.html",
        username=username,
        skills=skills,
        stats=stats_dict,
        levels=levels
    )

def parse_stats(data):
    parsed = {}
    for i, skill in enumerate(SKILLS):
        try:
            rank, level, xp = data[i].split(",")
            parsed[skill] = {"rank": int(rank),
                             "level": int(level),
                             "xp": int(xp)}
        except:
            parsed[skill] = {"rank": "-",
                             "level": "-",
                             "xp": "-"}
    return parsed

if __name__ == "__main__":
    app.run(debug=True)