from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
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
        ]
    }
    
    return jsonify(userData)

@app.route('/users', methods=['POST'])
def createUser():
    try:
        user_data = request.json['user']
        pathological_data = request.json['pathological_data']

        birth_date_str = user_data['birthDate']
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()

        new_user = User(
            cpf=user_data['cpf'],
            name=user_data['name'],
            email=user_data['email'],
            birthDate=birth_date,
            gender=user_data['gender'],
            status=user_data['status'],
            password=user_data['password'],
            type=user_data['type']
        )

        db.session.add(new_user)
        db.session.commit()

        print(new_user)

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

        return jsonify({"message": "User and pathological data created successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
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



if __name__ == '__main__':
    app.run(debug=True)