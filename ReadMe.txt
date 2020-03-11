Welcome to the ActionKeeper library!  A fun way to store all your data about average times for actions. Useful for high school track & field coaches, people who love timing themselves, and testing potential new hires!  

ActionKeeper was written and tested in Python 3.8.1 and is not guaranteed to work on earlier versions, especially not 2.X versions.

ActionKeeper usage:
ActionKeeper does its magic via the ActionServer class.  ActionServer can be used in two ways: 

Single-threaded:
	ActionKeeper was written for use in single-threaded applications with no configuration or setup out of the box! simply import ActionServer, create a new ActionServer object, and go.

Multi-threaded:
	In order to make use of ActionServer on a multi-threaded environment, it must be managed by the included ActionManager class. Simply create an ActionManager and then create the desired ActionServer via ActionManager.actServ().  For Examples, see comments in ActionKeeper.py or the testConcurrentInputs function in ActionKeeperTest.py

ActionServer has two handy methods you can call for all of your action storage needs:
	addAction(actStr)  accepts a stringified json object in the form:
		{'action':'[name of action]', 'time': [int time of action]}
	getStats() returns a stringified json list of objects with all the actions ActionServer is keeping track of as well as the average time taken for each action.

If you have any questions or comments regarding the ActionKeeper library, or wish to hire the handsome developer who created it, please contact Nate Hillman at natehillman156@gmail.com or call (207)-660-7381.