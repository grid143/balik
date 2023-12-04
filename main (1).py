# DoggyData Web Service v1
# ITCC 14 B - GROUP C - FINAL PROJECT
# Members: Isaac Martel V. Abogatal, Mona Camille Madria VII, Joash Mathew Zamoras

from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)

client = MongoClient('mongodb+srv://DoggyData:DoggyPass@cluster0.bw0qv3b.mongodb.net/')
db = client['DoggyData']

dogs = db['dogs']
dogdiseases = db['dogdiseases']
dogsymptoms = db['dogsymptoms']
dogallergies = db['dogallergies']
dogvaccines = db['dogvaccines']
dogmedications = db['dogmedications']
dogdiet = db['dogdiet']
user = db['user']


# ---------------- DOGS ROUTE -----------------------------------------

# GET all dogs WORKING
@app.route('/dogs', methods=['GET'])
def get_dogs():
    return dumps({'dogs': dogs.find()})


# GET dog by id WORKING
@app.route('/dogs/<int:dogbreedId>', methods=['GET'])
def get_dog_by_id(dogbreedId):
    dog = dogs.find_one({'dogbreedId': dogbreedId})
    if dog is None:
        return jsonify({'error': 'Dog not found'}), 404
    return dumps({'dog': dog})


# POST new dog WORKING
@app.route('/dogs', methods=['POST'])
def create_dog():
    if not request.json or 'breedName' not in request.json:
        return jsonify({'error': 'BreedName is required'}), 400

    new_dog = {
        'dogbreedId': dogs.count_documents({}) + 1,
        'breedName': request.json['breedName'],
        'size': request.json.get('size', ""),
        'dogbreedImageURL': request.json.get('dogbreedImageURL', ""),
        'description': request.json.get('description', "")
    }

    result = dogs.insert_one(new_dog)
    new_dog['_id'] = str(result.inserted_id)
    success_message = f"New dog breed '{new_dog['breedName']}' has been added successfully!"
    return jsonify({'dog': new_dog, 'message': success_message}), 201

# PUT update dog WORKING
@app.route('/dogs/<int:dogbreedId>', methods=['PUT'])
def update_dog(dogbreedId):
    dog = dogs.find_one({'dogbreedId': dogbreedId})
    if dog is None:
        return jsonify({'error': 'Dog not found'}), 404

    updated_data = {
        'breedName': request.json.get('breedName', dog['breedName']),
        'size': request.json.get('size', dog['size']),
        'dogbreedImageURL': request.json.get('dogbreedImageURL', dog['dogbreedImageURL']),
        'description': request.json.get('description', dog['description']),
    }

    dogs.update_one({'dogbreedId': dogbreedId}, {'$set': updated_data})
    updated_dog = dogs.find_one({'dogbreedId': dogbreedId})
    success_message = f"Dog breed '{updated_dog['breedName']}' has been updated successfully!"
    updated_dog['_id'] = str(updated_dog['_id'])
    return jsonify({'dog': updated_dog, 'message': success_message})

# DELETE dog by id WORKING
@app.route('/dogs/<int:dogbreedId>', methods=['DELETE'])
def delete_dog(dogbreedId):
    dog = dogs.find_one({'dogbreedId': dogbreedId})
    if dog is None:
        return jsonify({'error': 'Dog not found'}), 404

    breed_name = dog['breedName']

    result = dogs.delete_one({'dogbreedId': dogbreedId})
    if result.deleted_count == 0:
        return jsonify({'error': f'Dog breed "{breed_name}" not found'}), 404

    success_message = f'Dog breed "{breed_name}" with ID {dogbreedId} has been deleted successfully!'

    return jsonify({'result': True, 'message': success_message})


# ---------------- DOG DISEASES ROUTE -----------------------------------------

# GET dog disease by id
@app.route('/dogdiseases/<int:dogbreedId>', methods=['GET'])
def get_dog_disease_by_id(dogbreedId):
    dog_disease = dogdiseases.find_one({'dogbreedId': dogbreedId})
    if dog_disease is None:
        return jsonify({'error': 'Dog disease not found'}), 404
    return dumps({'dog disease': dog_disease})


# POST new dog disease
@app.route('/dogdiseases', methods=['POST'])
def create_dog_disease():
    if not request.json or 'dsName' not in request.json:
        return jsonify({'error': 'dsName is required'}), 400

    new_dog_disease = {
        'dsId': dogdiseases.find().count() + 1,
        'dsName': request.json['dsName'],
        'dogbreedId': request.json.get('dogbreedId', "")
    }

    dogdiseases.insert_one(new_dog_disease)
    return dumps({'dog disease': new_dog_disease}), 201


# PUT update dog disease
@app.route('/dogdiseases/<int:dogbreedId>', methods=['PUT'])
def update_dog_disease(dogbreedId):
    dog_disease = dogdiseases.find_one({'dogbreedId': dogbreedId})
    if dog_disease is None:
        return jsonify({'error': 'Dog disease not found'}), 404

    dogdiseases.update_one(
        {'dogbreedId': dogbreedId},
        {
            '$set': {
                'dsName': request.json.get('dsName', dog_disease['dsName']),
                'dogbreedId': request.json.get('dogbreedId', dog_disease['dogbreedId']),
            }
        }
    )

    return dumps({'dog disease': dogdiseases.find_one({'dogbreedId': dogbreedId})})


# DELETE dog disease by id
@app.route('/dogdiseases/<int:dogbreedId>', methods=['DELETE'])
def delete_dog_disease(dogbreedId):
    result = dogdiseases.delete_one({'dogbreedId': dogbreedId})
    if result.deleted_count == 0:
        return jsonify({'error': 'Dog disease not found'}), 404

    return jsonify({'result': True})


@app.route('/dogdiseases/list/<int:dogbreedId>', methods=['GET'])
def get_dog_diseases_by_breed(dogbreedId):
    dog = dogs.find_one({'dogbreedId': dogbreedId})
    if dog is None:
        return jsonify({'error': 'Dog not found'}), 404

    diseases = dogdiseases.find({'dogbreedId': dogbreedId})
    return dumps({'dogbreedId': dogbreedId, 'diseases': list(diseases)})


# ---------------- DOG SYMPTOMS ROUTE -----------------------------------------

# CREATE new dog symptom for a specific dog breed
@app.route('/dogsymptoms', methods=['POST'])
def create_dog_symptom():
    if not request.json or 'stName' not in request.json or 'dogbreedId' not in request.json:
        return jsonify({'error': 'stName and dogbreedId are required'}), 400

    new_symptom = {
        'stId': dogsymptoms.find().count() + 1,
        'stName': request.json['stName'],
        'dogbreedId': request.json['dogbreedId']
    }

    dogsymptoms.insert_one(new_symptom)
    return dumps({'symptom': new_symptom}), 201


# UPDATE dog symptom for a specific dog breed
@app.route('/dogsymptoms/<int:dogbreedId>', methods=['PUT'])
def update_dog_symptom(dogbreedId):
    symptom = dogsymptoms.find_one({'dogbreedId': dogbreedId})
    if symptom is None:
        return jsonify({'error': 'Symptom not found'}), 404

    dogsymptoms.update_one(
        {'dogbreedId': dogbreedId},
        {
            '$set': {
                'stName': request.json.get('stName', symptom['stName']),
                'dogbreedId': request.json.get('dogbreedId', symptom['dogbreedId']),
            }
        }
    )

    return dumps({'symptom': dogsymptoms.find_one({'dogbreedId': dogbreedId})})


# DELETE dog symptom for a specific dog breed
@app.route('/dogsymptoms/<int:dogbreedId>', methods=['DELETE'])
def delete_dog_symptom(dogbreedId):
    result = dogsymptoms.delete_one({'dogbreedId': dogbreedId})
    if result.deleted_count == 0:
        return jsonify({'error': 'Symptom not found'}), 404

    return jsonify({'result': True})


# SEARCH for symptom based on dog breed's unique ID
@app.route('/dogsymptoms/breed/<int:dogbreedId>', methods=['GET'])
def get_symptom_by_breed_id(dogbreedId):
    symptoms = dogsymptoms.find({'dogbreedId': dogbreedId})
    return dumps({'dogbreedId': dogbreedId, 'symptoms': list(symptoms)})


# SEARCH for dog breed based on symptom's name
@app.route('/dogsymptoms/name/<string:stName>', methods=['GET'])
def get_breed_by_symptom_name(stName):
    symptom = dogsymptoms.find_one({'stName': stName})
    if symptom is None:
        return jsonify({'error': 'Symptom not found'}), 404

    return dumps({'breed': dogs.find_one({'dogbreedId': symptom['dogbreedId']})})


# GET list of symptoms based on a specific dog breed
@app.route('/dogsymptoms/breed/<int:dogbreedId>', methods=['GET'])
def get_symptoms_by_breed(dogbreedId):
    symptoms = dogsymptoms.find({'dogbreedId': dogbreedId})
    return dumps({'dogbreedId': dogbreedId, 'symptoms': list(symptoms)})


# GET list of possible diseases based on the dog's symptom
@app.route('/dogsymptoms/diseases/<string:stName>', methods=['GET'])
def get_possible_diseases_by_symptom(stName):
    symptom = dogsymptoms.find_one({'stName': stName})
    if symptom is None:
        return jsonify({'error': 'Symptom not found'}), 404

    diseases = dogdiseases.find({'dogbreedId': symptom['dogbreedId']})
    return dumps({'symptom': stName, 'possible_diseases': list(diseases)})


# GET list of possible allergies based on the dog's symptom
@app.route('/dogsymptoms/allergies/<string:stName>', methods=['GET'])
def get_possible_allergies_by_symptom(stName):
    symptom = dogsymptoms.find_one({'stName': stName})
    if symptom is None:
        return jsonify({'error': 'Symptom not found'}), 404

    allergies = dogallergies.find({'dogbreedId': symptom['dogbreedId']})
    return dumps({'symptom': stName, 'possible_allergies': list(allergies)})


# ---------------------------- DOG ALLERGIES ROUTE -------------------------------------------

# Create a new allergy
@app.route('/dogallergies', methods=['POST'])
def create_allergy():
    new_allergy_data = request.get_json()
    new_allergy_data['algId'] = dogallergies.find().count() + 1
    dogallergies.insert_one(new_allergy_data)
    return dumps({'allergy': new_allergy_data}), 201


# Create a new allergy for a specific dog breed
@app.route('/dogallergies/<breed>', methods=['POST'])
def create_allergy_for_breed(breed):
    new_allergy_data = request.get_json()
    new_allergy_data['breed'] = breed
    new_allergy_data['algId'] = dogallergies.find().count() + 1
    dogallergies.insert_one(new_allergy_data)
    return dumps({'allergy': new_allergy_data}), 201


# Search for an allergy based on the dog breed’s unique ID
@app.route('/dogallergies/<int:algId>', methods=['GET'])
def get_allergy_by_id(algId):
    allergy = dogallergies.find_one({'algId': algId})
    if allergy is None:
        return jsonify({'error': 'Allergy not found'}), 404
    return dumps({'allergy': allergy})


# Update the allergy for a specific dog breed
@app.route('/dogallergies/<breed>', methods=['PUT'])
def update_allergy_for_breed(breed):
    query = {'breed': breed}
    allergy = dogallergies.find_one(query)
    if allergy is None:
        return jsonify({'error': 'Allergy not found'}), 404

    update_data = request.get_json()
    dogallergies.update_one(query, {'$set': update_data})
    updated_allergy = dogallergies.find_one(query)

    return dumps({'allergy': updated_allergy})


# Delete an allergy for a specific dog breed
@app.route('/dogallergies/<breed>', methods=['DELETE'])
def delete_allergy_for_breed(breed):
    result = dogallergies.delete_one({'breed': breed})
    if result.deleted_count == 0:
        return jsonify({'error': 'Allergy not found'}), 404

    return jsonify({'result': True})


# Search for a dog breed based on the allergy’s name
@app.route('/breeds/<allergy_name>', methods=['GET'])
def get_breed_by_allergy_name(allergy_name):
    breed = dogallergies.find_one({'name': allergy_name})
    if breed is None:
        return jsonify({'error': 'Breed not found for the given allergy'}), 404

    return dumps({'breed': breed['breed']})


# Get the list of allergies based on a specific dog breed
@app.route('/dogbreeds/<breed>/allergies', methods=['GET'])
def get_allergies_for_breed(breed):
    allergies = dogallergies.find({'breed': breed})
    return dumps({'breed': breed, 'allergies': list(allergies)})


# --------------------------- DOG VACCINES ROUTE --------------------------------------

# Create a new vaccine
@app.route('/dogvaccines', methods=['POST'])
def create_vaccine():
    new_vaccine_data = request.get_json()
    new_vaccine_data['vacId'] = dogvaccines.find().count() + 1
    dogvaccines.insert_one(new_vaccine_data)
    return dumps({'vaccine': new_vaccine_data}), 201


# Create a new vaccine for a specific dog breed
@app.route('/dogvaccines/<breed>', methods=['POST'])
def create_vaccine_for_breed(breed):
    new_vaccine_data = request.get_json()
    new_vaccine_data['breed'] = breed
    new_vaccine_data['vacId'] = dogvaccines.find().count() + 1
    dogvaccines.insert_one(new_vaccine_data)
    return dumps({'vaccine': new_vaccine_data}), 201


# Search for a vaccine based on the dog breed’s unique ID
@app.route('/dogvaccines/<int:vacId>', methods=['GET'])
def get_vaccine_by_id(vacId):
    vaccine = dogvaccines.find_one({'vacId': vacId})
    if vaccine is None:
        return jsonify({'error': 'Vaccine not found'}), 404
    return dumps({'vaccine': vaccine})


# Update the vaccine for a specific dog breed
@app.route('/dogvaccines/<breed>', methods=['PUT'])
def update_vaccine_for_breed(breed):
    query = {'breed': breed}
    vaccine = dogvaccines.find_one(query)
    if vaccine is None:
        return jsonify({'error': 'Vaccine not found'}), 404

    update_data = request.get_json()
    dogvaccines.update_one(query, {'$set': update_data})
    updated_vaccine = dogvaccines.find_one(query)

    return dumps({'vaccine': updated_vaccine})


# Delete a vaccine for a specific dog breed
@app.route('/dogvaccines/<breed>', methods=['DELETE'])
def delete_vaccine_for_breed(breed):
    result = dogvaccines.delete_one({'breed': breed})
    if result.deleted_count == 0:
        return jsonify({'error': 'Vaccine not found'}), 404

    return jsonify({'result': True})


# Search for a dog breed based on the vaccine’s name
@app.route('/breeds/<vaccine_name>', methods=['GET'])
def get_breed_by_vaccine_name(vaccine_name):
    breed = dogvaccines.find_one({'name': vaccine_name})
    if breed is None:
        return jsonify({'error': 'Breed not found for the given vaccine'}), 404

    return dumps({'breed': breed['breed']})


# Get the list of vaccines based on a specific dog breed
@app.route('/dogbreeds/<breed>/vaccines', methods=['GET'])
def get_vaccines_for_breed(breed):
    vaccines = dogvaccines.find({'breed': breed})
    return dumps({'breed': breed, 'vaccines': list(vaccines)})


# ------------------------------ DOG MEDICATIONS ROUTE ------------------------------------------

# Create a new medication
@app.route('/dogmedications', methods=['POST'])
def create_medication():
    new_medication_data = request.get_json()
    new_medication_data['medId'] = dogmedications.find().count() + 1
    dogmedications.insert_one(new_medication_data)
    return dumps({'medication': new_medication_data}), 201


# Create a new medication for a specific dog breed
@app.route('/dogmedications/<int:dogbreedId>', methods=['POST'])
def create_medication_for_breed(dogbreedId):
    new_medication_data = request.get_json()
    new_medication_data['dogbreedId'] = dogbreedId
    new_medication_data['medId'] = dogmedications.find().count() + 1
    dogmedications.insert_one(new_medication_data)
    return dumps({'medication': new_medication_data}), 201


# Search for a medication based on the dog breed’s unique ID
@app.route('/dogmedications/<int:dogbreedId>', methods=['GET'])
def get_medication_by_id(dogbreedId):
    medication = dogmedications.find_one({'dogbreedId': dogbreedId})
    if medication is None:
        return jsonify({'error': 'Medication not found'}), 404
    return dumps({'medication': medication})


# Update the medication for a specific dog breed
@app.route('/dogmedications/<int:dogbreedId>', methods=['PUT'])
def update_medication_for_breed(dogbreedId):
    query = {'dogbreedId': dogbreedId}
    medication = dogmedications.find_one(query)
    if medication is None:
        return jsonify({'error': 'Medication not found'}), 404

    update_data = request.get_json()
    dogmedications.update_one(query, {'$set': update_data})
    updated_medication = dogmedications.find_one(query)

    return dumps({'medication': updated_medication})


# Delete a medication for a specific dog breed
@app.route('/dogmedications/<int:dogbreedId>', methods=['DELETE'])
def delete_medication_for_breed(dogbreedId):
    result = dogmedications.delete_one({'dogbreedId': dogbreedId})
    if result.deleted_count == 0:
        return jsonify({'error': 'Medication not found'}), 404

    return jsonify({'result': True})


# Search for a dog breed based on the medication’s name
@app.route('/breeds/medication/<medication_name>', methods=['GET'])
def get_breed_by_medication_name(medication_name):
    breed = dogmedications.find_one({'name': medication_name})
    if breed is None:
        return jsonify({'error': 'Breed not found for the given medication'}), 404

    return dumps({'breed': breed['dogbreedId']})


# Get the list of medications based on a specific dog breed
@app.route('/dogbreeds/<int:dogbreedId>/medications', methods=['GET'])
def get_medications_for_breed(dogbreedId):
    medications = dogmedications.find({'dogbreedId': dogbreedId})
    return dumps({'dogbreedId': dogbreedId, 'medications': list(medications)})


# -------------------------- DOG DIET ROUTE ------------------------------------------

# Create a new diet
@app.route('/dogdiet', methods=['POST'])
def create_food():
    new_food_data = request.get_json()
    new_food_data['foodId'] = dogdiet.find().count() + 1
    dogdiet.insert_one(new_food_data)
    return dumps({'food': new_food_data}), 201


# Create a new diet for a specific dog breed
@app.route('/dogdiet/<int:dogbreedId>', methods=['POST'])
def create_food_for_breed(dogbreedId):
    new_food_data = request.get_json()
    new_food_data['dogbreedId'] = dogbreedId
    new_food_data['foodId'] = dogdiet.find().count() + 1
    dogdiet.insert_one(new_food_data)
    return dumps({'food': new_food_data}), 201


# Search for a diet based on the dog breed’s unique ID
@app.route('/dogdiet/<int:dogbreedId>', methods=['GET'])
def get_food_by_id(dogbreedId):
    food = dogdiet.find_one({'dogbreedId': dogbreedId})
    if food is None:
        return jsonify({'error': 'Food not found'}), 404
    return dumps({'food': food})


# Update the diet for a specific dog breed
@app.route('/dogdiet/<int:dogbreedId>', methods=['PUT'])
def update_food_for_breed(dogbreedId):
    query = {'dogbreedId': dogbreedId}
    food = dogdiet.find_one(query)
    if food is None:
        return jsonify({'error': 'Food not found'}), 404

    update_data = request.get_json()
    dogdiet.update_one(query, {'$set': update_data})
    updated_food = dogdiet.find_one(query)

    return dumps({'food': updated_food})


# Delete a diet for a specific dog breed
@app.route('/dogdiet/<int:dogbreedId>', methods=['DELETE'])
def delete_food_for_breed(dogbreedId):
    result = dogdiet.delete_one({'dogbreedId': dogbreedId})
    if result.deleted_count == 0:
        return jsonify({'error': 'Food not found'}), 404

    return jsonify({'result': True})


# Search for a dog breed based on the diet's name
@app.route('/breeds/food/<food_name>', methods=['GET'])
def get_breed_by_food_name(food_name):
    breed = dogdiet.find_one({'name': food_name})
    if breed is None:
        return jsonify({'error': 'Breed not found for the given food'}), 404

    return dumps({'breed': breed['dogbreedId']})


# Get the list of diets based on a specific dog breed
@app.route('/dogbreeds/<int:dogbreedId>/diets', methods=['GET'])
def get_diets_for_breed(dogbreedId):
    diets = dogdiet.find({'dogbreedId': dogbreedId})
    return dumps({'dogbreedId': dogbreedId, 'diets': list(diets)})


# ---------------------------- USER ROUTE -------------------------------------------

# Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    new_user_data = request.get_json()
    new_user_data['password'] = generate_password_hash(new_user_data['password'], method='sha256')
    new_user_data['userId'] = users.find().count() + 1
    users.insert_one(new_user_data)
    return dumps({'user': new_user_data}), 201

# Update user information
@app.route('/users/<int:userId>', methods=['PUT'])
def update_user(userId):
    user = users.find_one({'userId': userId})
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    update_data = request.get_json()
    users.update_one({'userId': userId}, {'$set': update_data})
    updated_user = users.find_one({'userId': userId})

    return dumps({'user': updated_user})

# Delete user
@app.route('/users/<int:userId>', methods=['DELETE'])
def delete_user(userId):
    result = users.delete_one({'userId': userId})
    if result.deleted_count == 0:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'result': True})

# User login
@app.route('/users/login', methods=['POST'])
def user_login():
    login_data = request.get_json()
    user = users.find_one({'userName': login_data['userName']})
    if user and check_password_hash(user['password'], login_data['password']):
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

# Change password of user
@app.route('/users/<int:userId>/change-password', methods=['PUT'])
def change_user_password(userId):
    user = users.find_one({'userId': userId})
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    update_data = request.get_json()
    update_data['password'] = generate_password_hash(update_data['password'], method='sha256')

    users.update_one({'userId': userId}, {'$set': update_data})
    updated_user = users.find_one({'userId': userId})

    return dumps({'user': updated_user})

# Create a new admin user
@app.route('/admins', methods=['POST'])
def create_admin():
    new_admin_data = request.get_json()
    new_admin_data['password'] = generate_password_hash(new_admin_data['password'], method='sha256')
    new_admin_data['adminId'] = admins.find().count() + 1
    admins.insert_one(new_admin_data)
    return dumps({'admin': new_admin_data}), 201

# Update admin user information
@app.route('/admins/<int:adminId>', methods=['PUT'])
def update_admin(adminId):
    admin = admins.find_one({'adminId': adminId})
    if admin is None:
        return jsonify({'error': 'Admin not found'}), 404

    update_data = request.get_json()
    admins.update_one({'adminId': adminId}, {'$set': update_data})
    updated_admin = admins.find_one({'adminId': adminId})

    return dumps({'admin': updated_admin})

# Delete admin user
@app.route('/admins/<int:adminId>', methods=['DELETE'])
def delete_admin(adminId):
    result = admins.delete_one({'adminId': adminId})
    if result.deleted_count == 0:
        return jsonify({'error': 'Admin not found'}), 404

    return jsonify({'result': True})

# Admin user login
@app.route('/admins/login', methods=['POST'])
def admin_login():
    login_data = request.get_json()
    admin = admins.find_one({'userName': login_data['userName']})
    if admin and check_password_hash(admin['password'], login_data['password']):
        return jsonify({'message': 'Admin login successful'})
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

# Change password of admin
@app.route('/admins/<int:adminId>/change-password', methods=['PUT'])
def change_admin_password(adminId):
    admin = admins.find_one({'adminId': adminId})
    if admin is None:
        return jsonify({'error': 'Admin not found'}), 404

    update_data = request.get_json()
    update_data['password'] = generate_password_hash(update_data['password'], method='sha256')

    admins.update_one({'adminId': adminId}, {'$set': update_data})
    updated_admin = admins.find_one({'adminId': adminId})

    return dumps({'admin': updated_admin})


if __name__ == '__main__':
    app.run(debug=True)
