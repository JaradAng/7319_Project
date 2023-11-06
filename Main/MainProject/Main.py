import os
from threading import Thread
from DataProducer.dataProducer import DataProducer  # Assuming DataProducer is defined in a file named data_producer.py
from EventListener.eventListener import EventListener  # Assuming EventListener is defined in a file named event_listener.py
from FrontEnd.Server import APIService
from FrontEnd.App import StreamlitDashboard




def main():
    # Database configuration for EventListener
    db_config = {
        # Your database configuration here
    }

    os.system("streamlit run FrontEnd/App.py --server.port 8502 &")
   
    # Create an instance of EventListener with the database configuration
    listener = EventListener(db_config=db_config)

    # Create an instance of DataProducer
    producer = DataProducer()

    # Register the EventListener instance as an observer to DataProducer
    producer.register_observer(listener)

    # Initialize FastAPI service
    api_service = APIService()
    api_thread = Thread(target=api_service.run_service)
    api_thread.start()


    # Initialize Streamlit Dashboard
    streamlit_dashboard = StreamlitDashboard()
    streamlit_thread = Thread(target=streamlit_dashboard.run_app)
    streamlit_thread.start()

    # Start the DataProducer's loop
    producer.run()

if __name__ == '__main__':
    main()
    
