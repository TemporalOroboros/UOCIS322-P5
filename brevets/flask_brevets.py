"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import os
import arrow # Replacement for datetime, based on moment.js
import logging
import flask
from flask import Flask, redirect, url_for, request, render_template
from flask_restful import Resource, Api
from pymongo import MongoClient
import acp_times
import config

###
# Globals
###

CONFIG = config.configuration()
app = flask.Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client['acp-controle-times']
controles = db.controles

app.secret_key = os.urandom(24)

###
# Pages
###

# Main page (brevet controle time calculator)
@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')

# Display page (displays all brevet controle times in the database)
@app.route("/display")
def display():
    app.logger.debug("")

    db_dump = controles.find(projection={"_id": 0})
    return flask.render_template('display.html', controles = db_dump)


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############

# 
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from km using rules
    described at https://rusa.org/octime_alg.html
    Extacts three URL-encoded arguments,
        The number of km to the controle
        The distance of the brevet
        The start time of the brevet
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', None, type=float)
    brevet = request.args.get('brevet', 200, type=float)
    iso_start_time = request.args.get('start_time', arrow.now().isoformat, type=str)
    start_time = arrow.get(iso_start_time)

    result = get_times_strings(km, brevet, start_time)
    return flask.jsonify(result=result)

def get_times(controle_dist_km, brevet_dist_km, brevet_start_time):
    """
    Calculates open/close times from km using rules
    described at https://rusa.org/octime_alg.html
    Expects three arguments
        The number of km to the controle
        The distanct of the brevet
        The start time of the brevet
    """
    open_time = acp_times.open_time(controle_dist_km, brevet_dist_km, brevet_start_time)
    close_time = acp_times.close_time(controle_dist_km, brevet_dist_km, brevet_start_time)
    return open_time, close_time

def get_times_strings(controle_dist_km, brevet_dist_km, brevet_start_time):
    """
    Calculates open/close times from km using rules
    described at https://rusa.org/octime_alg.html
    Expects three arguments
        The number of km to the controle
        The distanct of the brevet
        The start time of the brevet
    """
    open_time, close_time = get_times(controle_dist_km, brevet_dist_km, brevet_start_time)
    return {
        "open": open_time.format('YYYY-MM-DDTHH:mm'),
        "close": close_time.format('YYYY-MM-DDTHH:mm')
    }


@app.route("/controles", methods=["POST"])
def add_controles_to_db():
    app.logger.debug("Got a POST request to database")
    insert = request.args.get('controles', None, type=list)
    if (insert is None) or (len(insert) == 0):
        return "", 501
    result = controles.insert_many(insert).inserted_ids
    return flask.jsonify(result = result), 200

class Controles(Resource):
    def get(self, uid):
        app.logger.debug("Got a get request to database")
        if uid == 'all':
            result_cursor = controles.find(projection={'_id': 0})
        result_cursor = controles.find_one({'_id': uid}, {'_id': 0})
        return flask.jsonify(result=list(result_cursor)), 200

    def post(self, uid):
        return add_controles_to_db()

    def put(self, uid):
        app.logger.debug("Got a put request to database")
        return "", 501
    
    def delete(self, uid):
        app.logger.debug("Got a delete request to database")
        return "", 501

api.add_resource(Controles, '/controles/<uid>')

###
# Error Handlers
###

@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404

@app.errorhandler(501)
def not_supported(error):
    app.logger.debug("")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('501.html'), 501

#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")

