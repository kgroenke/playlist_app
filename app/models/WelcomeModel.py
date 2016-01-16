"""
    Sample Model File

    A Model should be in charge of communicating with the Database.
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model

class WelcomeModel(Model):
    def __init__(self):
        super(WelcomeModel, self).__init__()

    def new_user(self, user_info):
        password = user_info['password']

        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []

        if len(user_info['first_name']) < 1:
            errors.append('First name cannot be blank')
        if len(user_info['last_name']) < 1:
            errors.append('Last name cannot be blank')
        if len(user_info['email']) < 1:
            errors.append('email cannot be blank')
        if not EMAIL_REGEX.match(user_info['email']):
            errors.append('Must enter a valid email')
        if len(user_info['password']) < 8:
            errors.append('Password must be at least 8 characters')
        if user_info['password'] != user_info['pw_confirm']:
            errors.append('Passwords must match')

        if errors:
            return {
            "status" : False,
            "errors" : errors
            }
            print errors['errors']

        else:
            pw_hash = self.bcrypt.generate_password_hash(password)
            registration_query = "INSERT INTO users (name, alias, email, password, created_at, updated_at) VALUES ('{}', '{}', '{}', '{}', NOW(), NOW())".format(user_info['name'], user_info['alias'], user_info['email'], pw_hash)
            self.db.query_db(registration_query)
            session['name'] = user_info['name']
            return{"status" : True}
    """
    Below is an example of a model method that queries the database for all users in a fictitious application

    def get_all_users(self):
        print self.db.query_db("SELECT * FROM users")

    Every model has access to the "self.db.query_db" method which allows you to interact with the database
    """

    """
    If you have enabled the ORM you have access to typical ORM style methods.
    See the SQLAlchemy Documentation for more information on what types of commands you can run.
    """
