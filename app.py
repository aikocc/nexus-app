from database import db

from flask import Flask, Blueprint # pyright: ignore[reportMissingImports]
from importlib import import_module
import os

def register_routes(app, directory, package_prefix=""):
    for entry in os.scandir(directory):
        # Skip dunder/private/cache dirs and files
        if entry.name.startswith(("_", ".")):
            continue

        if entry.is_dir():
            # Recurse into subdirectory
            sub_prefix = f"{package_prefix}.{entry.name}" if package_prefix else entry.name
            register_routes(app, entry.path, sub_prefix)

        elif entry.is_file() and entry.name.endswith(".py"):
            module_name = entry.name[:-3]  # strip .py
            full_module_path = (
                f"{package_prefix}.{module_name}" if package_prefix else module_name
            )

            module = import_module(full_module_path)

            # Register every Blueprint object found in the module
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, Blueprint):
                    app.register_blueprint(attr)
                    print(f"Registered blueprint '{attr.name}' from {full_module_path}")

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-me-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///nexus.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    register_routes(app, "routes", package_prefix="routes")

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

