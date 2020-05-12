run:
	./manage.py runserver
postgres:
	docker-compose up ticketing_postgres
kafka:
	docker-compose up ticketing_kafka
listener:
	./manage.py run_kafka_consumer