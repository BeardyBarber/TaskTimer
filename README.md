# TaskTimer
Kivy application for everyday counting time of your computer tasks.


## Prerequisites

To run this app you need Python3 and Kivy module installed.
For instruction on installing kivy please refer to the [Instruction](https://kivy.org/doc/stable/installation/installation.html)

## Contributing

Please read [this](https://www.contributor-covenant.org/version/1/4/code-of-conduct) for details on our code of conduct, and the process for submitting pull requests to us.

## Running
After satysfying all prerequisites run ```python3 TaskTimer.py``` to start the app.

### App logic
After adding your first task you can see it on the screen. Each task has 2 flags **DONE** and **REPEATABLE**. 
Done flag is set after clicking the `DONE` button, this state is **final**.
Repeatable flag can be change freely, to change the flag simply click rapeat icon on the left.

Effects of afforementions flags are in table below:

|**DONE**|**REPEATABLE**|**Effect**|
|-------|----------------|----------|
|False|True|Task will be shown after app restart with last saved time|
|False|False|Task will be shown after app restart with last saved time|
|True|False|Task will not appear after aplication restart|
|True|True|Task will be shown after application restart with time = 0 (new)|

## Authors

* **Karol Majchrzak** - *Initial work* - [BeardyBarber](https://github.com/BeardyBarber)

See also the list of [contributors](https://github.com/BeardyBarber/TaskTimer/contributors) who participated in this project.

## License

This project is licensed under the APACHE License. For further information please read [LICENCE.MD](https://github.com/BeardyBarber/AddressBook/blob/master/LICENSE) 
