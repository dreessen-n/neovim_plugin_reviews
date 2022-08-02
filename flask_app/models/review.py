# Import mysqlconnection config
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
from flask_app.models import user

"""
Change class construct, queries, and db for review
"""

class Review:
    # Use a alias for the database; call in classmethods as cls.db
    # For staticmethod need to call the database name not alias
    db = "neovim_plugin_reviews"

    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.category = data['category']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        # Needed to create this to capture the creator of the review
        self.creator = None
        self.user_ids_who_liked = []
        self.users_who_liked = []

    # CRUD CREATE METHODS
    @classmethod
    def create_review(cls,data):
        """Create a review"""
        query = "INSERT INTO reviews (name, category, content, user_id) VALUES (%(name)s, %(category)s, %(content)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def like(cls,data):
        query = "INSERT INTO likes (user_id, review_id) VALUES (%(user_id)s, %(id)s);"
        return connectToMySQL(cls.db).query_db(query,data)


    # CRUD READ METHODS -- Modified for many to many
    @classmethod
    def get_all_reviews(cls):
        """Get all the reviews in db"""
        query = '''SELECT * FROM reviews
                JOIN users AS creators ON reviews.user_id = creators.id
                LEFT JOIN likes ON likes.review_id = reviews.id
                LEFT JOIN users AS users_who_liked ON likes.user_id = users_who_liked.id
                ORDER BY reviews.name ASC;'''
        results = connectToMySQL(cls.db).query_db(query)
        all_reviews = []
        for r in results:
            new_review = True
            users_who_liked_data = {
                'id': r['users_who_liked.id'],
                'first_name': r['users_who_liked.first_name'],
                'last_name': r['users_who_liked.last_name'],
                'email': r['users_who_liked.email'],
                'password': r['users_who_liked.password'],
                'created_at': r['users_who_liked.created_at'],
                'updated_at': r['users_who_liked.updated_at']
            }
            # Check to see if previous processed review, exist as current row
            num_of_review = len(all_reviews)
            print(num_of_review)
            # Check to see if we have reviews in list
            # If num_of_review is > 0; then we have procesed a row/review
            # already
            if num_of_review > 0:
                # Check if last review equals current row
                last_review = all_reviews[num_of_review-1]
                if last_review.id == r['id']:
                    last_review.user_ids_who_liked.append(r['users_who_liked.id'])
                    last_review.users_who_liked.append(user.User(users_who_liked_data))
                    new_review = False
            # Create new review object if review has not been created
            # and added to the list
            if new_review:
                # Create the review object
                review = cls(r)
                # Create the associated User object; include all contructors
                user_data = {
                    'id': r['creators.id'],
                    'first_name': r['first_name'],
                    'last_name': r['last_name'],
                    'email': r['email'],
                    'password': r['password'],
                    'created_at': r['creators.created_at'],
                    'updated_at': r['creators.updated_at']
                }
                one_user = user.User(user_data)
                # Set user to creator in review
                review.creator = one_user
                # Check to see if any user liked this review
                if r['users_who_liked.id']:
                    review.user_ids_who_liked.append(r['users_who_liked.id'])
                    review.users_who_liked.append(user.User(users_who_liked_data))
                    print(review.users_who_liked)
                # Append the review to the all_review list
                all_reviews.append(review)
        return all_reviews

    @classmethod
    def get_one_review(cls,data):
        """Get one review to display"""
        query = '''SELECT * FROM reviews
                JOIN users AS creators ON reviews.user_id = creators.id
                LEFT JOIN likes ON likes.review_id = reviews.id
                LEFT JOIN users AS users_who_liked ON likes.user_id = users_who_liked.id
                WHERE reviews.id = %(id)s;'''
        result = connectToMySQL(cls.db).query_db(query, data)
        # Now due to fav and comments; we can get back multiple rows or no rows
        # (if no fav or on comments)
        # So we need to check for both conditions
        # First condition no results; return False
        if len(result) < 1:
            return False
        # Check if multiple rows (or fav and/or comments)
        # If one row then review so set to True to start check
        new_review = True
        for r in result:
            if new_review:
                # If this is the first row
                # Create the review object
                review = cls(result[0])
                # Create user_data dict for the creator of review
                user_data = {
                    'id': r['creators.id'],
                    'first_name': r['first_name'],
                    'last_name': r['last_name'],
                    'email': r['email'],
                    'password': r['password'],
                    'created_at': r['creators.created_at'],
                    'updated_at': r['creators.updated_at']
                }
                one_user = user.User(user_data)
                # Set one_user to creator in review
                review.creator = one_user
                # Set new_review to False once we create 
                new_review = False
            # if any fav data associate it with user
            if r['users_who_liked.id']:
                users_who_liked_data = {
                    'id': r['users_who_liked.id'],
                    'first_name': r['users_who_liked.first_name'],
                    'last_name': r['users_who_liked.last_name'],
                    'email': r['users_who_liked.email'],
                    'password': r['users_who_liked.password'],
                    'created_at': r['users_who_liked.created_at'],
                    'updated_at': r['users_who_liked.updated_at']
                }
                # Create instance of user who fav
                users_who_liked = user.User(users_who_liked_data)
                # Add user to users_who_liked list
                review.users_who_liked.append(users_who_liked)
                # Add users_who_liked id to user_ids_who_liked list
                review.user_ids_who_liked.append(r['users_who_liked.id'])
        return review

    # CRUD UPDATE METHODS
    @classmethod
    def update_review(cls,data):
        """Update the review"""
        query = "UPDATE reviews SET name=%(name)s, category=%(category)s, content=%(content)s WHERE reviews.id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    # CRUD DELETE METHODS
    @classmethod
    def delete_review(cls,data):
        """Delete review"""
        query = "DELETE FROM reviews WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def unlike(cls,data):
        query = "DELETE FROM likes WHERE user_id=%(user_id)s AND review_id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    # FORM VALIDATION
    @staticmethod
    def validate_form(review):
        """Validate the new review create form"""
        is_valid = True # We set True until False
        if len(review['name']) < 2:
            flash("The Name must be at least 2 characters.", "danger")
            is_valid = False
        if len(review['category']) < 2:
            flash("The Category must be at least 2 characters.", "danger")
            is_valid = False
        if len(review['content']) < 20:
            flash("The Content must be greater than 20.", "danger")
            is_valid = False
        return is_valid

