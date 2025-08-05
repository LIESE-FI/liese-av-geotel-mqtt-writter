#!/usr/bin/env python3
"""
Script to insert sample data into the database for testing purposes.
"""

import os
import sys
import uuid
from datetime import datetime, date
from dotenv import load_dotenv

# Add the src directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from Services.DatabaseConnection import DatabaseConnection

def create_sample_data():
    """Create sample data for testing the MQTT writer"""
    
    # Load environment variables
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    
    if not db_url:
        print("DATABASE_URL not found in environment variables")
        return
    
    db = DatabaseConnection(db_url)
    
    try:
        print("Creating sample data...")
        
        # Create Emergency Contacts
        emergency_contacts = [
            {
                'emergency_contact_id': str(uuid.uuid4()),
                'first_name': 'María',
                'last_name': 'González',
                'middle_name': 'Elena',
                'phone': '+52-555-123-4567'
            },
            {
                'emergency_contact_id': str(uuid.uuid4()),
                'first_name': 'Carlos',
                'last_name': 'Rodríguez',
                'middle_name': 'Antonio',
                'phone': '+52-555-987-6543'
            },
            {
                'emergency_contact_id': str(uuid.uuid4()),
                'first_name': 'Ana',
                'last_name': 'Martínez',
                'middle_name': 'Sofía',
                'phone': '+52-555-456-7890'
            }
        ]
        
        for contact in emergency_contacts:
            db.insert_data('EmergencyContacts', contact)
        
        print(f"✓ Created {len(emergency_contacts)} emergency contacts")
        
        # Create Drivers
        drivers = [
            {
                'driver_id': str(uuid.uuid4()),
                'first_name': 'Juan',
                'middle_name': 'Carlos',
                'last_name_1': 'Pérez',
                'last_name_2': 'López',
                'rfc': 'PELJ850101ABC',
                'phone': '+52-555-111-2222',
                'birthday': date(1985, 1, 1),
                'is_current': True,
                'score': 85.5,
                'blood_type': 'O+',
                'emergency_contact': emergency_contacts[0]['emergency_contact_id'],
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            {
                'driver_id': str(uuid.uuid4()),
                'first_name': 'María',
                'middle_name': 'Isabel',
                'last_name_1': 'García',
                'last_name_2': 'Hernández',
                'rfc': 'GAHM900215XYZ',
                'phone': '+52-555-333-4444',
                'birthday': date(1990, 2, 15),
                'is_current': True,
                'score': 92.3,
                'blood_type': 'A+',
                'emergency_contact': emergency_contacts[1]['emergency_contact_id'],
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            {
                'driver_id': str(uuid.uuid4()),
                'first_name': 'Roberto',
                'middle_name': 'José',
                'last_name_1': 'Sánchez',
                'last_name_2': 'Morales',
                'rfc': 'SAMR880320DEF',
                'phone': '+52-555-555-6666',
                'birthday': date(1988, 3, 20),
                'is_current': True,
                'score': 78.9,
                'blood_type': 'B+',
                'emergency_contact': emergency_contacts[2]['emergency_contact_id'],
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
        ]
        
        for driver in drivers:
            db.insert_data('Drivers', driver)
        
        print(f"✓ Created {len(drivers)} drivers")
        
        # Create Fleet
        fleets = [
            {
                'fleet_id': str(uuid.uuid4()),
                'fleet_name': 'Flota Norte',
                'created_at': datetime.now()
            },
            {
                'fleet_id': str(uuid.uuid4()),
                'fleet_name': 'Flota Sur',
                'created_at': datetime.now()
            },
            {
                'fleet_id': str(uuid.uuid4()),
                'fleet_name': 'Flota Centro',
                'created_at': datetime.now()
            }
        ]
        
        for fleet in fleets:
            db.insert_data('Fleet', fleet)
        
        print(f"✓ Created {len(fleets)} fleets")
        
        # Create Models
        models = [
            {
                'model_id': str(uuid.uuid4()),
                'model_name': 'Ford Transit 2023',
                'created_at': datetime.now()
            },
            {
                'model_id': str(uuid.uuid4()),
                'model_name': 'Mercedes Sprinter 2022',
                'created_at': datetime.now()
            },
            {
                'model_id': str(uuid.uuid4()),
                'model_name': 'Iveco Daily 2023',
                'created_at': datetime.now()
            }
        ]
        
        for model in models:
            db.insert_data('Models', model)
        
        print(f"✓ Created {len(models)} models")
        
        # Create Motor Statuses
        motor_statuses = [
            {
                'motor_status_id': str(uuid.uuid4()),
                'motor_status_value': 'running',
                'motor_status_description': 'Motor en funcionamiento'
            },
            {
                'motor_status_id': str(uuid.uuid4()),
                'motor_status_value': 'idle',
                'motor_status_description': 'Motor en ralentí'
            },
            {
                'motor_status_id': str(uuid.uuid4()),
                'motor_status_value': 'off',
                'motor_status_description': 'Motor apagado'
            }
        ]
        
        for status in motor_statuses:
            db.insert_data('MotorStatuses', status)
        
        print(f"✓ Created {len(motor_statuses)} motor statuses")
        
        # Create Notification Types
        notification_types = [
            {
                'notification_type_id': str(uuid.uuid4()),
                'notification_value': 'speed_limit_exceeded',
                'created_at': datetime.now()
            },
            {
                'notification_type_id': str(uuid.uuid4()),
                'notification_value': 'panic_button_pressed',
                'created_at': datetime.now()
            },
            {
                'notification_type_id': str(uuid.uuid4()),
                'notification_value': 'low_fuel',
                'created_at': datetime.now()
            },
            {
                'notification_type_id': str(uuid.uuid4()),
                'notification_value': 'engine_warning',
                'created_at': datetime.now()
            }
        ]
        
        for notif_type in notification_types:
            db.insert_data('NotificationTypes', notif_type)
        
        print(f"✓ Created {len(notification_types)} notification types")
        
        # Create Units (using deterministic UUIDs based on unit numbers)
        namespace = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')
        units = []
        
        for i in range(1, 4):  # Create units 1, 2, 3
            unit_data = {
                'unit_id': str(uuid.uuid5(namespace, f"unit_{i}")),
                'driver': drivers[i-1]['driver_id'],
                'fleet': fleets[i-1]['fleet_id'],
                'model': models[i-1]['model_id'],
                'motor_status': motor_statuses[0]['motor_status_id'],  # All running initially
                'fuel_level': 75.0 + i * 5,  # 80, 85, 90
                'current_speed': 0.0,
                'is_online': True,
                'panic_button_active': False,
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'rpm': 800,
                'temperature': 85,
                'check_engine': False
            }
            units.append(unit_data)
            db.insert_data('Units', unit_data)
        
        print(f"✓ Created {len(units)} units")
        
        print("\n🎉 Sample data created successfully!")
        print("\nCreated Units:")
        for i, unit in enumerate(units, 1):
            print(f"  Unit {i}: {unit['unit_id']}")
        
        print("\nYou can now test MQTT messages with topics like:")
        print("  U1_Combustible")
        print("  U2_Velocidad") 
        print("  U3_Panic")
        print("  etc.")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
