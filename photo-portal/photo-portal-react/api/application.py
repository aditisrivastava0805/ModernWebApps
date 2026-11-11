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


class GeneralUser(Base):
    __tablename__ = "general_user"
    id = Column(Integer, primary_key=True)
    gmail = Column(String(120), unique=True, nullable=False)


class Photo(Base):
    __tablename__ = "photo"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    date_taken = Column(String(50))
    tags = Column(String(255))
    comments = Column(String(1000))


Base.metadata.create_all(engine)

# Seed the single pre-configured admin if none exists
with Session() as seed_db:
    if seed_db.query(Admin).count() == 0:
        seed_db.add(Admin(username="aditi@gmail.com", password=generate_password_hash("1234")))
        seed_db.commit()

# Requirement 2.1
# Add SQLAlchemy object to represent General User (refer assignment3)

# Requirement 3.1
# Add SQLAlchemy object to store photos; Add a column to store photo comments 


# Requirement 3.4
@app.route("/api/photos/<photo_name>/comments", methods=["GET"])
def get_photo_comments(photo_name):
    db = Session()
    try:
        photo = db.query(Photo).filter_by(name=photo_name).first()
        comments = photo.comments if photo and photo.comments else ""
    finally:
        db.close()
    return jsonify({"comments": comments})


# Requirement 3.3: Query the database to return photo metadata (date_taken and tags) for all photos
@app.route("/api/photos", methods=["GET"])
def get_photos():
    db = Session()
    try:
        photos = [{"name": p.name, "date_taken": p.date_taken, "tags": p.tags}
                  for p in db.query(Photo).all()]
    finally:
        db.close()
    return jsonify({"photos": photos})


# Requirement 5 -- Add search functionality
@app.route("/api/search", methods=["POST"])
def search_photos():
    data = request.get_json() or {}
    search_type = (data.get("type") or "").lower()
    query = (data.get("query") or "").strip()
    columns = {"name": Photo.name, "date": Photo.date_taken, "tags": Photo.tags}
    if search_type not in columns:
        return jsonify({"error": "Invalid search type"}), 400
    db = Session()
    try:
        photos = db.query(Photo).filter(columns[search_type].ilike(f"%{query}%")).all()
        results = [{"name": p.name, "date_taken": p.date_taken, "tags": p.tags} for p in photos]
    finally:
        db.close()
    return jsonify({"results": results})

@app.route('/api/upload', methods=['POST'])
def upload_photo():
    file = request.files.get('photo_file')
    date_taken = request.form.get('date_taken')
    tags = request.form.get('tags')
    comments = request.form.get('comments')

    # Requirement 3.2

    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    save_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(save_path)

    db = Session()
    try:
        photo = db.query(Photo).filter_by(name=file.filename).first()
        if photo:
            photo.date_taken = date_taken
            photo.tags = tags
            photo.comments = comments
        else:
            db.add(Photo(name=file.filename, date_taken=date_taken, tags=tags, comments=comments))
        db.commit()
    finally:
        db.close()

    return jsonify({
        'name': file.filename,
        'date_taken': date_taken,
        'tags': tags,
        'comments': comments
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

@app.route("/api/generaluser", methods=["POST"])
def add_generaluser():
    data = request.get_json() or {}
    gmail = data.get("gmail")
    if not gmail:
        return jsonify({"error": "gmail required"}), 400
    db = Session()
    try:
        if db.query(GeneralUser).filter_by(gmail=gmail).first():
            return jsonify({"error": "User already exists"}), 409
        user = GeneralUser(gmail=gmail)
        db.add(user)
        db.commit()
        return jsonify({"id": user.id, "gmail": user.gmail}), 201
    finally:
        db.close()


@app.route("/api/generaluser", methods=["GET"])
def get_generalusers():
    db = Session()
    try:
        users = [{"id": u.id, "gmail": u.gmail} for u in db.query(GeneralUser).all()]
        return jsonify({"generalusers": users})
    finally:
        db.close()

# Requirement 2.4 - Complete the generaluserlogin implementation
@app.route("/api/generaluserlogin", methods=["POST"])
def generaluser_login():
    data = request.get_json()
    print("Received:", data)
    username = data.get("gmail")
    db = Session()
    try:
        exists = db.query(GeneralUser).filter_by(gmail=username).first() is not None
    finally:
        db.close()
    if not exists:
        return jsonify({"message": "NotFound", "username": username})
    flask.session["username"] = username
    return jsonify({"message": "Success", "username": username})

# Requirement 2.3



@app.route("/api/logout",methods=['POST'])
def logout():
    data = request.get_json()
    print("Received:", data)
    username = data.get("userName")
    db = Session()
    try:
        is_admin = db.query(Admin).filter_by(username=username).first() is not None
    finally:
        db.close()
    user_type = "admin" if is_admin else "general"

    flask.session.clear()
    return jsonify({"message": "Success", "usertype": user_type})


if __name__ == "__main__":

    app.debug = False
    #app.logger.info('Portal started...')
    app.run(host='0.0.0.0', port=5000)
