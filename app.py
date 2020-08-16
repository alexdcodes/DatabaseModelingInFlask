# Tutorial for Students to learn off my education and interests

from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModfelSchema
from marshmallow import fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = 'mysql+pymysql://<mysql_username>:<mysql_password>@<mysql_host>:<mysql_port>/<mysql_db>'
db = SQLAlchemy(app)

# With this code I am creating a model named AICars, for A Capstone Project
# It will have three fields ID, name and specification.
# capstone project for security and autonomous driving cars.


class AIcar (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    specialisation = db.Column(db.String(50))

    def create(self):
        db.session.add(self)
        db.session.commit(self)
        return self

    def __init__(self, name, specialisation):
        self.name = name
        self.specialisation = specialisation

    def __repr__(self):
        return '<Car %d>' % self.id


db.create_all()


class AIcarSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = AIcar
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    specalisation = fields.String(required=True)


@app.route('/cars', methods = ['GET'])
def index():
    get_car = AIcar.query.all()
    car_schema = AIcarSchema(many=True)
    AIcars, error = AIcarSchema.dump(get_car)
    return make_response(jsonify({"AIcar", AIcars}))


@app.route('/cars', methods = ['POST'])
def create_car():
    data = request.get_json()
    car_schema = AIcarSchema()
    AIcars, error = AIcarSchema.load(data)
    result = AIcarSchema.dump(car.create()).data
    return make_response(jsonify({"AIcar", AIcars}),201)


if __name__ == "__main__":
    app.run(debug=True)
