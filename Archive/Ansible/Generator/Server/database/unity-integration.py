from flask import jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
unity_database_connection = Blueprint('unity-database_connection', __name__)

@unity_database_connection.route('/list', methods=['GET', 'POST'])
def fetch_player_list():
    fetch_result = userlist.query.all() # / profiles / users table on Supabase instance
    return jsonify([str(result) for result in fetch_result])

class userlist(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    
    def __repr__(self):
        return '... {0}: {1}: ...'