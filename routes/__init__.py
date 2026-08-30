import importlib
import os
import pkgutil
from flask import Blueprint


def register_blueprints(app):
    """Auto-discover and register all blueprints recursively."""
    package_dir = os.path.dirname(__file__)
    register_from_package(app, package_dir, 'routes')


def register_from_package(app, package_dir, package_name):
    """Recursively register blueprints from a package."""
    for module_info in pkgutil.iter_modules([package_dir]):
        if module_info.name.startswith('_'):
            continue
        
        if module_info.ispkg:
            sub_package_dir = os.path.join(package_dir, module_info.name)
            sub_package_name = f'{package_name}.{module_info.name}'
            register_from_package(app, sub_package_dir, sub_package_name)
        else:
            module = importlib.import_module(f'{package_name}.{module_info.name}')
            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)
                if isinstance(attribute, Blueprint):
                    app.register_blueprint(attribute)
                    app.logger.info(f'Registered blueprint: {attribute.name}')
                    # print(f'Registered blueprint: {attribute.name}')
