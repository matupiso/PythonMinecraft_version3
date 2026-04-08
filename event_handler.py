from settings import *
import time as t

class Task:
    def __init__(self, task_function, args, time, name):
        self.function = task_function
        self.args = args
        self.time = time
        self.finished = False
        self.name = name
        

    def  update(self, time):
        if round(time, 1) == round(self.time, 1):
            self.function(*self.args)
            self.finished = True


class RTask:
    def __init__(self, task_function, args, time, name):
        self.function = task_function
        self.args = args
        self.time = time
        self.finished = False
        self.name = name
        self.timer = t.time()
        

    def  update(self, time):
        if t.time() - self.timer > self.time:
            self.function(*self.args)
            self.timer = t.time()


class EventHandler:
    def __init__(self, app):
        self.app = app
        self.tasks = []
    

    def add_task(self, name, function, args=[], task_type="n", time_arg=1):
        if task_type == "n": self.tasks.append(Task(function, args, t.time() + time_arg, name))
        elif task_type == "r" :self.tasks.append(RTask(function, args, time_arg, name))


    def del_task(self, task_name):
        self.tasks = list(filter(lambda x: x.name == task_name, self.tasks))

    def update(self):
        time = t.time()
        for i in self.tasks:
            if i.finished:
                continue
            i.update(time)

        
        i = 0
        while i < len(self.tasks):
            if self.tasks[i].finished:
                del self.tasks[i]
            

            i += 1
        

