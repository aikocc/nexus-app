from flask import Flask, render_template
from dotenv import load_dotenv
import os
from extensions import db, csrf
from models import Customer, Vehicle, Lead
from routes import register_blueprints
import logging


load_dotenv()


def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///workshop.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    csrf.init_app(app)
    
    register_blueprints(app)
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.context_processor
    def utility_processor():
        return {
            'get_customer_full_name': lambda customer: customer.full_name if customer else ''
        }
    
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.logger.setLevel(logging.INFO)
    app.run(debug=True, host='0.0.0.0', port=5000)
