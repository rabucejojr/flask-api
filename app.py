from flask import Flask, jsonify, request
import Adafruit_DHT
import RPi.GPIO as GPIO
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Setup GPIO pin for DHT11 sensor
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  # GPIO4

# Define MQ137 pin
MQ_PIN = 17  # GPIO17
# MySQL Configuration
mysql_config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database'
}

# Function to save sensor data to MySQL
def save_sensor_data(sensor_type, value):
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()
    query = "INSERT INTO sensor_data (sensor_type, value) VALUES (%s, %s)"
    cursor.execute(query, (sensor_type, value))
    connection.commit()
    connection.close()

def save_data(timestamp, temperature, humidity, gas_level):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''INSERT INTO sensor_data (timestamp, temperature, humidity, gas_level) VALUES (?, ?, ?, ?)''',
              (timestamp, temperature, humidity, gas_level))
    conn.commit()
    conn.close()

def read_dht11_sensor():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    return temperature, humidity

def read_mq137_sensor():
    # Read from MQ137 sensor (Example)
    # This function should be replaced with actual code to read data from the MQ137 sensor
    gas_level = 0  # Placeholder
    return gas_level

@app.route('/api/data', methods=['GET', 'POST'])
def sensor_data():
    if request.method == 'GET':
        temperature, humidity = read_dht11_sensor()
        gas_level = read_mq137_sensor()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_data(timestamp, temperature, humidity, gas_level)
        return jsonify({
            'timestamp': timestamp,
            'temperature': temperature,
            'humidity': humidity,
            'gas_level': gas_level
        })
    elif request.method == 'POST':
        data = request.json
        temperature = data.get('temperature')
        humidity = data.get('humidity')
        gas_level = data.get('gas_level')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_data(timestamp, temperature, humidity, gas_level)
        return jsonify({'message': 'Data saved successfully'}), 201

if __name__ == '__main__':
    create_table()
    app.run(host='0.0.0.0', port=5000)
