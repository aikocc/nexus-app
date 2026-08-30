# Forms package initialization
# Import all form modules so they're available
from forms.public import auth_forms
from forms.customer import customer_forms
from forms.admin import customer_forms as admin_customer_forms
from forms.admin import vehicle_forms