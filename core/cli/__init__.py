import os
import json
import click
import shutil
import pathlib
from flask import current_app
from flask.cli import with_appcontext
import mysql.connector
from datetime import datetime

from core.config import (
    DATABASE_NAME,
    DATABASE_HOST,
    DATABASE_PASSWORD,
    DATABASE_USER
)

db = mysql.connector.connect(
    host=DATABASE_HOST,
    user=DATABASE_USER,
    passwd=DATABASE_PASSWORD
)

mysql_cursor = db.cursor()


@click.command('delete-db')
@with_appcontext
def reset():
    app_pyc = current_app.config['APPLICATION_ROOT'] + '/app.pyc'
    migration_folder = current_app.config['APPLICATION_ROOT'] + '/migrations'
    pycache = current_app.config['APPLICATION_ROOT'] + '/__pycache__'

    app_pyc_file = pathlib.Path(app_pyc)
    migration_folder_path = pathlib.Path(migration_folder)
    pycache_path = pathlib.Path(pycache)

    if app_pyc_file.is_file():
        app_pyc_file.unlink()
    if migration_folder_path.is_dir():
        shutil.rmtree(migration_folder_path)
    if pycache_path.is_dir():
        shutil.rmtree(pycache_path)

    try:
        mysql_cursor.execute("DROP DATABASE {}".format(DATABASE_NAME))
        click.echo('Database {} has been deleted..!!!'.format(DATABASE_NAME))
    except:
        click.echo('Database "{}" is not exist, so "delete action" is not running'.format(DATABASE_NAME))


@click.command('new')
@with_appcontext
def new_command():
    os.system("flask delete-db")
    mysql_cursor.execute("CREATE DATABASE {}".format(DATABASE_NAME))
    os.system("flask db init")
    os.system("flask db migrate")
    os.system("flask db upgrade")
    os.system("flask add-seek")
    click.echo("Done.!! :), DATABASE_NAME : {}".format(DATABASE_NAME))


@click.command('add-seek')
@with_appcontext
def add_seek():
    from apps.user.models import User, UserDetail
    # from apps.category_access.models import CategoryAccess
    seek_data = open('seek_data.json')
    seek_data = json.load(seek_data)

    for user in seek_data['users']:
        # ca = CategoryAccess(
        #     name=user['ca']['name'],
        #     root_access=user['ca']['root_access'],
        #     add_user=user['ca']['add_user'],
        #     delete_user=user['ca']['delete_user'],
        #     edit_user=user['ca']['edit_user'],
        #     add_job=user['ca']['add_job'],
        #     delete_job=user['ca']['delete_job'],
        #     update_job=user['ca']['update_job'],
        #     show_job=user['ca']['show_job'],
        #     show_user=user['ca']['show_user'],
        #     print_job=user['ca']['print_job'],
        #     check_job=user['ca']['check_job'],
        #     service_job=user['ca']['service_job']
        # )
        detail = UserDetail(
            fullname=user['fullname'],
            address=user['address'],
            phone_number=user['phone_number'],
            work_start_time=datetime.strptime(user['work_start_time'], "%d-%m-%Y").date(),
            activate=user['activate']
        )

        user = User(
            username=user['username'],
            email=user['email'],
            password=user['password'],
            user_detail=detail
        )
        user.commit()
        # ca.users.append(user)
        # ca.commit()
        click.echo("Add Data Done.!! :)")


@click.command('test')
@with_appcontext
def testing():
    from os import system
    system("coverage run -m pytest -vs")


class CLI:
    @staticmethod
    def init_app(app):
        app.cli.add_command(reset)
        app.cli.add_command(add_seek)
        app.cli.add_command(new_command)
        app.cli.add_command(testing)
