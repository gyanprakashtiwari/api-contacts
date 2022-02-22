from app import app ,db
from flask import request , jsonify ,make_response
from app.models import User , Contact
import jwt
from flask_jwt_extended import  create_access_token , create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager



@app.route("/")
def index():
    return {"message": "Welcome , but this method is not allowed"}

@app.route("/signup", methods=["POST"])
def signup():
    input_json = request.get_json()
    name = input_json['name']
    email = input_json['email']
    phone = input_json['phone']
    password = input_json['password']
    address = input_json['address']

    already_user = User.query.filter_by(email = email).first()
    if already_user is None:
        new_user = User(name=name,email=email,phone=phone,address=address)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        result_dict = {"message": "new user registered succesfully"}
        return jsonify(result_dict)
    else:
        result_dict = {"message": "The email is already registered. Please enter another email"}
        return jsonify(result_dict)



@app.route("/login", methods=["POST"])
def login():
    input_json = request.get_json()
    received_email = input_json['email']
    received_password = input_json['password']

    user = User.query.filter_by(email = received_email).first()

    if user is None:
        result_dict = {"message" : "email not registered , please signup first and then login"}
        return jsonify(result_dict)
    elif user.check_password(received_password):
        # generate access token and return for user to login
        access = create_access_token(identity = user.email)

        result_dict = {"message" : "login successful","user_id" :user.id , "email" : user.email ,"token":access }
        return jsonify(result_dict)
    else:
        result_dict = {"message" : "worng password entered"}
        return jsonify(result_dict)

    
@app.route("/user/<int:id>",methods = ['GET'])
@jwt_required()
def user_detail(id):
    create_user = get_jwt_identity()
    user = User.query.filter_by(id = id).first()
    if user is None:
        result_dict = {"status" : "Wrong user id used in url" }
        return jsonify(result_dict)
    else:
        if user.email == create_user:
            result_dict = {"logged in as ": create_user , "user_id": user.id }
            return jsonify(result_dict)
        else:
            result_dict = {"message" : "use the user_id that you logged in with"}
            return jsonify(result_dict)

    
@app.route("/user/<int:id>/contacts/add",methods = ['POST'])
@jwt_required()
def user_contacts_add(id):
    create_user = get_jwt_identity()
    user = User.query.filter_by(id = id).first()
    if user is None:
        result_dict = {"status" : "Wrong user id used in url" }
        return jsonify(result_dict)
    else:
        if user.email == create_user:
            input_json = request.get_json()

            name = input_json['name']
            email = input_json['email']
            address = input_json['address']
            country = input_json['country']
            phone = input_json['phone']

            contact = Contact(user_id = user.id,name=name,email=email,address=address,country=country,phone=phone)
            db.session.add(contact)
            db.session.commit()
            result_dict = {"message" : "contact added to your contact list"}
            return jsonify(result_dict)
        else:
            result_dict = {"message" : "use the user_id that you logged in with"}
            return jsonify(result_dict)


@app.route("/user/<int:id>/contacts/search",methods = ['GET'])
@jwt_required()
def user_contacts_search(id):
    create_user = get_jwt_identity()
    user = User.query.filter_by(id = id).first()
    if user is None:
        result_dict = {"status" : "Wrong user id used in url" }
        return jsonify(result_dict)
    else:
        if user.email == create_user:

            result_dict = []
            input_json = request.get_json()

            name = input_json['name']
            email = input_json['email']
            phone = input_json['phone']

            contacts = Contact.query.filter_by(user_id = user.id,name=name,email=email,phone=phone)

            for contact in  contacts:
                curr = {
                    "name": contact.name,
                    "email":contact.email,
                    "phone":contact.phone,
                    "address":contact.address,
                    "country":contact.country
                }
                result_dict.append(curr)

           
            
            return jsonify(result_dict)
        else:
            result_dict = {"message" : "use the user_id that you logged in with"}
            return jsonify(result_dict)




@app.route("/user/<int:id>/contacts",methods = ['GET'])
@jwt_required()
def user_contacts(id):
    create_user = get_jwt_identity()
    user = User.query.filter_by(id = id).first()
    if user is None:
        result_dict = {"status" : "Wrong user id used in url" }
        return jsonify(result_dict)
    else:
        if user.email == create_user:
            result_dict = []
            contacts = Contact.query.filter_by(user_id = user.id)

            for contact in contacts:
                curr = {
                    "name" : contact.name,
                    "phone" : contact.phone,
                    "email" : contact.email
                }
                result_dict.append(curr)

            return jsonify(result_dict)
        else:
            result_dict = {"message" : "use the user_id that you logged in with"}
            return jsonify(result_dict)
