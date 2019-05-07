'''
	Fetoiu Catalin-Emil, 341C3
'''

from elasticsearch import Elasticsearch
import json
import sys, time

elasticsearch_client = None
elasticsearch_port = '9200'

event_types = ['event_a', 'event_b', 'event_c', 'event_d', 'event_e', 'event_f']

def connect_to_elasticsearch(host):
	global elasticsearch_client

	while True:
		try:
			elasticsearch_client = Elasticsearch([{'host': host, 'port': elasticsearch_port}])
			break
		except:
			time.sleep(1)

def get_timestamp():
	return int(time.time())

def count_all_events(event):
	event_index = event + '_index'

	res = elasticsearch_client.search(index=event_index, body={
		'query': {
			'match_all': {}
		}
	})

	results = res['hits']['hits']
	return len(results)

def count_events(timestamp_bound, event):
	event_index = 'event_' + event + '_index'

	res = elasticsearch_client.search(index=event_index, body={
		'query': {
			'range' : {
	            'timestamp' : {
					'gte' : timestamp_bound
	            }
			}
		}
	})

	results = res['hits']['hits']
	print('Found ' + str(len(results)) + ' events')

def most_active(event, field):
	event_index = 'event_' + event + '_index'

	res = elasticsearch_client.search(index=event_index, body={
		'query': {
			'match_all': {}
		}
	})

	results = res['hits']['hits']
	event_count = dict()
	for result in results:
		event_json = result['_source']
		field_value = event_json[field]

		if not (field_value in event_count):
			event_count[field_value] = 0

		event_count[field_value] = event_count[field_value] + 1

	final_count = []
	for field_value in event_count:
		final_count.append((event_count[field_value], field_value))

	sorted_count = reverse(sorted(event_count))

	print('Most active ' + field + ' is ' + str(sorted_count[0][1]))

def majority_event():
	event_count = []

	for event in event_types:
		count = count_all_events(event)
		event_count.append((count, event))

	sorted_count = reverse(sorted(event_count))

	print('Most frequent event is ' + str(sorted_count[0][1]))

def search_word(word, event):
	event_index = 'event_' + event + '_index'

	res = elasticsearch_client.search(index=event_index, body={
		'query': {
			'wildcard' : {
				'message' : '*' + word + '*' 
			}
		}
	})

	results = res['hits']['hits']
	print('Found ' + str(len(results)) + ' events containing ' + word)

def main():
	connect_to_elasticsearch(sys.argv[1])

	while True:
		print('Select operation: ')
		print('Enter 1 for counting events of certain type')
		print('Enter 2 for finding user with most events')
		print('Enter 3 for finding country with most events')
		print('Enter 4 for finding the most frequent event')
		print('Enter 5 for finding number of events containing a word')

		option = input('adsadasdadasda')
		
		if option == '1':
			print('Enter number of seconds:')
			count = int(input())
			print('Enter event type (a ... f):')
			event = input()

			timestamp = get_timestamp() - count
			count_events(timestamp, event)

		elif option == '2':
			print('Enter event type (a ... f):')
			event = input()

			most_active(event, 'user')
		elif option == '3':
			print('Enter event type (a ... f):')
			event = input()

			most_active(event, 'country')
		elif option == '4':
			majority_event()
		elif option == '5':
			print('Enter word to search for:')
			word = input()
			print('Enter event type (a ... f):')
			event = input()

			search_word(word, event)

if __name__ == "__main__":
    main()