from multiprocessing import Pool
import json
from ActionKeeper import ActionServer, ActionManager

def testActionInput(actServ, testAction, desiredOut):
   #test that normal, single threaded input will result in expected values
   testActStr = json.dumps(testAction)
   actServ.addAction(testActStr)
   statStr = actServ.getStats()
   #turn the returned string into a list of objects
   #sort both lists so they will be equivalent if they have the same objects.
   outListSorted = sorted(json.loads(statStr), key=lambda k: k['action'])
   givenOutSorted = sorted(desiredOut, key=lambda k: k['action'])
   assert outListSorted == givenOutSorted
   print("Normal Function Test Passed!")

def testNormalFunction():
   #test regular functionality
   actServ = ActionServer()
   testAction = {"action": "jump", "time":50}
   outList = [{"action": "jump", "avg": 50}]
   testActionInput(actServ, testAction, outList)
   #add a few more actions to test averaging functionality
   testAction = {"action": "run", "time": 60}
   outList = [{"action": "jump", "avg": 50}, {"action": "run", "avg": 60}]
   testActionInput(actServ, testAction, outList)

   testAction = {"action": "jump", "time":100}
   outList = [{"action": "jump", "avg": 75}, {"action": "run", "avg": 60}]
   testActionInput(actServ, testAction, outList)
   
   testAction = {"action": "jump", "time":115}
   outList = [{"action": "jump", "avg": 88}, {"action": "run", "avg": 60}]
   testActionInput(actServ, testAction, outList)

   testAction = {"action": "run", "time":21}
   outList = [{"action": "jump", "avg": 88}, {"action": "run", "avg": 40}]
   testActionInput(actServ, testAction, outList)

def testBadInput(actServ, testAction):
   #bad or malformed input should throw a ValueError
   testActStr = json.dumps(testAction)
   didPass = False
   try:
      print("Testing bad input: "+testActStr)
      actServ.addAction(testActStr)
   except ValueError:
      print("Bad Input Test Passed!")
      didPass = True
   if not didPass:
      print("Bad Input Test Failed")

def testInvalidInputs():
   #test a few invalid inputs
   actServ = ActionServer()
   testAction = {}
   testBadInput(actServ, testAction)
   
   testAction = {"Action": "swim", 'time': 10}
   testBadInput(actServ, testAction)

   testAction = {'action': 'bike'}
   testBadInput(actServ, testAction)

   testAction = {'action': 'run', 'time': 'carrot'}
   testBadInput(actServ, testAction)

def testConcurrentInputs():
   #We used ActionServer before as we were only looking at a single thread.
   #For concurrent use, we need to have the ActionServer under new management.
   #ActionManager will hold our server in shared memory so all the sub-processes can access it.
   with ActionManager() as manager:
      actServ = manager.actServ()
      #create a list of inputs to enter concurrently
      actList = [
         {"action": "jump", "time":10},
         {"action": "run", "time":100},
         {"action": "swim", "time":50},
         {"action": "play", "time":80},
         {"action": "jump", "time":20},
         {"action": "run", "time":150},
         {"action": "swim", "time":20},
         {"action": "jump", "time":30},
         {"action": "run", "time":200},
         {"action": "swim", "time":70}
      ]
      #turn it into a list of json serialized strings
      actStrList = list(map(json.dumps, actList))

      p = Pool(processes=5)
      #distribute the inputs across the pool of workers
      p.map(actServ.addAction, actStrList)
      #after our workers have added all the data, see if it adds up correctly
      resultsStr = actServ.getStats()
      print(resultsStr)

      expectList = [{'action': 'jump', 'avg': 20}, {'action': 'run', 'avg': 150}, {'action': 'swim', 'avg': 46}, {'action': 'play', 'avg': 80}]

      outListSorted = sorted(json.loads(resultsStr), key=lambda k: k['action'])
      expectListSorted = sorted(expectList, key=lambda k: k['action'])
      assert outListSorted == expectListSorted
      print("Concurrency Test Passed!")


if __name__ == '__main__':
   testNormalFunction()
   testInvalidInputs()
   testConcurrentInputs()