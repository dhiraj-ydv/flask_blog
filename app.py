from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

def create_test_data():
    db.create_all()
    if BlogPost.query.count() == 0:  # Add test data only if the table is empty
        post1 = BlogPost(title="First Post", content="Content of the first post")
        post2 = BlogPost(title="Second Post", content="Content of the second post")
        db.session.add(post1)
        db.session.add(post2)
        db.session.commit()
    # Print out the IDs of the posts for debugging
    posts = BlogPost.query.all()
    for post in posts:
        print(f"Post ID: {post.id}, Title: {post.title}")

@app.route('/')
def index():
    posts = BlogPost.query.all()
    for post in posts:
        print(f"Index Page - Post ID: {post.id}, Title: {post.title}")  # Debug print
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = BlogPost(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_post.html')

@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    print(f"View Post - Post ID: {post.id}, Title: {post.title}")  # Debug print
    return render_template('post.html', post=post, post_id=post_id)

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('view_post', post_id=post_id))
    return render_template('edit_post.html', post=post)

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        create_test_data()  # Create database tables and add test data
    app.run(debug=True, use_reloader=False)
