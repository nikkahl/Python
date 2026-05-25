import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from minidb import Database, Column, IntegerType, StringType

class TestIntegrity(unittest.TestCase):

    def setUp(self):
        """Runs before every test to set up a fresh database."""
        self.db = Database("test_db")
        
        self.db.create_table("users", [
            Column("id", IntegerType(), unique=True),
            Column("username", StringType(), nullable=False, unique=True)
        ])
        
        self.db.create_table("posts", [
            Column("id", IntegerType(), unique=True),
            Column("title", StringType(), nullable=False),
            Column("user_id", IntegerType(), references=("users", "id"))
        ])

        self.users = self.db.get_table("users")
        self.posts = self.db.get_table("posts")

    def test_insert_valid_data(self):
        row = self.users.insert({"id": 1, "username": "alice"})
        self.assertEqual(row["username"], "alice")
        self.assertEqual(len(self.users), 1)

    def test_not_null_constraint(self):
        with self.assertRaises(ValueError):
            self.users.insert({"id": 2})

    def test_unique_constraint(self):
        self.users.insert({"id": 1, "username": "alice"})
        with self.assertRaises(ValueError):
            self.users.insert({"id": 2, "username": "alice"})

    def test_type_validation(self):
        with self.assertRaises(TypeError):
            self.users.insert({"id": "one", "username": "bob"})

    def test_foreign_key_constraint(self):
        with self.assertRaises(ValueError):
            self.posts.insert({"id": 1, "title": "Hello", "user_id": 99})

    def test_delete_restrict_policy(self):
        self.users.insert({"id": 1, "username": "alice"})
        self.posts.insert({"id": 101, "title": "My Post", "user_id": 1})
        
        with self.assertRaises(ValueError):
            self.users.delete(1, policy="RESTRICT")

    def test_delete_cascade_policy(self):
        self.users.insert({"id": 1, "username": "alice"})
        self.posts.insert({"id": 101, "title": "My Post", "user_id": 1})
        
        #cascade
        self.users.delete(1, policy="CASCADE")
        self.assertEqual(len(self.posts), 0)

if __name__ == '__main__':
    unittest.main()