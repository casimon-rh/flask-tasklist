"""Main model"""
from app import BD_
from flask_bcrypt import Bcrypt

class User(BD_.Model):
    """This class defines the users table """

    __tablename__ = 'users'

    # Define the columns of the users table, starting with the primary key
    id = BD_.Column(BD_.Integer, primary_key=True)
    email = BD_.Column(BD_.String(256), nullable=False, unique=True)
    password = BD_.Column(BD_.String(256), nullable=False)
    bucketlists = BD_.relationship(
        'Bucketlist', order_by='Bucketlist.id', cascade="all, delete-orphan")

    def __init__(self, email, password):
        """Initialize the user with an email and a password."""
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        """Save a user to the database.
        This includes creating a new user and editing one.
        """
        BD_.session.add(self)
        BD_.session.commit()


class Bucketlist(BD_.Model):
    """This class represents the bucketlist table."""

    __tablename__ = 'bucketlists'

    id = BD_.Column(BD_.Integer, primary_key=True)
    name = BD_.Column(BD_.String(255))
    date_created = BD_.Column(BD_.DateTime, default=BD_.func.current_timestamp())
    date_modified = BD_.Column(
        BD_.DateTime, default=BD_.func.current_timestamp(),
        onupdate=BD_.func.current_timestamp())
    created_by = BD_.Column(BD_.Integer, BD_.ForeignKey(User.id))


    def __init__(self, name, created_by):
        """initialize with name and its kreator."""
        self.name = name
        self.created_by = created_by

    def save(self):
        """Save bucket"""
        BD_.session.add(self)
        BD_.session.commit()

    @staticmethod
    def get_all(user_id):
        """Get all from list"""
        return Bucketlist.query.filter_by(created_by=user_id)

    def delete(self):
        """Delelte one"""
        BD_.session.delete(self)
        BD_.session.commit()

    def __repr__(self):
        """Tostring"""
        return "<Bucketlist: {}>".format(self.name)
