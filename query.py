"""

This file is the place to write solutions for the
skills assignment called skills-sqlalchemy. Remember to
consult the exercise instructions for more complete
explanations of the assignment.

All classes from model.py are being imported for you
here, so feel free to refer to classes without the
[model.]User prefix.

"""

from model import *

init_app()


# -------------------------------------------------------------------
# Part 2: Discussion Questions


# 1. What is the datatype of the returned value of
# ``Brand.query.filter_by(name='Ford')``?

# The returned value is a query object. 


# 2. In your own words, what is an association table, and what type of
# relationship (many to one, many to many, one to one, etc.) does an
# association table manage?

# An association table is created when there is a many to many relationship between 
# two tables. The association table does not hold any meaningful fields, but instead
# manages one to many relationships between both of the original tables.

# -------------------------------------------------------------------
# Part 3: SQLAlchemy Queries


# Get the brand with the brand_id of ``ram``.
q1 = db.session.query(Brand).filter_by(brand_id='ram').one()

# Get all models with the name ``Corvette`` and the brand_id ``che``.
q2 = db.session.query(Model).filter_by(name='Corvette', brand_id='che').all()

# Get all models that are older than 1960.
q3 = db.session.query(Model).filter(Model.year < 1960).all()

# Get all brands that were founded after 1920.
q4 = db.session.query(Brand).filter(Brand.founded > 1920).all()

# Get all models with names that begin with ``Cor``.
q5 = db.session.query(Model).filter(Model.name.like('Cor%')).all()

# Get all brands that were founded in 1903 and that are not yet discontinued.
q6 = db.session.query(Brand).filter(Brand.founded == 1903, Brand.discontinued == None).all()

# Get all brands that are either 1) discontinued (at any time) or 2) founded
# before 1950.
q7 = db.session.query(Brand).filter((Brand.discontinued != None) | (Brand.founded < 1950)).all()

# Get all models whose brand_id is not ``for``.
q8 = db.session.query(Model).filter(Model.brand_id != 'for').all()


# -------------------------------------------------------------------
# Part 4: Write Functions


def get_model_info(year):
    """Takes in a year and prints out each model name, brand name, and brand
    headquarters for that year using only ONE database query."""

    model_info = db.session.query(Model.name, Brand.name, 
        Brand.headquarters).join(Brand).filter(Model.year == year).all()
    
    for model_name, brand_name, brand_year in model_info:
        print "Model name: %s, Brand name: %s, Brand headquarters: %s" % (model_name, 
                                                                          brand_name,
                                                                          brand_year) 

def get_brands_summary():
    """Prints out each brand name (once) and all of that brand's models,
    including their year, using only ONE database query."""

    brands = db.session.query(Brand.name, Model.name, Model.year).join(Model).all()

    brands_dict = {}

    for (brand, model, year) in brands:
        if brand not in brands_dict:
            brands_dict[brand] = [(model, year)]
        else:         
            brands_dict[brand].append((model, year))

    for brand in brands_dict:
        print "Brand: %s \nModel(s):" % (brand) 
        for model, year in brands_dict[brand]:
            print "- %s %s" % (model, year)
            

def search_brands_by_name(mystr):
    """Returns all Brand objects corresponding to brands whose names include
    the given string."""

    brand_objects = Brand.query.filter(Brand.name.like('%' + mystr + '%')).all()

    return brand_objects

def get_models_between(start_year, end_year):
    """Returns all Model objects corresponding to models made between
    start_year (inclusive) and end_year (exclusive)."""

    models = Model.query.filter(Model.year >= start_year, 
                                Model.year < end_year).all()

    return models

