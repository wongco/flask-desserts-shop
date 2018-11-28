from flask import Flask, render_template, jsonify, request
from desserts import dessert_list

app = Flask(__name__)


@app.route("/")
def home():
    """Return home page with basic info"""
    return render_template("index.html")


@app.route("/desserts")
def show_desserts():
    return jsonify(dessert_list.serialize())


@app.route("/desserts", methods=["POST"])
def post_desserts():
    """ Add new dessert and post reply """
    user_data = request.json
    dessert_list.add(user_data['name'],
                     user_data['description'], user_data['calories'])

    return jsonify(dessert_list.desserts[-1].serialize())


@app.route("/desserts/<id>")
def show_dessert(id):
    """Display data on specific dessert id"""

    id = int(id)
    # retreieve targeted dessert details
    sel_dessert = [
        dessert for dessert in dessert_list.desserts if dessert.id == id][0]

    return jsonify(sel_dessert.serialize())


@app.route("/desserts/<id>", methods=["PATCH"])
def modify_dessert(id):
    """ Modify Dessert Details """

    id = int(id)
    # retreieve targeted dessert details
    sel_dessert = [
        dessert for dessert in dessert_list.desserts if dessert.id == id][0]

    user_data = request.json

    sel_dessert.modify(
        user_data['name'], user_data['description'], user_data['calories'])

    return jsonify(sel_dessert.serialize())
