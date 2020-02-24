.PHONY: init pull build build-nc run clean cleanall
#Configure the primary node information in.env


init: 
	@which docker >/dev/null || ( echo "Error: Docker is not installed"; exit 1 )
	@which docker-compose >/dev/null || ( echo "Error: docker-compose is not installed"; exit 1 )

pull: init 
	@docker-compose pull #Pull the images

build: init
	@docker-compose build  #build images

build-nc: init
	@docker-compose build --no-cache

run: init pull build
	@docker-compose up -d
	@sleep 60
	@echo "Monitoring stack is started!"
	@echo "ElasticSearch Url: http://${ELASTICSEARCH_HOST}:9200/"
	@echo "Kibana Url: http://${KIBANA_HOST}:5601/"

beat: init pull build  #Execute commands from the node
	@docker-compose -f docker-compose.beat.yml up -d  #Execute the docker-compose yml file
	@sleep 60  #sleep
	@echo "Monitoring stack(Beats part) is started!"   #output
	@echo "ElasticSearch Url: http://${ELASTICSEARCH_HOST}:9200/"  #input
	@echo "Kibana Url: http://${KIBANA_HOST}:5601/"

clean: 
	@docker-compose down --remove-orphans -v

cleanall:
	@docker-compose down --remove-orphans --rmi all -v