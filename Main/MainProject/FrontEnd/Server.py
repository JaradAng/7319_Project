from DataProducer.dataProducer import DataProducer  # Assuming DataProducer is defined in a file named data_producer.py
from EventListener.eventListener import EventListener  # Assuming EventListener is defined in a file named event_listener.py
from fastapi import FastAPI
from uvicorn import run
from threading import Thread

class APIService:
    def __init__(self):
        # Initialize FastAPI app
        self.app = FastAPI()

        # Global variables for FastAPI to store data
        self.person_data = []
        self.vehicle_data = []

        # FastAPI routes
        self.app.post("/add_person_data/")(self.add_person_data)
        # print('posted data')
        self.app.post("/add_vehicle_data/")(self.add_vehicle_data)
        self.app.get("/get_person_data/")(self.get_person_data)
        self.app.get("/get_vehicle_data/")(self.get_vehicle_data)

    async def add_person_data(self, data: dict):
        self.person_data.append(data)
        return {"status": "success"}

    async def add_vehicle_data(self, data: dict):
        self.vehicle_data.append(data)
        return {"status": "success"}

    async def get_person_data(self):
        return {"data": self.person_data}

    async def get_vehicle_data(self):
        return {"data": self.vehicle_data}

    def run_service(self):
        run(self.app, host="0.0.0.0", port=8000)
        print('service running')