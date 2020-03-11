import json
from threading import Semaphore
from multiprocessing.managers import BaseManager

class ActionServer:
   """
      ActionServer is my solution to the Backend Assignment 4-17-2019 technical interview.
      It was designed with a cloud server idea in mind, as I imagined might be needed for a service that needs to process
      multiple connections and requests to both update and verify information.

      In order to be used in a concurrent fashion, the ActionServer needs to be spun up by an ActionManager (included below):
         with ActionManager() as manager:
            actionServer = manager.actServ()
            #do things with actionServer
      This is also demonstrated in the ActionKeeperTest file included in this package.

      ActionServer was designed to be extensible to network connectivity in future if such functionality was needed.
      The Python Manager library includes this ability, so updating ActionServer to work over a network would probably
      not require much of an overhaul.
   """

   def __init__(self):
      #create the dict to store incoming actions and times.
      self.actionStore = {}
      #need to be able to handle multiple incoming requests at once. 
      #Have the functions use a lock to keep from stepping on each other's toes.
      self.actLock = Semaphore()

   def addAction(self, actStr):
      with self.actLock:
         print("adding action")
         actObj = json.loads(actStr);
         #verify that the incoming actStr is valid
         if 'action' in actObj and actObj['action'] and 'time' in actObj and isinstance(actObj['time'], int):
            actionKey = actObj['action']
            actionTime = actObj['time']
            #keep times in a list so we can average them when needed.
            if actionKey in self.actionStore:
               self.actionStore[actionKey].append(actionTime)
            else:
               actTimeList = [actionTime]
               self.actionStore[actionKey] = actTimeList
         else:
            raise ValueError("Not a valid action input string!")
            

   def getStats(self):
      #grab the lock so that the data doesn't get rewritten while we're reading it
      with self.actLock:
         actionList = []
         for act, timeList in self.actionStore.items():
            actObj = {}
            actObj['action'] = act
            #average the times for the action. Make it an int since that's what was in the spec.
            actAvgTime = int(sum(timeList) / len(timeList))
            actObj['avg'] = actAvgTime
            actionList.append(actObj)
            actListStr = json.dumps(actionList)
         return actListStr

class ActionManager(BaseManager):
   """ActionManager was created as a way to handle concurrency.
      An object needs to be pickle-able to be able to pass between Processes.
      As is, ActionServer wasn't pickle-able, and it was easier to
      implement a separate manager that can create a shared
      object than to make the ActionServer class pickle-able.
   """
   pass

#register ActionServer so we can make one via the ActionManager to share between processes
ActionManager.register('actServ', ActionServer)
