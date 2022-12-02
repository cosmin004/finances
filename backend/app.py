import logging
import sys
import os
from common import config
from common.db import DBConnector
from flask import Flask, redirect, jsonify, request, abort, make_response
from flask_cors import CORS
import pymongo
from pymongo import MongoClient, ReturnDocument

logging.basicConfig(stream=sys.stdout)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(config.LOG_LEVEL)

class FinancesService:
    """
        The FinancesService class represents the startable unit

        The server can be started in a stand-alone mode (e.g. for testing
        purposes) as well as by using the WSGI interface. For instance in 
        production the RestServer may be managed by running the gunicorn
        WSGI HTTP Server. To run the RestService in stand-alone mode the
        run() method is used.    
    """

    def __init__(self):
        # TODO: Statically initialize blueprints and DB Connector
        # TODO: Send db connector to the initialized blueprints
        db = DBConnector()
        self.app = FinancesService._make_wsgi_app(db)
        LOGGER.info("\n\nFinances Service started!\n\n")

    @staticmethod
    def _make_wsgi_app(db):
        """
            Creates the Flask app and configures the endpoints
            Returns:
                Flask: The finished Flask object
        """
        from endpoints.expenses import ExpensesBlueprint
        from endpoints.revenue import RevenueBlueprint

        app = Flask(__name__)
        app.register_blueprint(RevenueBlueprint(db).blueprint, url_prefix='/revenue')
        app.register_blueprint(ExpensesBlueprint(db).blueprint, url_prefix='/expenses')
        CORS(app, resources={r"/*": {"origins": "*"}})

        @app.route('/print-friend', methods=['GET'])
        def print_friends():
            return {
                'msg': "Hello friend!"
            }

        @app.route('/')
        def home():
            return redirect('/api')

        return app

        
    @property
    def wsgi_app(self):
        return self.app