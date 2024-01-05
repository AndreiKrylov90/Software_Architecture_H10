from flask import Flask, request
from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vet_clinic.db'
db = SQLAlchemy(app)

api = Api(app, version='1.0', title='Vet Clinic API', description='API for Vet Clinic')

# Модель для Client
client_model = api.model('Client', {
    'ClientId': fields.Integer(readonly=True),
    'Document': fields.String(required=True),
    'SurName': fields.String(required=True),
    'FirstName': fields.String(required=True),
    'Patronymic': fields.String(),
    'Birthday': fields.Integer()
})

# Модель для Pet
pet_model = api.model('Pet', {
    'PetId': fields.Integer(readonly=True),
    'ClientId': fields.Integer(required=True),
    'Name': fields.String(required=True),
    'Birthday': fields.Integer()
})

# Модель для Consultation
consultation_model = api.model('Consultation', {
    'ConsultationId': fields.Integer(readonly=True),
    'ClientId': fields.Integer(required=True),
    'PetId': fields.Integer(required=True),
    'ConsultationDate': fields.Integer(),
    'Description': fields.String()
})


# Классы моделей для работы с базой данных
class Client(db.Model):
    ClientId = db.Column(db.Integer, primary_key=True)
    Document = db.Column(db.String(255), nullable=False)
    SurName = db.Column(db.String(255), nullable=False)
    FirstName = db.Column(db.String(255), nullable=False)
    Patronymic = db.Column(db.String(255))
    Birthday = db.Column(db.Integer)


class Pet(db.Model):
    PetId = db.Column(db.Integer, primary_key=True)
    ClientId = db.Column(db.Integer, nullable=False)
    Name = db.Column(db.String(255), nullable=False)
    Birthday = db.Column(db.Integer)


class Consultation(db.Model):
    ConsultationId = db.Column(db.Integer, primary_key=True)
    ClientId = db.Column(db.Integer, nullable=False)
    PetId = db.Column(db.Integer, nullable=False)
    ConsultationDate = db.Column(db.Integer)
    Description = db.Column(db.String(255))


# Создание таблиц в базе данных
db.create_all()


# Контроллеры для работы с данными
@api.route('/clients')
class ClientResource(Resource):
    @api.marshal_with(client_model, as_list=True)
    def get(self):
        return Client.query.all()

    @api.expect(client_model)
    @api.marshal_with(client_model)
    def post(self):
        new_client = Client(**request.json)
        db.session.add(new_client)
        db.session.commit()
        return new_client


@api.route('/pets')
class PetResource(Resource):
    @api.marshal_with(pet_model, as_list=True)
    def get(self):
        return Pet.query.all()

    @api.expect(pet_model)
    @api.marshal_with(pet_model)
    def post(self):
        new_pet = Pet(**request.json)
        db.session.add(new_pet)
        db.session.commit()
        return new_pet


@api.route('/consultations')
class ConsultationResource(Resource):
    @api.marshal_with(consultation_model, as_list=True)
    def get(self):
        return Consultation.query.all()

    @api.expect(consultation_model)
    @api.marshal_with(consultation_model)
    def post(self):
        new_consultation = Consultation(**request.json)
        db.session.add(new_consultation)
        db.session.commit()
        return new_consultation


if __name__ == '__main__':
    app.run(debug=True)