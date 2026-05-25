import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from minidb import Database, Column, IntegerType, StringType, FloatType, COUNT, SUM, AVG
from minidb.query.engine import JoinedTable, Query

class TestQueryEngine(unittest.TestCase):

    def setUp(self):
        self.db = Database("store_db")
        
        self.db.create_table("categories", [
            Column("id", IntegerType(), unique=True),
            Column("name", StringType())
        ])
        
        self.db.create_table("products", [
            Column("id", IntegerType(), unique=True),
            Column("name", StringType()),
            Column("price", FloatType()),
            Column("cat_id", IntegerType(), references=("categories", "id"))
        ])

        self.cats = self.db.get_table("categories")
        self.prods = self.db.get_table("products")

        self.cats.insert({"id": 1, "name": "Electronics"})
        self.cats.insert({"id": 2, "name": "Clothing"})

        self.prods.insert({"id": 1, "name": "Laptop", "price": 1000.0, "cat_id": 1})
        self.prods.insert({"id": 2, "name": "Mouse", "price": 50.0, "cat_id": 1})
        self.prods.insert({"id": 3, "name": "T-Shirt", "price": 20.0, "cat_id": 2})
        self.prods.insert({"id": 4, "name": "Keyboard", "price": 80.0, "cat_id": 1})

        self.db.save_to_json("test_query_state.json")

    def test_simple_select_and_where(self):
        result = self.prods.query().where("price", ">", 60.0).execute()
        self.assertEqual(len(result), 2)
        
        names = [r["name"] for r in result]
        self.assertIn("Laptop", names)
        self.assertIn("Keyboard", names)

    def test_chained_where_and_like(self):
        result = self.prods.query()\
            .where("cat_id", "=", 1)\
            .where("name", "LIKE", "%board")\
            .execute()
            
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Keyboard")

    def test_order_by_and_limit(self):
        result = self.prods.query().order_by("price", ascending=False).limit(2).execute()
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "Laptop")
        self.assertEqual(result[1]["name"], "Keyboard")

    def test_group_by_and_aggregations(self):
        result = self.prods.query()\
            .select(["cat_id", COUNT("id"), AVG("price")])\
            .group_by("cat_id")\
            .execute()

        self.assertEqual(len(result), 2)
        
        cat_1_data = next(r for r in result if r["cat_id"] == 1)
        self.assertEqual(cat_1_data["COUNT(id)"], 3)
        self.assertAlmostEqual(cat_1_data["AVG(price)"], 376.666, places=2)

    def test_inner_join(self):
        joined = JoinedTable(self.cats, self.prods, "id", "cat_id")
        
        result = Query(joined).where("products.price", "<", 100.0).execute()
        
        self.assertEqual(len(result), 3) 
        
        first_row = result[0]
        self.assertIn("categories.name", first_row)
        self.assertIn("products.price", first_row)

if __name__ == '__main__':
    unittest.main()