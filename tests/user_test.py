"""Test file for user"""
import logging
import os
# from faker import Faker
from app import db
from app import config
from app.db.models import User, Song


def test_adding_user(application):
    """test for adding user """
    log = logging.getLogger("myApp")
    with application.app_context():
        assert db.session.query(User).count() == 0
        assert db.session.query(Song).count() == 0
        # showing how to add a record
        # create a record
        user = User('dsouza.rohit.94@gmail.com', 'testtest')
        # add it to get ready to be committed
        db.session.add(user)
        # call the commit
        # db.session.commit()
        # assert that we now have a new user
        # assert db.session.query(User).count() == 1
        # finding one user record by email
        user = User.query.filter_by(email='dsouza.rohit.94@gmail.com').first()
        log.info(user)
        # asserting that the user retrieved is correct
        assert user.email == 'dsouza.rohit.94@gmail.com'
        # this is how you get a related record ready for insert
        user.songs = [Song("test", "smap"), Song("test2", "te")]
        # commit is what saves the songs
        db.session.commit()
        assert db.session.query(Song).count() == 2
        song1 = Song.query.filter_by(title='test').first()
        assert song1.title == "test"
        # changing the title of the song
        song1.title = "SuperSongTitle"
        # saving the new title of the song
        db.session.commit()
        song2 = Song.query.filter_by(title='SuperSongTitle').first()
        assert song2.title == "SuperSongTitle"
        # checking cascade delete
        db.session.delete(user)
        assert db.session.query(User).count() == 0
        assert db.session.query(Song).count() == 0


def test_uploading_files(application, add_user):  # pylint: disable =unused-argument
    """test for uploading files"""
    log = logging.getLogger("myApp") # pylint: disable =unused-variable
    with application.app_context():
        assert db.session.query(User).count() == 1
        assert db.session.query(Song).count() == 0

    filecsv = 'music.csv'
    flupload = config.Config.UPLOAD_FOLDER
    upload_file = os.path.join(flupload, filecsv)
    assert os.path.exists(upload_file) is True

    with application.test_client() as client:
        with open(upload_file, 'rb') as file:
            data = {
                'file': (file, filecsv),

            }
            resp = client.post('songs/upload', data=data, follow_redirects=True)

    assert resp.status_code == 400


def user_dashboard_access_approved(client):
    """Test for dashboard access"""
    response = client.get("/dashboard")
    assert response.status_code == 200
    return client.get('/dashboard', follow_redirects=True)


def user_dashboard_access_deny(client):
    """test for access deny"""
    response = client.get("/dashboard")
    assert response.status_code == 403
    return client.get('/dashboard', follow_redirects=False)


def test_upload_csvfile_access_denied(client):
    """test for csv upload"""
    response = client.get("/upload", follow_redirects=False)
    assert response.status_code == 404
