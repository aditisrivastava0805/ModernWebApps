from flask import Flask, request, jsonify
from flask_cors import CORS

import flask
from flask import session

import secrets
import os

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.secret_key = secrets.token_hex() 

UPLOAD_FOLDER = 'static/images/photos'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

engine = create_engine("sqlite:///photoportal.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)


# Requirement 1.1
class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(255), nullable=False)


Base.metadata.create_all(engine)

# Requirement 2.1
# Add SQLAlchemy object to represent General User (refer assignment3)

# Requirement 3.1
# Add SQLAlchemy object to store photos; Add a column to store photo comments 


# Requirement 3.4
@app.route("/api/photos/<photo_name>/comments", methods=["GET"])
def get_photo_comments(photo_name):
    print("Comments for:" + photo_name)
    comments = "This is comment 1"
    return jsonify({"comments": comments})


# Requirement 3.3: Query the database to return photo metadata (date_taken and tags) for all photos
@app.route("/api/photos", methods=["GET"])
def get_photos():
    photos = [{"name": p, "date_taken": "...", "tags": "..."} for p in os.listdir("static/images/photos")]
    return jsonify({"photos": photos})


# Requirement 5 -- Add search functionality - Refer to your assignment2 implementation

@app.route('/api/upload', methods=['POST'])
def upload_photo():
    file = request.files.get('photo_file')
    date_taken = request.form.get('date_taken')
    tags = request.form.get('tags')

    # Requirement 3.2

    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    save_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(save_path)

    # You’d normally save metadata to DB here
    return jsonify({
        'name': file.filename,
        'date_taken': date_taken,
        'tags': tags
    })

# -- Admin user -- 

@app.route("/api/admin", methods=["POST"])
def add_admin():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "username and password required"}), 400
    db = Session()
    try:
        if db.query(Admin).filter_by(username=username).first():
            return jsonify({"error": "User already exists"}), 409
        admin = Admin(username=username, password=generate_password_hash(password))
        db.add(admin)
        db.commit()
        return jsonify({"id": admin.id, "username": admin.username}), 201
    finally:
        db.close()


@app.route("/api/admin", methods=["GET"])
def get_admins():
    db = Session()
    try:
        admins = [{"id": a.id, "username": a.username} for a in db.query(Admin).all()]
        return jsonify({"admins": admins})
    finally:
        db.close()

# Requirement 1.4 - Complete the adminlogin implementation
@app.route("/api/adminlogin", methods=["POST"])
def admin_login():
    data = request.get_json()
    print("Received:", data)
    username = data.get("name")
    password = data.get("password")
    db = Session()
    try:
        admin = db.query(Admin).filter_by(username=username).first()
        valid = admin is not None and check_password_hash(admin.password, password or "")
    finally:
        db.close()
    if valid:
        flask.session["username"] = username
        return jsonify({"message": "Success", "username": username})
    else:
        return jsonify({"message": "NotFound", "username": username})

# -- General user --

# Requirement 2.2 - Add a POST call to register a general user

# Requirement 2.3 - Add a GET call to get all registered general users

# Requirement 2.4 - Complete the generaluserlogin implementation
@app.route("/api/generaluserlogin", methods=["POST"])
def generaluser_login():
    data = request.get_json()
    print("Received:", data)
    username = data.get("gmail")
    flask.session["username"] = username
    # Query database to check if username/password exists or  not
    # Replace the below if check with database query
    # If the generaluser is not present, return NotFound
    return jsonify({"message": "Success", "username": username})

# Requirement 2.3



@app.route("/api/logout",methods=['POST'])
def logout():
    data = request.get_json()
    print("Received:", data)
    username = data.get("userName")
    user_type = "admin"
    if "gmail.com" in username:
        user_type = "general"

    flask.session.clear()
    return jsonify({"message": "Success", "usertype": user_type})


if __name__ == "__main__":

    app.debug = False
    #app.logger.info('Portal started...')
    app.run(host='0.0.0.0', port=5000)
