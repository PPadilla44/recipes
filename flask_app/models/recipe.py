from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request
from flask_app import app

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_thirty = data['under_thirty']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_all_user_recipes(cls,data):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id \
        WHERE users.id = %(id)s ORDER BY recipes.updated_at DESC"
        recipes_from_db = connectToMySQL('recipes_schema').query_db(query,data)

        recipes = []
        for recipe in recipes_from_db:
            recipes.append(cls(recipe))
        return recipes


    @classmethod
    def delete_recipe(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL('recipes_schema').query_db(query,data)


    @classmethod
    def get_recipe_by_id(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL('recipes_schema').query_db(query,data)
        return cls(results[0])


    @classmethod
    def create_recipe(cls,data):
        query = "INSERT INTO recipes(user_id,name,description,instructions,under_thirty) \
        VALUES (%(user_id)s,%(name)s,%(description)s,%(instructions)s,%(under_thirty)s)"
        return connectToMySQL('recipes_schema').query_db(query,data)

    @classmethod
    def edit_recipe(cls,data):
        query = "UPDATE recipes SET name=%(name)s,description=%(description)s, \
        instructions=%(instructions)s,under_thirty=%(under_thirty)s, updated_at=NOW() \
        WHERE id=%(id)s;"
        return connectToMySQL('recipes_schema').query_db(query,data)


    @staticmethod
    def validate_recipe(recipe):
        is_valid = True

        if len(recipe['name']) < 3:
            flash('Name must be at least 3 characters long')
            is_valid = False
        if len(recipe['description']) < 3:
            flash('Description must be at least 3 characters long')
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash('Instructions must be at least 3 characters long')
            is_valid = False

        return is_valid
