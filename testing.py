from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)

# Mongodb Database and Collection
client = MongoClient('mongodb+srv://gamutingridjezreeln:foodnutritionalAPI@cluster1.6wm59m1.mongodb.net/')
db = client['food_nutritional_API']

food_collection = db['food_data']

# Food route for listing all the data
@app.route('/food', methods=['GET'])
def get_food():
    food_data = food_collection.find()
    return dumps({'food': food_data})

# Food route para mag request of data just by an ID
@app.route('/food/<int:foodId>', methods=['GET'])
def get_food_by_id(foodId):
    # Ensure that 'foodId' is treated as an integer
    food_data = food_collection.find_one({'_id': foodId})
    if food_data is None:
        return jsonify({'error': 'Food not found'}), 404

    return jsonify({'food': food_data})

# Food route para maka request by foodType
@app.route('/food/type/<string:foodType>', methods=['GET'])
def get_food_by_type(foodType):
    # Assuming food_collection is your MongoDB collection
    food_data_cursor = food_collection.find({'foodType': foodType})

    # Convert the cursor to a list of dictionaries
    food_list = list(food_data_cursor)

    if not food_list:
        return jsonify({'error': 'Food type not found'}), 404

    return jsonify({'food': food_list})

# Food route para maka request by foodName
@app.route('/food/name/<string:foodName>', methods=['GET'])
def get_food_by_name(foodName):
    # Assuming food_collection is your MongoDB collection
    food_data = food_collection.find_one({'foodName': foodName})

    if food_data is None:
        return jsonify({'error': 'Food not found'}), 404

    return jsonify({'food': food_data})

# Food route para maka post og new set of datas
@app.route('/food', methods=['POST'])
def add_food():
    if not request.json or 'foodName' not in request.json:
        return jsonify({'error': 'FoodName is required'}), 400

    new_food = {
        'foodId': food_collection.find().count() + 1,
        'foodName': request.json['foodName'],
        'foodType': request.json.get('foodType', ""),
        'nutritionalInformation': {
            'Calories': request.json.get('nutritionalInformation', {}).get('Calories', ""),
            'Protein': request.json.get('nutritionalInformation', {}).get('Protein', ""),
            'Fat': request.json.get('nutritionalInformation', {}).get('Fat', ""),
            'Cholesterol': request.json.get('nutritionalInformation', {}).get('Cholesterol', ""),
            'Sodium': request.json.get('nutritionalInformation', {}).get('Sodium', ""),
            'Carbohydrate': request.json.get('nutritionalInformation', {}).get('Carbohydrate', ""),
            'DietaryFiber': request.json.get('nutritionalInformation', {}).get('DietaryFiber', ""),
            'Vitamins': request.json.get('nutritionalInformation', {}).get('Vitamins', []),
        }
        # Add other fields as needed
    }

    result = food_collection.insert_one(new_food)
    new_food['_id'] = str(result.inserted_id)  # Convert ObjectId to string

    return jsonify({'food': new_food}), 201

# Food route para maka update of data
@app.route('/food/<int:id>', methods=['PUT'])
def update_food(id):
    # Kulang data for PUT
    return jsonify({'food': food})

# Food route para maka delete og data
@app.route('/food/<int:id>', methods=['DELETE'])
def delete_food(id):
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)