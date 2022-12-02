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

class ExpensesBlueprint():
    def __init__(self, db_conn):
        self.expenses = ExpensesBlueprint._make_blueprint(db_conn)
        LOGGER.info("\n\nExpenses Blueprint configured!\n\n")

    @staticmethod
    def _make_blueprint(db):
        expenses = Blueprint('expenses', __name__)
        
        @expenses.route('/', methods=['GET', 'POST', 'DELETE'])
        def get_or_create():
            if request.method == 'GET':
                return jsonify(
                    dumps(
                        db.get_all(
                            'expenses'
                        )
                    )
                )
            elif request.method == 'POST':
                id = db.insert_one(
                    'expenses',
                    request.get_json()
                )
                return jsonify({
                    'id': id
                })
            elif request.method == 'DELETE':
                db.delete_all('expenses')

                return jsonify({
                    'message': "success"
                })

        @expenses.route('/<string:id>', methods=['PUT', 'DELETE'])
        def update_or_delete(id):
            if request.method == 'PUT':
                db.update_one(
                    'expenses',
                    {'_id': ObjectId(id)},
                    {'$set': request.get_json()}
                )

                return jsonify({
                    'message': "success"
                })
            elif request.method == 'DELETE':
                db.delete_one(
                    'expenses',
                    {'_id': ObjectId(id)}
                )
                return jsonify({
                    'message': "success"
                })

        @expenses.route('/<string:id>', methods=['GET'])
        def total_cost(id):
            if request.method == 'GET':
                current_expenses = db.get_one(
                    'expenses',
                    {'_id': ObjectId(id)},
                )

                return jsonify({
                    'total_cost': computeTotalCost(
                        'expenses',
                        current_expenses,
                        db
                    )
                })
        @expenses.route('/expenses-category/<string:year>', methods=['GET'])
        def expenses_by_category(year):
            expenses = db.get_all('expenses', {'year': int(year)}, {'name': 1, 'year': 1, 'subtype': 1})
            subtypes_prices = {}
            LOGGER.info(year)

            for exp in expenses:
                LOGGER.info(exp)
                if exp['subtype'] in subtypes_prices.keys():
                    subtypes_prices[exp['subtype']] += computeTotalCost(
                        'expenses',
                        exp,
                        db
                    )
                else:
                    subtypes_prices[exp['subtype']] = computeTotalCost(
                        'expenses',
                        exp,
                        db
                    )
            
            return jsonify(
                {
                    'subtypes_expenses': subtypes_prices
                }
            )

        @expenses.route('/total-expenses/<string:year>', methods=['GET'])
        def total_expenses(year):
            expenses = db.get_all('expenses', {'year': int(year)}, {'name': 1, 'year': 1, 'subtype': 1})
            cost = 0
            for exp in expenses:
                LOGGER.info(exp)
                cost += computeTotalCost(
                    'expenses',
                    exp,
                    db
                )

            return jsonify(
                {
                    'total_cost': cost
                }
            )

        return expenses

    @property
    def blueprint(self):
        return self.expenses