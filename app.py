from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from prognosis import calcular_pontuacao, obter_prognostico, obter_prognostico_humanizado

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(45))
    name = db.Column(db.String(45))
    email = db.Column(db.String(45))
    birthDate = db.Column(db.Date)
    gender = db.Column(db.String(1))
    status = db.Column(db.Boolean)
    password = db.Column(db.String(45))
    type = db.Column(db.String(45))
    
    pathological_data = db.relationship('PathologicalData', backref='user', lazy=True)
    prognosis = db.relationship('Prognosis', backref='user', lazy=True)

class PathologicalData(db.Model):
    __tablename__ = 'pathological_data'
    id = db.Column(db.Integer, primary_key=True)
    diff_diag = db.Column(db.String(45))
    encephalopathy = db.Column(db.String(45))
    ascites = db.Column(db.String(45))
    inr = db.Column(db.Float)
    total_bilirubin = db.Column(db.Float)
    albumin = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Prognosis(db.Model):
    __tablename__ = 'prognosis'
    id = db.Column(db.Integer, primary_key=True)
    class_ = db.Column(db.String(1))
    score = db.Column(db.Integer)
    one_year = db.Column(db.Float)
    two_years = db.Column(db.Float)
    perioperative_mortality = db.Column(db.String(45))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.Column(db.String(45))

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/users/<int:user_id>', methods=['GET'])
def getUserAllData(user_id):
    user = User.query.get(user_id)
    
    if user is None:
        return jsonify({"error": "User not found"}), 404
    
    userData = {
        'id': user.id,
        'cpf': user.cpf,
        'name': user.name,
        'email': user.email,
        'birthDate': user.birthDate,
        'gender': user.gender,
        'status': user.status,
        'type': user.type,
        'pathological_data': [
            {
                'diff_diag': data.diff_diag,
                'encephalopathy': data.encephalopathy,
                'ascites': data.ascites,
                'inr': data.inr,
                'total_bilirubin': data.total_bilirubin,
                'albumin': data.albumin
            } for data in user.pathological_data
        ],
        'prognosis': [
            {
                'class': prognosis.class_,
                'score': prognosis.score,
                'one_year': prognosis.one_year,
                'two_years': prognosis.two_years,
                'perioperative_mortality': prognosis.perioperative_mortality,
                'comments': prognosis.comments
            } for prognosis in user.prognosis
        ],
        'humanized_prognosis': obter_prognostico_humanizado(user.prognosis[-1].class_)
    }
    
    return jsonify(userData)

@app.route('/users', methods=['POST'])
def createUser():
    try:
        data = request.json
        pathological_data = request.json['pathological_data']

        birth_date_str = data['birthDate']
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        
        new_user = User(
            cpf=data['cpf'],
            name=data['name'],
            email=data['email'],
            birthDate=birth_date,
            gender=data['gender'],
            status=data['status'],
            password=data['password'],
            type=data['type']
        )


        db.session.add(new_user)
        db.session.commit()


        new_pathological_data = PathologicalData(
            diff_diag=pathological_data['diff_diag'],
            encephalopathy=pathological_data['encephalopathy'],
            ascites=pathological_data['ascites'],
            inr=pathological_data['inr'],
            total_bilirubin=pathological_data['total_bilirubin'],
            albumin=pathological_data['albumin'],
            user_id=new_user.id
        )

        db.session.add(new_pathological_data)
        db.session.commit()

        classe, pontuacao = calcular_pontuacao(pathological_data['encephalopathy'], pathological_data['ascites'], pathological_data['inr'], pathological_data['total_bilirubin'], pathological_data['albumin'])
        prognostico = obter_prognostico(classe, pontuacao)

        new_prognosis = Prognosis(
            class_=classe,
            score=pontuacao,
            one_year=prognostico['sobrevida_1_ano'],
            two_years=prognostico['sobrevida_2_anos'],
            perioperative_mortality=prognostico['mortalidade_perioperatoria'],
            user_id=new_user.id,
            comments=prognostico['recommendations']
        )

        db.session.add(new_prognosis)
        db.session.commit()

        return jsonify({"message": "User, pathological and prognosis data created successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@app.route('/users', methods=['GET'])
def getAllUsers():
    users = User.query.all()
    
    if not users:
        return jsonify({"message": "No users found"}), 404

    allUsers = []
    for user in users:
        userData = {
            'id': user.id,
            'cpf': user.cpf,
            'name': user.name,
            'email': user.email,
            'birthDate': user.birthDate,
            'gender': user.gender,
            'status': user.status,
            'type': user.type,
        }
        allUsers.append(userData)

    return jsonify(allUsers), 200

@app.route('/users/<int:user_id>', methods=['PUT'])
def updateUser(user_id):
    try:
        user = User.query.get(user_id)

        if user is None:
            return jsonify({"error": "User not found"}), 404

        data = request.json
        pathological_data = request.json['pathological_data']

        birth_date_str = data['birthDate']
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()

        user.cpf = data['cpf']
        user.name = data['name']
        user.email = data['email']
        user.birthDate = birth_date
        user.gender = data['gender']
        user.status = data['status']
        user.type = data['type']

        db.session.commit()

        user_pathological_data = PathologicalData.query.filter_by(user_id=user_id).first()
        user_pathological_data.diff_diag = pathological_data['diff_diag']
        user_pathological_data.encephalopathy = pathological_data['encephalopathy']
        user_pathological_data.ascites = pathological_data['ascites']
        user_pathological_data.inr = pathological_data['inr']
        user_pathological_data.total_bilirubin = pathological_data['total_bilirubin']
        user_pathological_data.albumin = pathological_data['albumin']

        db.session.commit()

        classe, pontuacao = calcular_pontuacao(pathological_data['encephalopathy'], pathological_data['ascites'], pathological_data['inr'], pathological_data['total_bilirubin'], pathological_data['albumin'])
        prognostico = obter_prognostico(classe, pontuacao)

        user_prognosis = Prognosis.query.filter_by(user_id=user_id).first()
        user_prognosis.class_ = classe
        user_prognosis.score = pontuacao

        user_prognosis.one_year = prognostico['sobrevida_1_ano']
        user_prognosis.two_years = prognostico['sobrevida_2_anos']
        user_prognosis.perioperative_mortality = prognostico['mortalidade_perioperatoria']
        user_prognosis.comments = prognostico['recommendations']

        db.session.commit()

        return jsonify({"message": "User, pathological and prognosis data updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

        


if __name__ == '__main__':
    app.run(debug=True)