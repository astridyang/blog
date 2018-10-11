import click
from blog import app, db
from blog.models import Admin

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
def init(username, password):
    """Building Bluelog, just for you."""

    click.echo('Initializing the database...')
    db.create_all()

    admin = Admin.query.first()
    if admin is not None:
        click.echo('The administrator already exists, updating...')
        admin.username = username
        admin.set_password(password)
    else:
        click.echo('Creating the temporary administrator account...')
        admin = Admin(
            username=username,
            name='Admin',
        )
        admin.set_password(password)
        db.session.add(admin)
    db.session.commit()
    click.echo('Done.')