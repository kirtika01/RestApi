from flask import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_marshmallow import Marshmallow

### Create an instance of flask
app = Flask(__name__)


db = SQLAlchemy()
ma = Marshmallow()

mysql = MySQL(app)


# Create a model for our table


class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False)
    phonenumber = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(150), nullable=False)

    def __init__(self, email, phonenumber, username):
        self.email = email
        self.phonenumber = phonenumber
        self.username = username


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "phonenumber", "username")


user_schema = UserSchema()
users_schema = UserSchema(many=True)

##MYSQL
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/user"

##SQLITE
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/user/add", methods=["POST"])
def add_user():
    _json = request.json
    email = _json["email"]
    phonenumber = _json["phonenumber"]
    username = _json["username"]
    new_user = user(email=email, phonenumber=phonenumber, username=username)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "the user has been added "})


@app.route("/user", methods=["GET"])
def get_product():
    users = []
    data = user.query.all()
    users = users_schema.dump(data)
    return jsonify(users)


@app.route("/user/<int:id>", methods=["GET"])
def user_byid(id):
    users = []
    data = user.query.get(id)
    users = user_schema.dump(data)
    return jsonify(users)


@app.route("/user/delete/<int:id>", methods=["POST"])
def delete_user(id):
    users = []
    data = user.query.get(id)
    if user is None:
        return jsonify(f"Error: the user doesn't exist")
    db.session.delete(data)
    db.session.commit()
    return jsonify({"message": "the user has been deleted"})




if __name__ == "__main__":
    app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)
