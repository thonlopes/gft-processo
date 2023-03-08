.PHONY: build

build:
	@cd hadoop/base && docker build . -t hadoop-base && cd ../..
	@cd spark/base && docker build . -t spark-base && cd ../..
	@docker-compose up -d
