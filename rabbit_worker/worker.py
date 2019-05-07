'''
	Fetoiu Catalin-Emil, 341C3
'''

from elasticsearch import Elasticsearch
import pika
import json
import sys, time, random

queue_name = 'logs'

rabbit_connection = None
rabbit_channel = None

elasticsearch_client = None
elasticsearch_port = '9200'

countries = ['Romania', 'France', 'United Kingdom', 'Germany', 'Spain', 'Italy']

def get_location(ip_address):
	return random.choice(countries)

def callback(ch, method, properties, body):
	global elasticsearch_client

	print(" [x] Received %r" % body)

	event = json.loads(body)
	event['country'] = get_location(event['ip'])

	event_type = event['event_type']
	index = event_type + '_index'

	print(event)
	elasticsearch_client.index(index=index, doc_type='log', body=event)

	ch.basic_ack(delivery_tag = method.delivery_tag)

def connect_to_rabbit(host):
	global rabbit_channel
	global rabbit_connection

	while True:
		try:
			rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters(host))
			break
		except:
			time.sleep(1)

	rabbit_channel = rabbit_connection.channel()
	rabbit_channel.queue_declare(queue=queue_name, durable=True)

	rabbit_channel.basic_consume(queue=queue_name,
								on_message_callback=callback)

	rabbit_channel.start_consuming()

def connect_to_elasticsearch(host):
	global elasticsearch_client

	while True:
		try:
			elasticsearch_client = Elasticsearch([{'host': host, 'port': elasticsearch_port}])
			break
		except:
			time.sleep(1)


def main():
	connect_to_elasticsearch(sys.argv[2])
	connect_to_rabbit(sys.argv[1])


if __name__ == "__main__":
    main()