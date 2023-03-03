.PHONY: build

build:
	@cd hadoop/base && docker build . -t hadoop-base && cd ../..
	@cd spark/base && docker build . -t spark-base && cd ../..
	@cd airflow && docker build . --tag pyrequire_airflow:2.5.1


	@docker-compose up

