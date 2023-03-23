from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

class DBStorage:
    """This class manages storage of hbnb models in a database"""
    __engine = None
    __session = None

    def __init__(self):
        """Create an instance of a DBStorage object"""
        self.__engine = create_engine('mysql+mysqldb://<user>:<password>@<host>/<database>',
                                       pool_pre_ping=True)
        if 'test' in sys.argv:
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        class_list = [BaseModel, User, Place, State, City, Amenity, Review]

        if cls is None:
            objs = {}
            for c in class_list:
                objs.update({obj.id: obj for obj in self.__session.query(c).all()})
            return objs
        else:
            if cls not in class_list:
                return {}
            return {obj.id: obj for obj in self.__session.query(cls).all()}

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes to the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an object from the database"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Loads all tables from the database"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))()

