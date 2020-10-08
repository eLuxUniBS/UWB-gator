import asyncio
from srv.subs.srv import main
from orm import orm
db_name="test_loc"
db_table="test_loc_table"
db_obj=orm.DB(db_name=db_name, db_table=db_table)
db_obj.create_db()
asyncio.run(main(db_obj))