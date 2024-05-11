.PHONY: build
build: ## Build image and docker container
	docker build -t crypt_proj-image . && docker run  -p 0.0.0.0:8000:8000 --env-file .env --name cryptoProj -v $(shell pwd):/home/appuser crypt_proj-image

.PHONY: remove
remove: ## Stop and delete docker container
	docker rm -f cryptoProj

.PHONY: logs
logs: ## Run container logs (container must be running)
	docker logs -f cryptoProj

.PHONY: shell
shell: ## Run container shell (container must be running)
	docker exec -it cryptoProj /bin/sh

.PHONY: linters
linters: ## Run code linters (container must be running)
	docker exec -it cryptoProj bash -c "black . ; isort . ; flake8"

.PHONY: help
help: ## Show this help instruction
	@echo "Usage: make [target]"
	@echo "Targets:"
	@awk '/^[a-zA-Z0-9_-]+:.*?##/ { \
		helpMessage = match($$0, /## (.*)/); \
		if (helpMessage) { \
			target = $$1; \
			sub(/:/, "", target); \
			printf "  \033[36m%-20s\033[0m %s\n", target, substr($$0, RSTART + 3, RLENGTH); \
		} \
	}' $(MAKEFILE_LIST)