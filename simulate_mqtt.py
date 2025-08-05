#!/usr/bin/env python3
"""
Script to simulate MQTT messages for testing the MQTT writer.
"""

import paho.mqtt.client as mqtt
import random
import time
import json
import argparse

def simulate_unit_data(client, unit_number, delay=2):
    """Simulate telemetry data for a specific unit"""
    
    topics_and_ranges = {
        'Combustible': (0, 100),      # Fuel level percentage
        'Velocidad': (0, 120),        # Speed in km/h
        'RPM': (600, 3000),           # Engine RPM
        'Temperatura': (70, 110),     # Engine temperature in Celsius
        'Latitud': (19.4, 19.5),     # Latitude (Mexico City area)
        'Longitud': (-99.2, -99.1),  # Longitude (Mexico City area)
    }
    
    print(f"Starting simulation for Unit {unit_number}")
    
    while True:
        try:
            # Generate random values for each parameter
            for topic_suffix, (min_val, max_val) in topics_and_ranges.items():
                # Use the original format with underscore: U1_Combustible
                topic = f"U{unit_number}_{topic_suffix}"
                
                if topic_suffix in ['Latitud', 'Longitud']:
                    # GPS coordinates with more precision
                    value = round(random.uniform(min_val, max_val), 6)
                elif topic_suffix in ['RPM', 'Temperatura']:
                    # Integer values
                    value = random.randint(int(min_val), int(max_val))
                else:
                    # Float values with 1 decimal
                    value = round(random.uniform(min_val, max_val), 1)
                
                # Publish the value
                result = client.publish(topic, str(value))
                if result.rc == 0:
                    print(f"✅ Published: {topic} = {value}")
                else:
                    print(f"❌ Failed to publish: {topic} = {value} (rc: {result.rc})")
                
                # Small delay between topics
                time.sleep(0.1)
            
            # Occasionally simulate panic button (rare event)
            if random.random() < 0.05:  # 5% chance
                panic_topic = f"U{unit_number}_Panic"
                panic_value = "1"
                result = client.publish(panic_topic, panic_value)
                print(f"🚨 Published: {panic_topic} = {panic_value}")
                
                # Send panic off after a few seconds
                time.sleep(3)
                result = client.publish(panic_topic, "0")
                print(f"✅ Published: {panic_topic} = 0")
            
            print(f"--- Waiting {delay} seconds for next cycle ---")
            time.sleep(delay)
            
        except KeyboardInterrupt:
            print(f"\nStopping simulation for Unit {unit_number}")
            break
        except Exception as e:
            print(f"Error in simulation: {e}")
            time.sleep(1)

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}")
    else:
        print("Connected to MQTT broker successfully")

def main():
    parser = argparse.ArgumentParser(description='Simulate MQTT telemetry data')
    parser.add_argument('--unit', type=int, default=1, help='Unit number to simulate (default: 1)')
    parser.add_argument('--host', type=str, default='localhost', help='MQTT broker host (default: localhost)')
    parser.add_argument('--port', type=int, default=1883, help='MQTT broker port (default: 1883)')
    parser.add_argument('--delay', type=int, default=2, help='Delay between cycles in seconds (default: 2)')
    parser.add_argument('--all-units', action='store_true', help='Simulate all units (1, 2, 3)')
    
    args = parser.parse_args()
    
    if args.all_units:
        import threading
        
        def simulate_unit(unit_num):
            client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
            client.on_connect = on_connect
            client.connect(args.host, args.port, 60)
            client.loop_start()
            simulate_unit_data(client, unit_num, args.delay)
            client.disconnect()
        
        print("Starting simulation for all units (1, 2, 3)")
        threads = []
        
        for unit_num in [1, 2, 3]:
            thread = threading.Thread(target=simulate_unit, args=(unit_num,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
            time.sleep(1)  # Stagger the start times
        
        try:
            for thread in threads:
                thread.join()
        except KeyboardInterrupt:
            print("\nStopping all simulations...")
    
    else:
        # Simulate single unit
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.on_connect = on_connect
        
        print(f"Connecting to MQTT broker at {args.host}:{args.port}")
        client.connect(args.host, args.port, 60)
        client.loop_start()
        
        simulate_unit_data(client, args.unit, args.delay)
        
        client.disconnect()

if __name__ == "__main__":
    main()
