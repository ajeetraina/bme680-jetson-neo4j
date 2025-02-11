from neo4j import GraphDatabase
from datetime import datetime, timedelta

class Neo4jEnhanced:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def store_reading_with_analysis(self, reading, analysis):
        with self.driver.session() as session:
            session.run("""
            CREATE (s:SensorReading {
                timestamp: datetime(),
                temperature: $temperature,
                humidity: $humidity,
                pressure: $pressure,
                gas: $gas
            })-[:HAS_ANALYSIS]->(a:Analysis {
                content: $analysis,
                timestamp: datetime()
            })
            """, {
                'temperature': reading['temperature'],
                'humidity': reading['humidity'],
                'pressure': reading['pressure'],
                'gas': reading['gas'],
                'analysis': analysis
            })

    def get_historical_readings(self, hours=24):
        with self.driver.session() as session:
            result = session.run("""
            MATCH (s:SensorReading)
            WHERE s.timestamp > datetime() - duration($hours + 'h')
            RETURN s
            ORDER BY s.timestamp
            """, {'hours': hours})
            return [dict(record['s']) for record in result]

    def get_latest_analysis(self):
        with self.driver.session() as session:
            result = session.run("""
            MATCH (a:Analysis)
            RETURN a.content as analysis
            ORDER BY a.timestamp DESC
            LIMIT 1
            """)
            return result.single()['analysis'] if result.peek() else None
