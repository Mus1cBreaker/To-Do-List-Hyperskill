# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return "+++ {0}: {1} --- Deadline: {2} +++".format(self.id, self.task, self.deadline)


engine = create_engine("sqlite:///todo.db?check_same_thread=False")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
a = -1
while a != 0:
    print("1) Today's tasks\n"
          "2) Week's tasks\n"
          "3) All tasks\n"
          "4) Missed tasks\n"
          "5) Add task\n"
          "6) Delete task\n"
          "0) Exit")
    a = int(input())
    print()
    if a == 1:
        today_tasks = session.query(Table).filter(Table.deadline == datetime.today()).all()
        print("Today {0} {1}:".format(datetime.today().day, datetime.today().strftime('%b')))
        if today_tasks:
            for task in today_tasks:
                print(task)
        else:
            print("Nothing to do!")
    elif a == 2:
        weekly_tasks = session.query(Table).filter(Table.deadline.between((datetime.today() - timedelta(days=1)), (datetime.today() + timedelta(days=7)))).all()
        sdate = datetime.today()  # start date
        edate = datetime.today() + timedelta(days=6)  # end date

        delta = edate - sdate  # as timedelta
        week = []
        for i in range(delta.days + 1):
            day = sdate + timedelta(days=i)
            week.append(day)
        for date in week:
            print(date.strftime("%A ") + str(date.day) + date.strftime(" %b:"))
            _flag = False
            if weekly_tasks:
                for _e in range(len(weekly_tasks)):
                    if weekly_tasks[_e].deadline == date.date():
                        print(weekly_tasks[_e])
                        _flag = True
            if not _flag:
                print("Nothing to do!")
            print()
    elif a == 3:
        all_tasks = session.query(Table).all()
        print("All tasks:")
        if all_tasks:
            for _e in range(len(all_tasks)):
                print(str((_e + 1)) + ". " + str(all_tasks[_e]))
        else:
            print("Nothing to do!")
    elif a == 4:
        missed_tasks = session.query(Table).filter(Table.deadline < datetime.today()).all()
        print("Missed tasks: ")
        if missed_tasks:
            for _e in range(len(missed_tasks)):
                print(str((_e + 1)) + ". " + str(missed_tasks[_e]))
        else:
            print("Nothing is missed!")
    elif a == 5:
        print("Enter task")
        task_name = input()
        print("Enter deadline")
        _deadline = datetime.strptime(input(), '%Y-%m-%d')
        new_row = Table(task=task_name, deadline=_deadline)
        session.add(new_row)
        session.commit()
        print("The task has been added!")
    elif a == 6:
        all_tasks = session.query(Table).all()
        print("Choose the number of task you want to delete:")
        if all_tasks:
            for _e in range(len(all_tasks)):
                print(str((_e + 1)) + ". " + str(all_tasks[_e]))
        session.delete(all_tasks[(int(input()) - 1)])
        session.commit()
        print("The task has been deleted!")
    print()
