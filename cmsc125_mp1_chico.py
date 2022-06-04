"""
    FILE:       cmsc125_mp1_chico.py
    ABOUT:      Implement a time-sharing system (with multiprogramming)

    NAME:       Melzar Jan E. Chico
    COURSE:     CMSC125 B
    DATE:       2022 March 16
    TASK:       Machine Problem 1

    NOTE:       When running local, please use `from msvcrt import getch` instead when using getch(). Thank you!
"""

from math import floor
#from msvcrt import getch    # use this if running in your local
from getch import getch    # use this if running in repl.it
import random

class User:
    def __init__(self, index:int) -> None:
        self.__index = index

    def __repr__(self) -> str:
        return f'User{str(self.__index).zfill(2)}'

class Task:
    def __init__(self, user:User, time:int) -> None:
        self.__requester = user
        self.__maxTime = time
        self.__remTime = 0
        self.__status = 'waiting'

    def getTaskStatus(self) -> str:
        return self.__status

    def getRemainingTime(self) -> int:
        return self.__remTime

    def getMaxTime(self) -> int:
        return self.__maxTime

    def activate(self) -> None:
        self.__status = 'active'

    def update(self) -> None:
        if (self.__status == 'active'):
            self.__remTime += 1
            if (self.__remTime >= self.__maxTime):
                self.__status = 'done'
        else:
            print(f'ERROR: {self} is not yet active.')

    def __repr__(self) -> str:
        # text-related stats 
        taskStat = f'{str(self.__remTime).zfill(2)}/{str(self.__maxTime).zfill(2)}'
        statusStat = '{:<7}'.format(self.__status.upper())

        # for the progress bar stats
        rawTaskNumbers = floor((self.__remTime/self.__maxTime) * 10)
        progressBar = '█'*rawTaskNumbers + '░'*(10-rawTaskNumbers)

        return f'Task <{str(self.__requester)}: {statusStat}, {taskStat} {progressBar}>'

class Resource:
    def __init__(self, index:int) -> None:
        self.__index:int = index
        self.__taskQueue:list[Task] = []
        self.__curentTask:Task = None
        self.__doneTask:Task = None
        self.__status:str = 'offline'

    def getResourceStatus(self) -> str:
        return self.__status

    def addTask(self, user:User, time:int) -> None:
        self.__taskQueue.append(Task(user, time))

    def start(self) -> None:
        if self.__taskQueue:
            self.__status = 'busy'
            self.nextTask()
        else:
            self.__status = 'free'
    
    def nextTask(self) -> None:
        self.__doneTask = self.__curentTask
        if self.__taskQueue:
            self.__curentTask = self.__taskQueue.pop(0)
            self.__curentTask.activate()
        else:
            self.__curentTask = None
            self.__status = 'free'

    def update(self) -> None:
        self.__doneTask = None
        if self.__curentTask:
            if self.__curentTask.getTaskStatus() != 'done':
                self.__curentTask.update()
                if self.__curentTask.getTaskStatus() == 'done':
                    self.nextTask()
        print(self.stats())

    def stats(self) -> None:
        statString = f'======= [RESOURCE {str(self.__index).zfill(2)}] =======\n'
        waitTime = 0

        if self.__status == 'busy':
            statString += f'\t{self.__doneTask}\n' if self.__doneTask else ''
            statString += f'\t{self.__curentTask}\n'
            waitTime += self.__curentTask.getMaxTime() - self.__curentTask.getRemainingTime()

            for task in self.__taskQueue:
                statString += f'\t{task}, {waitTime}s til start\n'
                waitTime += task.getMaxTime()
        else:
            if self.__doneTask:
                statString += f'\t{self.__doneTask}\n'
            else:
                statString += "\tNO TASKS IN QUEUE.\n"
        return statString

    def __repr__(self) -> str:
        return f'Resource{str(self.__index).zfill(2)}'


def checkResources(resource_list:'list[Resource]') -> bool:
    for resource in resource_list:
        if resource.getResourceStatus() != 'free':
            return True
    return False
    

def main():
    user_list:list[User] = []
    resource_list:list[Resource] = []
    timer = 0
    
    # ! (1) generate user list
    for i in range(random.randint(1, 30)):
        user_list.append(User(i+1))

    # ! (2) generate resource list
    for i in range(random.randint(1, 30)):
        resource_list.append(Resource(i+1))

    # ! (3) generate each user a random needed resource with random time
    for user in user_list:
        chosenResource:Resource = random.choice(resource_list)
        chosenResource.addTask(user, random.randint(1,30))

    # ! query
    print("Do you want to print the results ALL AT ONCE? (y/n)")
    userChoice = input("CHOICE: ")

    while userChoice not in ['y', 'n']:
        userChoice = input("Try again! - CHOICE: ")
    
    print()

    # ! initializing resources    
    print('*'*50)
    print(f'USERS: {user_list}')
    print(f'RESOURCES: {resource_list}')
    print(f'TIME: {timer}s\n')

    for resource in resource_list:
        resource.start()
        print(resource.stats())

    print('*'*50)

    if userChoice == 'n':
        print("Press any key to continue.")
        getch()
    timer += 1
    print()

    # ! main loop
    while checkResources(resource_list):
        print('*'*50)
        print(f'USERS: {user_list}')
        print(f'RESOURCES: {resource_list}')
        print(f'TIME: {timer}s\n')

        for resource in resource_list:
            resource.update()

        print('*'*50)
        
        if userChoice == 'n':
            print("Press any key to continue.")
            getch()
        timer += 1
        print()

main()