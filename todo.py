from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date, String
from sqlalchemy.orm import sessionmaker
from datetime import datetime , timedelta

# creating of the database file with the file name.

engine = create_engine("sqlite:///todo.db?check_same_thread=False")

# class for creating table into  database

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column("id", Integer, primary_key=True)
    string_field = Column("task", String, default='default_value')
    date_field = Column("deadline", Date, default=datetime.today())

    def __repr__(self):
        return self.string_field


# creating table in our database

Base.metadata.create_all(engine)

# creating session for accessing and storing data

Session = sessionmaker(bind=engine)
session = Session()


# # adding of the row in the table in database


def Add_task(string, date_):
    # adding of the row in the table in database

    new_row = Table(string_field=string, date_field=datetime.strptime(date_, '%Y-%m-%d'))
    session.add(new_row)
    session.commit()


def tasks(time):
    # retrieving of the rows from the table
    # return list of the information
    # rows = session.query(Table).all()
    today = datetime.today().strftime("%Y-%m-%d")
    rows = session.query(Table).filter(Table.date_field == today).all()

    return rows


def all_tasks():
    '''function for printing all the tasks'''
    rows = session.query(Table).all()

    return rows


def weeks_task():
    '''function for generating tasks for whole week'''
    today = datetime.today()

    for x in range(7):
        day_ = today.strftime("%A")
        today2 = today.strftime("%Y-%m-%d")
        month = today.strftime("%b")

        rows = session.query(Table).filter(Table.date_field == today2).all()

        print(f"{day_} {today.day} {month}:")
        if rows == []:
            print("Nothing to do!")
        else:
            order = 1
            for x in rows:
                print(f"{order}. {x}")
                order += 1
        print()
        today += timedelta(days=1)


def delete():
    '''function for deleting qeuries'''
    rows = session.query(Table).all()

    print("Chose the number of the task you want to delete:")
    order = 1
    for x in rows:
        date = x.date_field
        date1 = date.day
        month = date.strftime("%b")
        print(f"{order}. {x.string_field}. {date1} {month} ")
        order += 1

    num = int(input())

    session.delete(rows[num - 1])

    session.commit()

    print("The task has been deleted!\n")


def missed():
    '''funtion for missing tasks'''
    today = datetime.today()
    t1 = today.strftime("%Y-%m-%d")
    rows = session.query(Table).filter(Table.date_field < datetime.today()).all()
    order = 1
    if rows == []:
        print("Nothing is missed!\n")
    else:
        for x in rows:
            date = x.date_field
            date1 = date.day
            month = date.strftime("%b")
            print(f"{order}. {x.string_field}. {date1} {month} ")
            order += 1
    print()


if __name__ == "__main__":

    flag = True

    my_dict = {}

    while flag:

        print('''1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit''')

        schedule = int(input())

        # checking for the tasks in the database table
        if schedule == 1:

            today = datetime.now()
            task = tasks(today)
            day = today.day
            month = today.strftime("%b")
            print(f"\nToday {day} {month}")
            if task == []:
                print("Nothing to do!\n")

            else:
                o_r = 1
                for x in task:
                    date = x.date_field

                    date1 = date.day

                    month = date.strftime("%b")

                    print(o_r, x.string_field)
                    o_r += 1

            print()

        # inserting of the task in the database table

        elif schedule == 0:
            flag = False
            print()

        elif schedule == 5:
            task_ = input("\nEnter task\n")
            deadline = input("Enter deadline\n")
            Add_task(task_, deadline)
            print('The task has been added!')
            print()

        elif schedule == 3:
            t_all = all_tasks()
            order = 1
            print("\nAll tasks:")
            for x in t_all:
                date = x.date_field
                date1 = date.day
                month = date.strftime("%b")
                print(f"{order}. {x.string_field}. {date1} {month} ")
                order += 1

            print()

        elif schedule == 2:
            print()
            weeks_task()

        elif schedule == 6:
            print()
            delete()

        elif schedule == 4:
            print()
            print("Missed tasks:")
            missed()

    print("Bye!")
