import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from minidb import Database, Column, IntegerType, StringType, COUNT, TransactionError

def main():
    print("--- 1. Initializing Database ---")
    db = Database("company_db")

    db.create_table("departments", [
        Column("id", IntegerType(), unique=True),
        Column("name", StringType(), nullable=False)
    ])

    db.create_table("employees", [
        Column("id", IntegerType(), unique=True),
        Column("name", StringType(), nullable=False),
        Column("dept_id", IntegerType(), references=("departments", "id"))
    ])

    depts = db.get_table("departments")
    emps = db.get_table("employees")

    print("--- 2. Inserting Base Data ---")
    depts.insert({"id": 1, "name": "Engineering"})
    depts.insert({"id": 2, "name": "Marketing"})

    emps.insert({"id": 101, "name": "Alice", "dept_id": 1})
    emps.insert({"id": 102, "name": "Bob", "dept_id": 1})
    emps.insert({"id": 103, "name": "Charlie", "dept_id": 2})

    print("\n--- 3. Testing Aggregation ---")
    agg_results = emps.query().select(["dept_id", COUNT("id")]).group_by("dept_id").execute()
    for row in agg_results:
        print(f"Dept {row['dept_id']} has {row['COUNT(id)']} employees.")

    print("\n--- 4. Testing Transactions ---")
    try:
        with db.transaction():
            print("Starting transaction")
            depts.insert({"id": 3, "name": "HR"})
            print("HR Dept inserted.")
            
            print("Attempting to insert employee with invalid dept_id")
            emps.insert({"id": 104, "name": "David", "dept_id": 99})
            
    except TransactionError as e:
        print(f"Transaction Error Caught: {e}")
        print("Database rolled back successfully!")

    hr_exists = depts.query().where("name", "=", "HR").execute()
    print(f"Does HR department exist after rollback? {'Yes' if hr_exists else 'No'}")

    print("\n--- 5. Testing JSON Serialization ---")
    backup_file = "backup.json"
    db.save_to_json(backup_file)
    print(f"Database saved to {backup_file}.")

    new_db = Database("restored_db")
    new_db.load_from_json(backup_file)
    
    restored_emps = new_db.get_table("employees")
    print(f"Loaded {len(restored_emps)} employees from JSON backup.")

    # if os.path.exists(backup_file):
    #     os.remove(backup_file)
        
if __name__ == "__main__":
    main()