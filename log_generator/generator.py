'''
	Fetoiu Catalin-Emil, 341C3
'''

import time, sys
import random
import string
import json
import pika

events_per_second = 10
queue_name = 'logs2'

ip_addresses = ['20.187.69.219', '114.16.93.195', '71.26.105.228', '3.3.83.233', '175.94.246.190',
				'126.56.171.117', '165.211.148.30', '181.28.24.96', '118.6.69.250', '241.22.221.160']

user_anons = ['a5595do8de', 'z4zo4xwqej', 'o9gm30nn18', 'r716x69yaf', 'qyip9iveg2',
				'dtpvtt4io9', 'xohmvv4xcu', 'px10dhf3xs', '0v2qfw5m78', '1ky8oihkqd']

event_types = ['event_A', 'event_B', 'event_C', 'event_D', 'event_E', 'event_F']

rabbit_connection = None
rabbit_channel = None

def connect_to_rabbit(host):
	global rabbit_connection
	global rabbit_channel

	rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters(host))
	rabbit_channel = rabbit_connection.channel()
	rabbit_channel.queue_declare(queue=queue_name, durable=True)

def publish_event(event):
	global rabbit_channel

	rabbit_channel.basic_publish(exchange='',
							routing_key=queue_name,
							body=event)

def get_timestamp():
	return int(time.time())

def generate_event(timestamp):
	ip = random.choice(ip_addresses)
	user = random.choice(user_anons)
	event_type = random.choice(event_types)
	
	event_json = {
		'ip': ip,
		'user': user,
		'event_type': event_type,
		'timestamp': timestamp
	}

	return json.dumps(event_json)

def main():
	connect_to_rabbit(sys.argv[1])

	while True:
		timestamp = get_timestamp()

		for _ in range(events_per_second):
			event = generate_event(timestamp)
			print(event)
			publish_event(event)

		time.sleep(1)

if __name__ == "__main__":
    main()