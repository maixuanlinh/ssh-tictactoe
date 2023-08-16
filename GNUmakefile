CONTAINER_BASE := ssh/assignment/front

.PHONY: build run

build:
	docker build -t ${CONTAINER_BASE} .

run: build
	docker run -p 5555:5000 ${CONTAINER_BASE}
