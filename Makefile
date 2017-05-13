SRV_PATH=/srv/burnyourcode.com
HUGO=$(SRV_PATH)/hugo-linux64

.PHONY: deploy_rsync deploy_git sakura
help: ## Print this help text
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

deploy_rsync: ## Build locally and rsync to server
	./hugo && rsync -avz --exclude='.git/' --delete . ark:$(SRV_PATH)

deploy_git: ## git based deployment
	ssh -t ark "cd ark:$(SRV_PATH)  &&\
		git pull && \
		$(HUGO)"

sakura:
	cp /cabinet/lab/sakura.css/css/sakura-vader.css themes/sakura/static/css/sakura.css
