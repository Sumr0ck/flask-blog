from app import db
from datetime import datetime
import re


post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

def slugify(s):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', s).lower()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now)
    tags = db.relationship(
        'Tag',
        secondary=post_tags,
        backref=db.backref('posts', lazy='dynamic')   
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self) -> str:
        return f'<Post id: {self.id}, title: {self.title}>'


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    slug = db.Column(db.String(100))

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self) -> str:
        return f'<Tag id: {self.id}, name: {self.name}>'
