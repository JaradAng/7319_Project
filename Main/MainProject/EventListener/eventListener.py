from EventConsumer.PersonConsumer import PersonSecurityAnalysis
from EventConsumer.VehicleConsumer import VehicleSecurityAnalysis

class EventListener:
    def __init__(self, db_config):
        # Initialize analysis classes
        self.person_analysis = PersonSecurityAnalysis(db_config)
        self.vehicle_analysis = VehicleSecurityAnalysis(db_config)

    def process_data(self, data):
        """Process incoming data from DataProducer."""
        tracker_output = data.get('tracker_output', [])
        
        for track in tracker_output:  
            class_id = track[-2]  

            if class_id == 0:
                print("Routing to person analysis.")
                self.person_route(track)
            elif class_id in [2, 7]:
                print("Routing to vehicle analysis.")
                self.vehicle_route(track)

    def person_route(self, track):
        # print("Data sent to Person Route:", track)
        self.person_analysis.analyze(track)

    def vehicle_route(self, track):
        print("Data sent to Vehicle Route:", track)
        self.vehicle_analysis.analyze(track)


if __name__ == "__main__":
    db_config = {}  # Future database connection
    listener = EventListener(db_config=db_config)

   

 
