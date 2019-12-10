from service import app
import json
from flask import jsonify
import logging
from dao.products_dao import ProductsDAO
from data.ingest import ingest_defaults


log = logging.getLogger(__name__)

app.products_dao = None


@app.before_first_request
def before_first_request_func():
    if not app.products_dao:
        return jsonify(status="Hey! This is your first request, so I will be loading up "+
                       "some nice data for you. Check back in a little while."), 200


def get_dao():
    if not app.products_dao:
        app.products_dao = ProductsDAO(ingest_defaults())
    return app.products_dao

@app.route("/")
def home():
    return jsonify("try GET /data/dgd or GET /data/cheapest/10")

@app.route("/data/<id>", methods=["GET"])
def get_by_id(id:str):
    response = get_dao().get_product_by_id(id)
    if response is None:
        return jsonify(result="nothing!"), 200
    return response, 200

@app.route("/data/cheapest/<number>", methods=["GET"])
def get_n_cheapest(number:int):
    try:
        n = int(number)
    except ValueError:
        return jsonify(error=f"This ({number}) is not an int"), 400
    response = get_dao().get_n_cheapest_products(n)
    return jsonify(response), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
