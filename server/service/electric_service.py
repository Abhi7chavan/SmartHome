import time
import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from service.models.database import get_db
from service.submeters_service import get_submeter
from service.household_service import get_item_by_name
from confluent_kafka import Producer
import asyncio
import random
from typing import Dict, Union
from datetime import datetime,timedelta

router = APIRouter()


from confluent_kafka import Producer
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.routing import APIRouter
import asyncio
import json

router = APIRouter()

class KafkaProducer:
    def __init__(self, client_id='ems-household-manager'):
        self.producer = Producer({
            "bootstrap.servers": "localhost:9092",
            "client.id": client_id
        })
        self.topic = 'energy'

    def produce_message(self, message):
        self.producer.produce(topic=self.topic, value=json.dumps(message), callback=self.delivery_report)
        self.producer.flush()

    def delivery_report(self, err, msg):
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

    def close(self):
        self.producer.flush(timeout=5)
        self.producer.close()

producer = KafkaProducer()
realtime_data_task = None 

async def send_realtime_data_worker(username, db):
    submeter_data = await get_submeter(username, db)
    sub_data = submeter_data['data']
    associations = sub_data.get('associations', {})

    itemlist = []
    household_items = {}

    for record, items in associations.items():
        itemlist.extend(items)

    for item in itemlist:
        data = await get_item_by_name(item, db)
        data = data[0]
        household_items[data[1]] = {"watt_range": (data[2], data[3]), "is_on": True, "status": "cool"}

    try:
        while True:
            realtime_data = generate_realtime_data(household_items)
            producer.produce_message(realtime_data)
            await asyncio.sleep(2)
    except asyncio.CancelledError:
        pass
    finally:
        producer.close()

@router.get("/send_realtime_data/{username}")
async def send_realtime_data(username: str, db: Session = Depends(get_db)):
    global realtime_data_task
    if realtime_data_task and not realtime_data_task.done():
        return {"message": "Real-time data generation is already running."}

    realtime_data_task = asyncio.create_task(send_realtime_data_worker(username, db))
    return {"message": "Real-time data generation started."}

@router.post("/stop_realtime_data")
async def stop_realtime_data_route():
    global realtime_data_task
    if realtime_data_task and not realtime_data_task.done():
        realtime_data_task.cancel()
        return {"message": "Stopping real-time data generation."}
    else:
        return {"message": "Real-time data generation is not running."}

def generate_realtime_data(household_devices, current_time=None):
    timestamp = current_time if current_time else datetime.now().strftime("%H:%M:%S")

    real_time_data = {"total_consumption": 0, "items": {}}

    total_wattage = 0
    devices_data = {}

    for device, details in household_devices.items():
        if details["is_on"]:
            wattage = random.randint(details["watt_range"][0], details["watt_range"][1])
            status = "high" if wattage == details["watt_range"][1] else "low"

            # Update duration only if the device was on in the previous session
            if details.get("last_state", False):
                duration = details.get("duration", timedelta()) + timedelta(minutes=1)
            else:
                duration = details.get("duration", timedelta())

            # Update the last_state to True for the next iteration
            details["last_state"] = True

            current_energy_consumption = (wattage / 1000) * duration.total_seconds() / 3600
            total_consumption = details.get("total_consumption", 0) + current_energy_consumption

            # Format power factor to one decimal place
            power_factor = round(random.uniform(0.2, 0.9), 1)

            # Format total consumption with a short decimal and unit
            formatted_total_consumption = f"{total_consumption:.2f} kWh" if total_consumption > 0 else "0 kWh"

            device_data = {
                "is_on": details['is_on'],
                "wattage": wattage,
                "status": status,
                "timestamp": timestamp,
                "power_factor": power_factor,
                "voltage": random.randint(115, 120),
                "electric": formatted_total_consumption,
                "energy": details.get("energy", 1.0),
                "duration": f"Started {int(duration.total_seconds() / 60)} min ago",
                "last_state": details["last_state"],
                "current_consumption": current_energy_consumption,
            }

            devices_data[device] = device_data
            total_wattage += wattage
        else:
            # If the device is turned off, set last_state to False
            details["last_state"] = False

            device_data = {"wattage": 0, "status": "OFF", "electric": "0 kWh", "energy": 1.0, "duration": "Off", "last_state": details["last_state"]}
            devices_data[device] = device_data

    # Format total consumption for the entire household with a short decimal and unit
    formatted_total_wattage = f"{total_wattage:.2f} kWh" if total_wattage > 0 else "0 kWh"
    real_time_data["total_consumption"] = formatted_total_wattage
    real_time_data["items"] = devices_data

    return real_time_data