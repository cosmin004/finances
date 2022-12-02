build_docker_local:
	docker-compose build
run_docker_local: build_docker_local
run_docker_local:
	docker-compose up