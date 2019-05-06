'''
	Fetoiu Catalin-Emil, 341C3
'''

from elasticsearch import Elasticsearch
import pika
import json
import sys, time, random

queue_name = 'logs2'
ipinfo_handler = None

rabbit_connection = None
rabbit_channel = None

elasticsearch_client = None
elasticsearch_port = '9200'

countries = ['Romania', 'France', 'United Kingdom', 'Germany']

def get_location(ip_address):
	return random.choice(countries)

def callback(ch, method, properties, body):
	print(" [x] Received %r" % body)

	event = json.loads(body)
	event['location'] = get_location(event['ip'])

	event_type = event['event_type']
	index = event_type + '_index'

	print(event)
	res = elasticsearch_client.index(index=index, doc_type='log', body=event)

	ch.basic_ack(delivery_tag = method.delivery_tag)

def connect_to_rabbit(host):
	global rabbit_channel
	global rabbit_connection

	rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters(host))
	rabbit_channel = rabbit_connection.channel()
	rabbit_channel.queue_declare(queue=queue_name, durable=True)

	rabbit_channel.basic_consume(queue=queue_name,
								on_message_callback=callback)

	rabbit_channel.start_consuming()

def connect_to_elasticsearch():
	global elasticsearch_client

	elasticsearch_client = Elasticsearch([{'host': host, 'port': elasticsearch_port}])


def main():
	connect_to_rabbit(sys.argv[1])
	connect_to_elasticsearch(sys.argv[2])


if __name__ == "__main__":
    main()