import dbm
from flask import Blueprint, request, jsonify
import logging
import sys
from common import config
from common.jsonschemas import *
from bson.objectid import ObjectId
from bson.json_util import dumps

logging.basicConfig(stream=sys.stdout)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(config.LOG_LEVEL)

class RevenueBlueprint():
    def __init__(self, db_conn):
        self.revenue = RevenueBlueprint._make_blueprint(db_conn)
        LOGGER.info("\n\nRevenue Blueprint configured!\n\n")

    @staticmethod
    def _make_blueprint(db):
        revenue = Blueprint('revenue', __name__)

        @revenue.route('/', methods=['GET', 'POST', 'DELETE'])
        def get_or_create():
            if request.method == 'GET':
                return jsonify(
                    dumps(
                        db.get_all(
                            'revenue'
                        )
                    )
                )
            elif request.method == 'POST':
                LOGGER.info(request.get_json())
                id = db.insert_one(
                    'revenue',
                    request.get_json()
                )
                return jsonify({
                    'id': id
                })
            elif request.method == 'DELETE':
                db.delete_all('revenue')

                return jsonify({
                    'message': "success"
                })

        @revenue.route('/<string:id>', methods=['PUT', 'DELETE'])
        def update_or_delete(id):
            if request.method == 'PUT':
                LOGGER.info(request.get_json())
                LOGGER.info(type(request.get_json()))
                db.update_one(
                    'revenue',
                    {'_id': ObjectId(id)},
                    {'$set': request.get_json()}
                )

                return jsonify({
                    'message': "success"
                })
            elif request.method == 'DELETE':
                db.delete_one(
                    'revenue',
                    {'_id': ObjectId(id)}
                )
                return jsonify({
                    'message': "success"
                })

        @revenue.route('/<string:id>', methods=['GET'])
        def total_cost(id):
            if request.method == 'GET':
                current_revenue = db.get_one(
                    'revenue',
                    {'_id': ObjectId(id)},
                )

                return jsonify({
                    'total_cost': computeTotalCost(
                        'revenue',
                        current_revenue,
                        db
                    )
                })
        
        @revenue.route('/revenue-category/<string:year>', methods=['GET'])
        def revenue_by_category(year):
            revenues = db.get_all('revenue', {'year': int(year)}, {'name': 1, 'year': 1, 'subtype': 1})
            subtypes_prices = {}

            for exp in revenues:
                if exp['subtype'] in subtypes_prices.keys():
                    subtypes_prices[exp['subtype']] += computeTotalCost(
                        'revenue',
                        exp,
                        db
                    )
                else:
                    subtypes_prices[exp['subtype']] = computeTotalCost(
                        'revenue',
                        exp,
                        db
                    )
            
            return jsonify(
                {
                    'subtypes_revenues': subtypes_prices
                }
            )

        @revenue.route('/total-revenue/<string:year>', methods=['GET'])
        def total_revenue(year):
            revenues = db.get_all('revenue', {'year': int(year)}, {'name': 1, 'year': 1, 'subtype': 1})
            cost = 0
            for rev in revenues:
                cost += computeTotalCost(
                    'revenue',
                    rev,
                    db
                )

            return jsonify(
                {
                    'total_cost': cost
                }
            )

        return revenue

    @property
    def blueprint(self):
        return self.revenue