import datetime
import dbpipe as db

class Client:
    name, location = ''
    hourlyRate = 0
    appointmentDate
    clientList = []
    verifyMembership = false
    
    def __init__(self, name, location, hourlyRate):
        self._name = name
        self._location = location
        self._hourlyRate = hourlyRate
        
    def newAppointment(self):
        self._appointmentDate = datetime.datetime(Field.getYear, Field.Getmonth, Field.getDay)
        #TODO update database

    def appointmentReminder(self):
        #if(self._appointmentDate == datetime.datetime.now()):
            #TODO reminder
        
class Runner:
    """clientList = []
    
    def newClient(self, Client):
        clientList.append(Client(Field.getName, Field.getLocation, Field.getHourlyRate))
        """
        
    def newClient(self, Client):
        #send Client to database
        db.ToDatabase(Client)
    
        
        

        
    #TODO reminder for appointments
    #TODO update database
    
    
        
    