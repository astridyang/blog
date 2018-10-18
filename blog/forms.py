from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, ValidationError
from wtforms.validators import DataRequired, Length
from flask_ckeditor import CKEditorField
from blog.models import Category, BookCategory, LinkCategory


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 60)])
    category = SelectField('Category', coerce=int, default=1)
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]


class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField()

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('Name already in use')


class SettingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 70)])
    blog_title = StringField('Blog Title', validators=[DataRequired(), Length(1, 60)])
    blog_sub_title = StringField('Blog sub title', validators=[DataRequired(), Length(1, 100)])
    about = CKEditorField('About page', validators=[DataRequired()])
    submit = SubmitField()


class BookForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 100)])
    category = SelectField('Category',  coerce=int, default=1)
    comment = CKEditorField('Comment')
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in BookCategory.query.order_by(BookCategory.name).all()]


class BookCategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 60)])
    submit = SubmitField()

    def validate_name(self, field):
        if BookCategory.query.filter_by(name=field.data).first():
            raise ValidationError('Name already in use')


class LinkForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 60)])
    url = StringField('Url', validators=[DataRequired(), Length(1, 100)])
    category = SelectField('Category', coerce=int, default=1)
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(LinkForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in LinkCategory.query.order_by(LinkCategory.name).all()]


class LinkCategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 60)])
    submit = SubmitField()

    def validate_name(self, field):
        if LinkCategory.query.filter_by(name=field.data).first():
            raise ValidationError('Name already in use')




