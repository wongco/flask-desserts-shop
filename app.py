from flask import Flask, render_template, jsonify, request, session
from desserts import dessert_list

app = Flask(__name__)
app.secret_key = "RANDOM KEY"


@app.route("/")
def home():
    """ Return home page with basic info """
    return render_template("index.html")


@app.route("/desserts")
def get_all_desserts():
    """ Gets all desserts info """
    return jsonify(dessert_list.serialize())


@app.route("/desserts", methods=["POST"])
def add_dessert():
    """ Add new dessert and post reply """

    # obtain body json data from user post
    user_data = request.json
    dessert_list.add(user_data['name'],
                     user_data['description'], user_data['calories'])

    return jsonify(dessert_list.desserts[-1].serialize())


@app.route("/desserts/<int:id>")
def get_specific_dessert(id):
    """Display data on specific dessert id"""

    try:
        sel_dessert = dessert_list.find(id)
    except ValueError:
        return render_template("404.html"), 404

    return jsonify(sel_dessert.serialize())


@app.route("/desserts/<int:id>", methods=["PATCH"])
def modify_dessert(id):
    """ Modify Dessert Details """

    try:
        sel_dessert = dessert_list.find(id)
    except ValueError:
        return render_template("404.html"), 404

    # obtain body json data from user patch
    user_data = request.json

    sel_dessert.modify(
        user_data['name'], user_data['description'], user_data['calories'])

    return jsonify(sel_dessert.serialize())


@app.route("/desserts/<int:id>", methods=["DELETE"])
def delete_dessert(id):
    """ Modify Dessert Details """

    try:
        sel_dessert = dessert_list.find(id)
    except ValueError:
        return render_template("404.html"), 404

    # find index of dessert needing to be removed
    remove_index = dessert_list.desserts.index(sel_dessert)

    # remove dessert from list and place into variable
    removed_dessert = dessert_list.desserts.pop(remove_index)

    return jsonify(removed_dessert.serialize())


@app.route("/desserts/<int:id>/eat", methods=["POST"])
def get_total_calories(id):
    """ get total calories eaten by user """

    try:
        sel_dessert = dessert_list.find(id)
    except ValueError:
        return render_template("404.html"), 404

    # retrieve session info, store updated info
    total_calories = session.get('total_calories', 0)
    total_calories += sel_dessert.calories
    session['total_calories'] = total_calories

    return jsonify({
        "total_calories": total_calories
    })
