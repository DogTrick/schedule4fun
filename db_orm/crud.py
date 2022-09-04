from sqlalchemy import or_, and_
from db_connect import session_scope
from tables import *

# CRUD for Account
def get_account(user_name, password):
    with session_scope() as session:
        account = session.query(Account).filter(and_(Account.user_name == user_name, Account.password == password)).first()
        if account:
            return account
        
def insert_account(user_name, password):
    with session_scope() as session:
        account = Account(user_name = user_name, password = password)        
        session.add(account)
        
# CRUD for Schedule
def insert_schedule(user_name, title, content):
    with session_scope() as session:
        user_id = session.query(Account).filter(Account.user_name == user_name).first().id
        schedule = Schedule(user_id = user_id, user_name = user_name, title = title, content = content)        
        session.add(schedule)
        
def get_schedule(schedule_id):
    with session_scope() as session:
        schedule = session.query(Schedule).filter(Schedule.id == schedule_id).first()
        return schedule
        
def get_all_schedule():
    with session_scope() as session:
        schedules = session.query(Schedule).all()
        return schedules

def delete_schedule(schedule_id):
    with session_scope() as session:
        schedule = session.query(Schedule).filter(Schedule.id == schedule_id).first()        
        if schedule:
            session.delete(schedule)
                                          