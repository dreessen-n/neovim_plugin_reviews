# Import app
from flask_app import app
# Import modules from flask
from flask_app import Flask, render_template, request, redirect, session, url_for, flash, bcrypt

# Import models class
from flask_app.models import user, review, comment

# CRUD Create Routes
@app.route('/comment/create', methods=['POST'])
def add_comment_review():
    """Add a comment to the review"""
    comment.Comment.create_comment(request.form)
    return redirect(f"/review/show/{request.form['review_id']}")

# CRUD Read Routes
@app.route('/comment/<int:review_id>/<int:user_id>')
def review_show_comment(review_id, user_id):
    """Add comment to review based on user_id and review_id"""
    # Check that user logged in
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    return render_template('comment.html', review_id=review_id, user_id=user_id)

# CRUD Delete Routes
