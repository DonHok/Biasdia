from data.db.db import Base
from sqlalchemy import Column, String


class Article(Base):

    __tablename__ = "Articles"

    publication = Column(String, primary_key=True)
    name = Column(String, primary_key=True)
    category = Column(String)
    author = Column(String)
    subcategory = Column(String)
    text = Column(String)

    def __repr__(self):
        return self.publication + "!$!" + self.author + "!$!" + self.name + "!$!" + self.category + "!$!" \
               + self.subcategory + "!$!" + self.text

