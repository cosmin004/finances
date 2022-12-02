import json
import os

def computeTotalCost(type, value, dbconn):
    category = value['subtype'].lower().replace(' ', '')
    year = value['year']
    name = value['name']

    with open(os.path.join('assets', 'jsonschemas', category.lower() + '.json')) as f:
        schema = json.loads(f.read())
        f.close()

    if type not in schema.keys():
        raise FileNotFoundError
    typeData = schema[type]

    costFormula = typeData['totalCostComputation']

    operation = '*'

    components = costFormula.split(operation)

    firstComponent = components[0].split('.')
    
    firstValue = dbconn.get_one(
        firstComponent[0],
        {
            'year': year,
            'name': name
        }
    )[firstComponent[1]]

    total = int(firstValue)

    for i in range(1, len(components)):
        currComponent = components[i].split('.')
        currValue = dbconn.get_one(
            currComponent[0],
            {
                'year': year,
                'name': name
            }
        )[currComponent[1]]
        total *= int(currValue)

    return total