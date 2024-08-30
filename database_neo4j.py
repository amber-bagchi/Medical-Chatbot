from neo4j import GraphDatabase
import os

class HospitalDatabaseManager:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_hospital(self):
        with self.driver.session() as session:
            session.run("""
            MERGE (h:Hospital {name: 'Wellness City Hospital', 
                               address: '123 Health Avenue, Wellness City, HC 45678', 
                               phone: '+1-234-567-8900', 
                               email: 'contact@ourhospital.com', 
                               website: 'www.ourhospital.com'})
            """)

    def create_services(self):
        services = [
            "Emergency Care", "Outpatient Services", "Inpatient Services", 
            "Surgery and Operating Theatres", "Diagnostic Imaging", 
            "Laboratory Services", "Maternity Services", "Pediatric Care", 
            "Cardiology Services", "Oncology Services", "Neurology Services", 
            "Orthopedic Services", "Physical Therapy", "Pharmacy Services", 
            "Mental Health Services"
        ]
        with self.driver.session() as session:
            for service in services:
                session.run("""
                MATCH (h:Hospital {name: 'Wellness City Hospital'})
                MERGE (s:Service {name: $service})
                MERGE (h)-[:OFFERS]->(s)
                """, service=service)

    def create_doctors(self):
        doctors = [
    {"name": "Dr. Elizabeth Weaver", "specialization": "Psychologist, counselling", "experience": 10, "availability": "03:00:36 - 09:45:30"},
    {"name": "Dr. Jasmine Wolfe", "specialization": "Optician, dispensing", "experience": 5, "availability": "13:08:31 - 23:24:50"},
    {"name": "Dr. Christopher Bennett", "specialization": "Land", "experience": 7, "availability": "07:13:40 - 14:12:07"},
    {"name": "Dr. Sean Hill", "specialization": "Immunologist", "experience": 9, "availability": "14:03:14 - 16:33:54"},
    {"name": "Dr. Dorothy West", "specialization": "Quarry manager", "experience": 6, "availability": "20:39:05 - 08:28:16"},
    {"name": "Dr. Joshua Greene", "specialization": "Therapist, art", "experience": 4, "availability": "21:47:33 - 03:12:08"},
    {"name": "Dr. Samuel Barron", "specialization": "Cytogeneticist", "experience": 8, "availability": "18:45:09 - 03:47:39"}
]
        with self.driver.session() as session:
            for doc in doctors:
                session.run("""
                MATCH (h:Hospital {name: 'Wellness City Hospital'})
                MERGE (d:Doctor {name: $name, specialization: $specialization, experience: $experience, availability: $availability})
                MERGE (h)-[:HAS_DOCTOR]->(d)
                """, name=doc["name"], specialization=doc["specialization"], experience=doc["experience"], availability=doc["availability"])

    def get_services_info(self):
        with self.driver.session() as session:
            result = session.run("MATCH (s:Service)<-[:OFFERS]-(h:Hospital {name: 'Wellness City Hospital'}) RETURN s.name")
            services = [record["s.name"] for record in result]
        return "Our hospital offers the following services: " + ", ".join(services)

    def get_doctors_info(self):
        with self.driver.session() as session:
            result = session.run("MATCH (d:Doctor)<-[:HAS_DOCTOR]-(h:Hospital {name: 'Wellness City Hospital'}) RETURN d.name, d.specialization, d.availability")
            doctors = [f"{record['d.name']} ({record['d.specialization']}) - Availability: {record['d.availability']}" for record in result]
        return "Here are the doctors available at our hospital: " + ", ".join(doctors)

# Example usage:
neo4j_uri = "neo4j+s://5521eb19.databases.neo4j.io"
neo4j_pass = "zkXJkL6v9a2QldrAg-BYYkmVy9Tu73HREPFebfKKlw8"

db_manager = HospitalDatabaseManager(neo4j_uri, "neo4j", neo4j_pass)
db_manager.create_hospital()
db_manager.create_services()
db_manager.create_doctors()
db_manager.close()
