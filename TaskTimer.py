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

    def add_task(self, label_text, is_repeatable):
        try:
            if label_text == '':
                raise ValueError('Cannot create task from empty String!')
        except ValueError as e:
            print(e)
        else:
            task = TaskTimerWidget(label_text, is_repeatable)
            self.add_widget(task)
            self.ids.new_task.text = ''
            self.ids.repeatable.active = False

    def stop_all(self):
        """Stops all tasks."""
        for child in self.children:
            if(type(child) == TaskTimerWidget):
                Clock.unschedule(child.update)

    def get_tasks(self):
        """Creates and return dict with all tasks."""
        data = []
        for child in self.children:
            if(type(child) == TaskTimerWidget):
                data.append(str(child))
        return data


class TaskTimerWidget(BoxLayout):
    seconds = NumericProperty(0)
    label = StringProperty('')
    is_repeatable_flag = BooleanProperty(False)
    is_done_flag = BooleanProperty(False)

    def __str__(self):
        return str({"time": self.seconds, "label": self.label, "is_repeatable": self.is_repeatable_flag, "is_done": self.is_done_flag})

    def __init__(self, label_text, is_repeatable, **kwargs):
        super(TaskTimerWidget, self).__init__(**kwargs)
        self.label = label_text
        self.is_repeatable_flag = is_repeatable
        self.is_done_flag = False

    def update(self, dt):
        self.seconds += dt

    def stop(self):
        Clock.unschedule(self.update)
        self.is_done_flag = True

    def start(self):
        Clock.schedule_interval(self.update, .016)

    @staticmethod
    def format(sec):
        m, s = divmod(sec, 60)
        h, m = divmod(m, 60)
        return "%02d:%02d:%02d" % (h, m, s)


class TimerApp(App):

    def build(self):
        self.root = RootWidget()
        return self.root

    def on_start(self):
        App.on_start(self)
        self.__import_tasks(self.__find_latest_file())

    def on_stop(self):
        App.on_stop(self)
        self.__pickle_tasks(self.root.get_tasks())

    def __find_latest_file(self):
        """Finds latest modified *.json file and returns it as String"""
        # find latest modified JSON file in program residence directory
        latest_file = max(
            glob.iglob(os.path.dirname(__file__) + '/*.[jJ][sS][oO][nN]'), key=os.path.getctime)
        if not os.path.isfile(latest_file):
            raise IOError('Cannot find a file!')
        input_tasks = open(
            os.path.join(os.path.dirname(__file__), latest_file), 'r')
        return input_tasks.read()

    def __import_tasks(self, data):
        if data:
            data_from_json = json.load(data)
            for item in data_from_json:
                item_dict = ast.literal_eval(item)
                if not(item_dict['is_done']) or (item_dict['is_repeatable']):
                    self.root.add_task(
                        item_dict['label'], bool(item_dict['is_repeatable']))

    def __pickle_tasks(self, data):
        file = open(os.path.join(
            os.path.dirname(__file__), time.strftime('%d_%m_%Y') + '.json'), 'w')
        json.dump(data, file, indent=4, separators=(',', ': '))
        file.close()

if __name__ == "__main__":
    TimerApp().run()
