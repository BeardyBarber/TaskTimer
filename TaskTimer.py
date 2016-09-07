#!/usr/bin/env python3.5
import os
import ast
import glob
import time
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from _datetime import timedelta


class RootWidget(BoxLayout):

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

    def add_task(self, labelText, isRepeatable):
        try:
            if labelText == '':
                raise ValueError('Cannot create task from empty String!')
        except ValueError as e:
            print(e)
        else:
            task = TaskTimerWidget(labelText, isRepeatable)
            self.add_widget(task)
            self.ids.new_task.text = ''
            self.ids.repeatable.active = False

    def stop_all(self):
        for child in self.children:
            if(type(child) == TaskTimerWidget):
                Clock.unschedule(child.update)

    def pickle_all(self):
        file = open(os.path.join(
            os.path.dirname(__file__), time.strftime('%d_%m_%Y') + '.txt'), 'w')
        data = []
        for child in self.children:
            if(type(child) == TaskTimerWidget):
                data.append(str(child))
        json.dump(data, file, indent=4, separators=(',', ': '))
        file.close()


class TaskTimerWidget(BoxLayout):
    seconds = NumericProperty(0)
    label = StringProperty('')
    isRepeatableFlag = BooleanProperty(False)
    isDoneFlag = BooleanProperty(False)

    def update(self, dt):
        self.seconds += dt

    def stop(self):
        Clock.unschedule(self.update)
        self.isDoneFlag = True
        print(self)

    def start(self):
        Clock.schedule_interval(self.update, .016)
        print(self)

    @staticmethod
    def format(sec):
        m, s = divmod(sec, 60)
        h, m = divmod(m, 60)
        return "%02d:%02d:%02d" % (h, m, s)

    def __str__(self):
        return str({"time": self.seconds, "label": self.label, "isRepeatable": self.isRepeatableFlag, "isDone": self.isDoneFlag})

    def __init__(self, labelText, isRepeatable, **kwargs):
        super(TaskTimerWidget, self).__init__(**kwargs)
        self.label = labelText
        self.isRepeatableFlag = isRepeatable
        self.isDoneFlag = False


class TimerApp(App):

    def build(self):
        self.root = RootWidget()
        return self.root

    def on_start(self):
        App.on_start(self)
        try:
            latestFile = max(
                glob.iglob(os.path.dirname(__file__) + '/*.[tT][xX][tT]'), key=os.path.getctime)
            inputTasks = open(
                os.path.join(os.path.dirname(__file__), latestFile), 'r')
        except (IOError, ValueError):
            print("No *.TXT file in directory. Starting without import...")
        else:
            dataFromJson = json.load(inputTasks, encoding='UTF8')
            for item in dataFromJson:
                item_dict = ast.literal_eval(item)
                if not(item_dict['isDone']) or (item_dict['isRepeatable']):
                    self.root.add_task(
                        item_dict['label'], bool(item_dict['isRepeatable']))
            inputTasks.close()

    def on_stop(self):
        App.on_stop(self)
        self.root.pickle_all()

if __name__ == "__main__":
    TimerApp().run()
