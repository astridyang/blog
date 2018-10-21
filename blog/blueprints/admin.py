from flask import Blueprint, flash, redirect, url_for, render_template, request, current_app
from flask_login import login_required, current_user
from ..forms import PostForm, CategoryForm, SettingForm, BookForm, BookCategoryForm, LinkForm, LinkCategoryForm
from ..models import Post, Category, Book, BookCategory, Link, LinkCategory
from ..extensions import db
from ..utils import redirect_back


admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        category = Category.query.get(form.category.data)
        body = form.body.data
        post = Post(title=title, category=category, body=body)
        db.session.add(post)
        db.session.commit()
        flash('Post created.', 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    return render_template('admin/new_post.html', form=form)


@admin_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.category = Category.query.get(form.category.data)
        db.session.commit()
        flash('Post updated.', 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    form.category.data = post.category_id
    return render_template('admin/edit_post.html', form=form)


@admin_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.', 'success')
    return redirect_back()


@admin_bp.route('/post/manage')
@login_required
def manage_post():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_MANAGE_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=per_page)
    posts = pagination.items
    return render_template('admin/manage_post.html', posts=posts, pagination=pagination, page=page)


@admin_bp.route('/category/new', methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash('Category created.', 'success')
        return redirect(url_for('.manage_category'))
    return render_template('admin/new_category.html', form=form)


@admin_bp.route('/category/manage')
@login_required
def manage_category():
    return render_template('admin/manage_category.html')


@admin_bp.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    form = CategoryForm()
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('You can not edit the default category.', 'warning')
        return redirect(url_for('blog.index'))
    if form.validate_on_submit():
        category.name = form.category.name
        db.session.commit()
        flash('Category updated.', 'success')
        return redirect(url_for('.manage_category'))
    form.name.data = category.name
    return render_template('admin/edit_category.html', form=form)


@admin_bp.route('/category/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('You can not delete the default category.', 'warning')
        return redirect(url_for('blog.index'))
    category.delete()
    flash('Category deleted.', 'success')
    return redirect(url_for('.manage_category'))


@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.blog_title = form.blog_title.data
        current_user.blog_sub_title = form.blog_sub_title.data
        current_user.about = form.about.data
        db.session.commit()
        flash('Setting updated.', 'success')
        return redirect(url_for('blog.index'))
    form.name.data = current_user.name
    form.blog_title.data = current_user.blog_title
    form.blog_sub_title.data = current_user.blog_sub_title
    form.about.data = current_user.about
    return render_template('admin/settings.html', form=form)


@admin_bp.route('/book/new', methods=['GET', 'POST'])
@login_required
def new_book():
    form = BookForm()
    if form.validate_on_submit():
        name = form.name.data
        category = BookCategory.query.get(form.category.data)
        comment = form.comment.data
        book = Book(name=name, category=category, comment=comment)
        db.session.add(book)
        db.session.commit()
        flash("Book created.", 'success')
        return redirect(url_for('book.show_book', book_id=book.id))
    return render_template('admin/new_book.html', form=form)


@admin_bp.route('/book/<int:book_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    form = BookForm()
    book = Book.query.get_or_404(book_id)
    if form.validate_on_submit():
        book.name = form.name.data
        book.category = BookCategory.query.get(form.category.data)
        book.comment = form.comment.data
        db.session.commit()
        flash('Book updated.', 'success')
        return redirect(url_for('book.show_book', book_id=book.id))
    form.name.data = book.name
    form.category.data = book.category_id
    form.comment.data = book.comment
    return render_template('admin/edit_book.html', form=form)


@admin_bp.route('/book/<int:book_id>/delete', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted.', 'success')
    return redirect_back()


@admin_bp.route('/book/manage')
@login_required
def manage_book():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_MANAGE_POST_PER_PAGE']
    pagination = Book.query.order_by(Book.timestamp.desc()).paginate(page, per_page=per_page)
    books = pagination.items
    return render_template('admin/manage_book.html', books=books, pagination=pagination, page=page)


@admin_bp.route('/book_category/new', methods=['GET', 'POST'])
@login_required
def new_book_category():
    form = BookCategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        category = BookCategory(name=name)
        db.session.add(category)
        db.session.commit()
        flash("Book category created.", "success")
        return redirect(url_for('.manage_book_category'))
    return render_template('admin/new_category.html', form=form, title="book")


@admin_bp.route('/book_category/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_book_category(category_id):
    form = BookCategoryForm()
    category = BookCategory.query.get_or_404(category_id)
    if category.id == 1:
        flash('You can not edit the default category.', 'warning')
        return redirect(url_for('book.index'))
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash('Book category updated.', 'success')
        return redirect(url_for('.manage_book_category'))
    form.name.data = category.name
    return render_template('admin/edit_category.html', form=form)


@admin_bp.route('/book_category/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_book_category(category_id):
    category = BookCategory.query.get_or_404(category_id)
    if category.id == 1:
        flash('You can not delete the default category.', 'warning')
        return redirect(url_for('book.index'))
    category.delete()
    flash('Category deleted.', 'success')
    return redirect(url_for('.manage_book_category'))


@admin_bp.route('/book_category/manage')
@login_required
def manage_book_category():
    return render_template('admin/manage_book_category.html')


@admin_bp.route('/link/new', methods=['GET', 'POST'])
@login_required
def new_link():
    form = LinkForm()
    if form.validate_on_submit():
        title = form.title.data
        url = form.url.data
        category = LinkCategory.query.get(form.category.data)
        link = Link(title=title, url=url, category=category)
        db.session.add(link)
        db.session.commit()
        flash('New link created.', 'success')
        return redirect(url_for('.manage_link'))
    return render_template('admin/new_link.html', form=form)


@admin_bp.route('/link/<int:link_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_link(link_id):
    form = LinkForm()
    link = Link.query.get_or_404(link_id)
    if form.validate_on_submit():
        link.title = form.title.data
        link.url = form.url.data
        link.category = LinkCategory.query.get(form.category.data)
        db.session.commit()
        flash('Link updated.', 'success')
        return redirect(url_for('.manage_link'))
    form.title.data = link.title
    form.url.data = link.url
    form.category.data = link.category_id
    return render_template('admin/new_link.html', form=form)


@admin_bp.route('/link/<int:link_id>/delete', methods=['POST'])
@login_required
def delete_link(link_id):
    link = Link.query.get_or_404(link_id)
    db.session.delete(link)
    db.session.commit()
    flash('Link deleted.', 'success')
    return redirect_back()


@admin_bp.route('/link/manage')
@login_required
def manage_link():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_MANAGE_POST_PER_PAGE']
    pagination = Link.query.order_by(Link.timestamp.desc()).paginate(page, per_page=per_page)
    links = pagination.items
    return render_template('admin/manage_link.html', links=links, pagination=pagination, page=page)


@admin_bp.route('/link_category/new', methods=['GET', 'POST'])
@login_required
def new_link_category():
    form = LinkCategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        category = LinkCategory(name=name)
        db.session.add(category)
        db.session.commit()
        flash("Link category created.", "success")
        return redirect(url_for('.manage_link_category'))
    return render_template('admin/new_category.html', form=form, title='link')


@admin_bp.route('/link_category/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_link_category(category_id):
    form = LinkCategoryForm()
    category = LinkCategory.query.get_or_404(category_id)
    if category.id == 1:
        flash('You can not edit the default category.', 'warning')
        return redirect(url_for('blog.index'))
    if form.validate_on_submit():
        category.name = form.category.name
        db.session.commit()
        flash('Category updated.', 'success')
        return redirect(url_for('.manage_link_category'))
    form.name.data = category.name
    return render_template('admin/edit_category.html', form=form)


@admin_bp.route('/link_category/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_link_category(category_id):
    category = LinkCategory.query.get_or_404(category_id)
    if category.id == 1:
        flash('You can not delete the default category.', 'warning')
        return redirect(url_for('book.index'))
    category.delete()
    flash('Category deleted.', 'success')
    return redirect(url_for('.manage_link_category'))


@admin_bp.route('/link_category/manage')
@login_required
def manage_link_category():
    return render_template('admin/manage_link_category.html')




