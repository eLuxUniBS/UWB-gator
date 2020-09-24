import asyncio
from srv.broker.srv import main
from orm import orm
db_name="test_drive"
db_table="test_table"
db_obj=orm.DB(db_name=db_name, db_table=db_table)
db_obj.create_db()
asyncio.run(main(db_obj))