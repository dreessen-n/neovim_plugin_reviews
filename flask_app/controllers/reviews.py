# Import app
from flask_app import app
# Import modules from flask
from flask_app import Flask, render_template, request, redirect, session, url_for, flash, bcrypt

# Import models class
from flask_app.models import user, review

# CRUD CREATE ROUTES
@app.route('/review/create', methods=['POST'])
def create_new_review():
    # Check that user is logged in
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    # Call staticmethod to validate form
    if not review.Review.validate_form(request.form):
        # Redirect back to new review page
        return redirect('/review/new')
    # Create data dict based on request form
    # the keys must match exactly to the var in the query set
    data = {
        'name': request.form['name'],
        'category': request.form['category'],
        'content': request.form['content'],
        'user_id': session['id']
    }
    review.Review.create_review(data)
    return redirect('/dashboard')

@app.route('/review/like', methods=['POST'])
def add_like_review():
    """Like the review"""
    review.Review.like(request.form)
    return redirect('/dashboard')

@app.route('/review/comment/create', methods=['POST'])
def add_comment_review():
    """Add a comment to the review"""
    review.Review.comment(request.form)
    return redirect(f"/review/show/{request.form['review_id']}")

@app.route('/review/new')
def review_new():
    """Display the form to create a new review"""
    # Check that user is logged in
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    # Create data dict based on user in session
    # the keys must match exactly to the var in the query set
    data = { 'id': session['id'] }
    # Call classmethod in models
    return render_template('new.html', user=user.User.get_user_by_id(data))

# CRUD READ ROUTES
@app.route('/dashboard')
def dashboard():
    """Welcome page"""
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    # Create data set to query user based on id to get name to display
    data = {
        'id': session['id']
    }
    # Pass the data dict to create_user method in class
    one_user = user.User.get_user_by_id(data)
    if one_user:
        session['email'] = one_user.email
        session['first_name'] = one_user.first_name
        session['last_name'] = one_user.last_name
    # Add all_reviews to the dashboard
    all_reviews = review.Review.get_all_reviews()
    print(all_reviews)
    return render_template('dashboard.html', one_user=one_user, all_reviews=all_reviews)

@app.route('/review/show/<int:review_id>')
def review_show_one(review_id):
    """Show the review on a page"""
    # Check that user is logged in
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    # Create data dict based on review_id
    # The keys must match exactly to the var in the query set
    data = { 'id': review_id }
    # Create additonal data dict for user
    data_user = { 'id': session['id'] }
    # Call classmethods and render_template edit template with data filled in
    return render_template('show.html', one_review=review.Review.get_one_review(data), user=user.User.get_user_by_id(data_user))

@app.route('/review/comment/<int:review_id>/<int:user_id>')
def review_show_comment(review_id, user_id):
    """Add comment to review based on user_id and review_id"""
    # Check that user logged in
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    return render_template('comment.html', review_id=review_id, user_id=user_id)


# CRUD UPDATE ROUTES
# Show review to edit with populated info
@app.route('/review/edit/<int:review_id>')
def edit_review(review_id):
    """Edit the review"""
    # Check that user is logged in
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    # Create data dict based on review_id
    # The keys must match exactly to the var in the query set
    data = { 'id': review_id }
    # Create additonal data dict for user
    data_user = { 'id': session['id'] }
    # Call classmethods and render_template edit template with data filled in
    return render_template('edit.html', one_review=review.Review.get_one_review(data), user=user.User.get_user_by_id(data_user))

# Update the review
@app.route('/review/update', methods=['POST'])
def update_review():
    """Update review after editing"""
    # Check that user is logged in
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    # Call staticmethod to validate form
    if not review.Review.validate_form(request.form):
        # Redirect back to new review page
        id = int(request.form['id'])
        return redirect(f'/review/edit/{id}')
    # Create data dict based on review_id
    # The keys must match exactly to the var in the query set
    data = {
        'id': request .form['id'],
        'name': request.form['name'],
        'category': request.form['category'],
        'content': request.form['content'],
    }
    # Call classmethod in models
    review.Review.update_review(data)
    id = request.form['id']
    # Give message that update was successful
    flash("Edit was successful", "success")
    # Redirect to dashboard after update
    return redirect(f'/review/edit/{id}')

# CRUD DELETE ROUTES
@app.route('/review/delete/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    """Delete review if session user created"""
    # Check that user is logged in
    if 'id' not in session:
        flash("Please register or login to continue", "danger")
        return redirect('/')
    # Create data dict based on review_id
    # The keys must match exactly to the var in the query set
    data = { 'id': review_id }
    # Call classmethod in models
    review.Review.delete_review(data)
    # Redirect back to dashboard after deletion
    return redirect('/dashboard')

@app.route('/review/unlike', methods=['POST'])
def un_like_review():
    review.Review.unlike(request.form)
    return redirect('/dashboard')

