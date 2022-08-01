
# Import mysqlconnection config
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash
from flask_app.models import user, review

"""
Change class construct, queries, and db for review
Check controllers import on server
"""

class Comment:
    # Use a alias for the database; call in classmethods as cls.db
    # For staticmethod need to call the database name not alias
    db = "neovim_plugin_reviews"

    def __init__(self,data):
        self.id = data['id']
        self.comment = data['comment']
        self.user_id = data['user_id']
        self.review_id = data['review_id']
        self.users_who_commented = user.User.get_user_by_id({"id": self.user_id})

    @classmethod
    def create_comment(cls, data):
        """Add comment to comment tbl"""
        query = '''INSERT INTO comments (comment, user_id, review_id)
        VALUES (%(comment)s, %(user_id)s, %(review_id)s);'''
        return connectToMySQL(cls.db).query_db(query,data)

# CRUD Read
    @classmethod
    def get_review_comments(cls, data):
        """Get comments based on review id"""
        query = "SELECT * FROM comments WHERE review_id=%(id)s ORDER BY id DESC;"
        results = connectToMySQL(cls.db).query_db(query,data)
        comments = []
        if not results:
            return  comments
        for r in results:
            comments.append(cls(r))
        return comments


