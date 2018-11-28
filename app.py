from flask import Flask, render_template, jsonify, request
from desserts import dessert_list

app = Flask(__name__)


@app.route("/")
def home():
    """Return home page with basic info"""
    return render_template("index.html")


@app.route("/desserts")
def get_all_desserts():
    return jsonify(dessert_list.serialize())


@app.route("/desserts", methods=["POST"])
def add_dessert():
    """ Add new dessert and post reply """

    # obtain body json data from user patch
    user_data = request.json
    dessert_list.add(user_data['name'],
                     user_data['description'], user_data['calories'])

    return jsonify(dessert_list.desserts[-1].serialize())


@app.route("/desserts/<int:id>")
def get_specific_dessert(id):
    """Display data on specific dessert id"""

    sel_dessert = dessert_list.find(id)

    return jsonify(sel_dessert.serialize())


@app.route("/desserts/<int:id>", methods=["PATCH"])
def modify_dessert(id):
    """ Modify Dessert Details """

    sel_dessert = dessert_list.find(id)

    # obtain body json data from user patch
    user_data = request.json

    sel_dessert.modify(
        user_data['name'], user_data['description'], user_data['calories'])

    return jsonify(sel_dessert.serialize())


@app.route("/desserts/<int:id>", methods=["DELETE"])
def delete_dessert(id):
    """ Modify Dessert Details """

    sel_dessert = dessert_list.find(id)

    # find index of dessert needing to be removed
    remove_index = dessert_list.desserts.index(sel_dessert)

    # remove dessert from list and place into variable
    removed_dessert = dessert_list.desserts.pop(remove_index)

    return jsonify(removed_dessert.serialize())
