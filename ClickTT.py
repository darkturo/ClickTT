import httplib
import json
import base64
import datetime

# When called, it will retrieve the state of the current counter (for work) in
# toggle, it will decide whether it needs to start or stop it, to finally
# perform the desired action.
def click(input, context):
   config = { "api_token": "xxxxxxxxxxxxxxxxxxxxxxxxxxx",
              "wid": 1929122,
              "pid": 21921919 }

   toggl = TogglService(config)

   return toggl.toggleTimerButton()

# Class modellign the toggl service, which will be instantiated and use from
# the click function.
# Note that TogglService is suposed to be used and discarded afterwards, the
# idea is to have state representing the current toggl serivce for a certain
# user in the moment of the instantiation.
class TogglService:
   TOGGL = "www.toggl.com"
   CURRENT = "/api/v8/time_entries/current"
   START = "/api/v8/time_entries/start"
   STOP = "/api/v8/time_entries/time_entry_id/stop"

   def __init__(self, config):
      self.workspaceId = config["wid"]
      self.projectId = config["pid"]
      self.token = base64.b64encode(config["api_token"] + ":api_token")
      self.headers = { 
          "Authorization": "Basic " + self.token,
          "Content-Type": "application/json"
      }

      self.dataCache = {};
      self._updateCacheWithToggleState()

   def _updateCacheWithToggleState(self):
      with HttpsTogglConnection(TogglService.TOGGL) as togglConn:
         # HTTP GET request to www.toggl.com/api/v8/time_entries/current
         togglConn.request("GET", TogglService.CURRENT, headers = self.headers)
         httpResponse = togglConn.getresponse()

         # Parse and return the JSON structure into something that python can use
         self.dataCache = json.loads( httpResponse.read() )

   def isTimerOnGoing(self):
      return self.dataCache["data"] != None

   def toggleTimerButton(self):
      self._updateCacheWithToggleState()

      operation   = ""
      currentTime = datetime.datetime.now().isoformat() 

      result = False
      if self.isTimerOnGoing():
         operation = "Stop"
         result = self.stopTimer()
      else:
         operation = "Start"
         result = self.startTimer()

      if result:
         print "%s timer on %s" % (operation, currentTime)
      else:
         print "Failed to %s the timer!!!"

      return result

   def startTimer(self):
      if self.isTimerOnGoing():
         self.stopTimer()

      # Preparing the parameters to encode in the POST request
      params = { "time_entry": { 
                 "description": "Working",
                 "billable": True,
                 "wid": self.workspaceId,
                 "pid": self.projectId,
                 "created_with": "flic",
                 "start": datetime.datetime.now().isoformat() } }

      # HTTP POST request to www.toggl.com/api/v8/time_entries/start to start the timer
      success = False
      with HttpsTogglConnection(TogglService.TOGGL) as togglConn:
         togglConn.request("POST", TogglService.START, json.dumps(params), self.headers)
         httpResponse = togglConn.getresponse()
         success = httpResponse.status == 200

      return success

   def stopTimer(self):
      if self.isTimerOnGoing():
         tid = str(self.dataCache["data"]["id"])
         stopRequest = TogglService.STOP.replace("time_entry_id", tid)

      success = False
      with HttpsTogglConnection(TogglService.TOGGL) as togglConn:
         togglConn.request("PUT", stopRequest, headers = self.headers)
         httpResponse = togglConn.getresponse()
         success = httpResponse.status == 200

      return success


class HttpsTogglConnection:
   def __init__(self, service_fqdn):
      self.conn = httplib.HTTPSConnection( service_fqdn )
      self.conn.connect()

   def __enter__(self):
      return self

   def __exit__(self, exc_type, exc_value, traceback):
      self.conn.close()

   def request(self, *args, **kwargs):
      return self.conn.request(*args, **kwargs)

   def getresponse(self):
      return self.conn.getresponse()

# Main
if __name__ == "__main__":
   click({}, {})

