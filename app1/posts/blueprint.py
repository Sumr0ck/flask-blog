from flask import Blueprint, flash, render_template, redirect, request, url_for
from flask_login import current_user
from flask_security import login_required

from models import Post, Tag, Role
from .forms import PostForm, RegistrationForm
from app import db, user_datastore


posts = Blueprint('posts', __name__, template_folder='templates')

@posts.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = user_datastore.create_user(email=form.email.data, password=form.password.data)
        role_user = Role.query.filter(Role.name=='user').first_or_404()
        user_datastore.add_role_to_user(user, role_user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('security.login', next=request.url))
    return render_template('posts/register.html', form=form)


@posts.route('/create', methods=['POST', 'GET'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        try:
            post = Post(title=title, body=body)
            db.session.add(post)
            db.session.commit()
        except:
            print('Something wrong')
        return redirect(url_for('.index'))
    form = PostForm()
    return render_template('posts/create_post.html', form=form)


@posts.route('/<slug>/edit/', methods=['POST', 'GET'])
@login_required
def edit_post(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    if request.method == 'POST':
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()
        return redirect(url_for('posts.post_detail', slug=post.slug))
    form = PostForm(obj=post)
    return render_template('posts/edit_post.html', post=post, form=form)


@posts.route('/')
def index():
    q = request.args.get('q')
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    if q:
        posts = Post.query.filter(Post.title.ilike(
            '%' + q + '%') | Post.body.ilike('%' + q + '%'))  # .all()
    else:
        posts = Post.query.order_by(Post.created.desc())
    pages = posts.paginate(page=page, per_page=10)
    return render_template('posts/index.html', pages=pages)


@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    return render_template('posts/post-detail.html', post=post)


@posts.route('/tag/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    posts = tag.posts.all()
    return render_template('posts/tag_detail.html', posts=posts, tag=tag)
