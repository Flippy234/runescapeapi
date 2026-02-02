from flask import Flask, render_template, request, redirect
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

SKILL_ICONS = {
    "Overall": "https://oldschool.runescape.wiki/images/Obtaining_max_total_level.gif?41325",
    "Attack": "https://oldschool.runescape.wiki/images/Attack_icon_%28detail%29.png?a4903",
    "Defence": "https://oldschool.runescape.wiki/images/Defence_icon_%28detail%29.png?a4903",
    "Strength": "https://oldschool.runescape.wiki/images/Strength_icon_%28detail%29.png?a4903",
    "Hitpoints": "https://oldschool.runescape.wiki/images/Defence_icon_%28detail%29.png?a4903",
    "Ranged": "https://oldschool.runescape.wiki/images/Ranged_icon_%28detail%29.png?a4903",
    "Prayer": "https://oldschool.runescape.wiki/images/Prayer_icon_%28detail%29.png?a4903",
    "Magic": "https://oldschool.runescape.wiki/images/Magic_icon_%28detail%29.png?a4903",
    "Cooking": "https://oldschool.runescape.wiki/images/Cooking_icon_%28detail%29.png?a4903",
    "Woodcutting": "https://oldschool.runescape.wiki/images/Woodcutting_icon_%28detail%29.png?a4903",
    "Fletching": "https://oldschool.runescape.wiki/images/Fletching_icon_%28detail%29.png?a4903",
    "Fishing": "https://oldschool.runescape.wiki/images/Fishing_icon_%28detail%29.png?a4903",
    "Firemaking": "https://oldschool.runescape.wiki/images/Firemaking_icon_%28detail%29.png?a4903",
    "Crafting": "https://oldschool.runescape.wiki/images/Crafting_icon_%28detail%29.png?a4903g",
    "Smithing": "https://oldschool.runescape.wiki/images/Smithing_icon_%28detail%29.png?a4903",
    "Mining": "https://oldschool.runescape.wiki/images/Mining_icon_%28detail%29.png?a4903",
    "Herblore": "https://oldschool.runescape.wiki/images/Herblore_icon_%28detail%29.png?a4903",
    "Agility": "https://oldschool.runescape.wiki/images/Agility_icon_%28detail%29.png?a4903",
    "Thieving": "https://oldschool.runescape.wiki/images/Thieving_icon_%28detail%29.png?a4903g",
    "Slayer": "https://oldschool.runescape.wiki/images/Slayer_icon_%28detail%29.png?a4903",
    "Farming": "https://oldschool.runescape.wiki/images/Farming_icon_%28detail%29.png?a4903",
    "Runecrafting": "https://oldschool.runescape.wiki/images/Runecraft_icon_%28detail%29.png?a4903",
    "Hunter": "https://oldschool.runescape.wiki/images/Hunter_icon_%28detail%29.png?a4903",
    "Construction": "https://oldschool.runescape.wiki/images/Construction_icon_%28detail%29.png?a4903"
}


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
        levels=levels,
        skill_icons=SKILL_ICONS,
        skill_info=skill_info
    )
skill_info = {
    "Strength": "www.flippysucks.com"
    }

@app.route("/skills/<skill_name>")
def show_guide(skill_name):
    url = skill_info.get(skill_name)
    if not url:
        return "skill not found.", 404
    return redirect(url)



def parse_stats(data):
    parsed = {}
    for i, skill in enumerate(SKILLS):
        try:
            rank, level, xp = data[i].split(",")
            level = int(level)
            xp = int(xp)

            if skill == "Overall":
                max_level = 2277
            else:
                max_level = 99

            percent = round((level / max_level) * 100, 2)

            parsed[skill] = {"rank": int(rank),"level": level,"xp": xp,"percent": percent
            }
        except:
            parsed[skill] = {"rank": "-","level": 0,"xp": 0,"percent": 0
            }
    return parsed

if __name__ == "__main__":
    app.run(debug=True)