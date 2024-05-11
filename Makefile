.PHONY: up
up: ## Run docker containers
	docker-compose up

.PHONY: down
down: ## Stop docker containers
	docker-compose down

.PHONY: clear-image
remove: ## Stop and delete docker container with service
	docker image remove cryptproj-app

.PHONY: logs
logs: ## Run container logs (container must be running)
	docker logs -f CryptoProjApp

.PHONY: shell
shell: ## Run container shell (container must be running)
	docker exec -it CryptoProjApp /bin/sh

.PHONY: linters
linters: ## Run code linters (container must be running)
	docker exec -it CryptoProjApp bash -c "black . ; isort . ; flake8"

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