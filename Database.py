__author__ = 'Joe Munoz'

import sqlite3
from MessageObject import Message


class Deployment():
    def deploy(self):
        try:
            db = sqlite3.connect(':memory:')

            cursor = db.cursor()

            cursor.execute('''
            CREATE TABLE messages(id INTEGER PRIMARY KEY, sender TEXT,
                           application TEXT unique, message TEXT, creation_time TEXT)
            ''')
            db.commit()
        except Exception as e:
            db.rollback()
        finally:
            db.close()


    def drop(self):
        try:
            # Get a cursor object
            db = sqlite3.connect(':memory:')
            cursor = db.cursor()
            cursor.execute('''DROP TABLE users''')
            db.commit()
        except Exception as e:
            db.rollback()
        finally:
            db.close()


class MessageOperations():
    def insert(self, Message):
        try:
            db = sqlite3.connect(':memory:')
            cursor = db.cursor()

            cursor.execute(
                '''INSERT INTO users(sender, application, message, creation_time)
                    VALUES(?, ?, ?, ?)''', (Message.sender, Message.application, Message.message, Message.creation_time)
            )

            db.commit()
        except Exception as e:
            db.rollback()
        finally:
            db.close()


    def remove_by_id(self, id):
        try:
            db = sqlite3.connect(':memory:')
            cursor = db.cursor()

            cursor.execute('''DELETE FROM messages WHERE id = ? ''', (id))
            db.commit()
        except Exception as e:
            db.rollback()
        finally:
            db.close()


    def get_first(self):
        db = sqlite3.connect(':memory:')
        cursor = db.cursor()

        cursor.execute(
            '''SELECT id, sender, application, message, creation_time FROM messages ORDER BY id ASC LIMIT 1'''
        )


    def last_row_id(self):
        db = sqlite3.connect(':memory:')
        cursor = db.cursor()

        return cursor.lastrowid


    def get_by_id(self, id):
        db = sqlite3.connect(':memory:')
        cursor = db.cursor()

        cursor.execute(
            '''SELECT name, email, phone FROM users WHERE id=?''', id
        )

