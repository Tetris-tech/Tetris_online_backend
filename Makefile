build:
	pack build tetris-tech-app --buildpack paketo-buildpacks/python \
	--builder paketobuildpacks/builder-jammy-base
up:
	docker compose up --build
up_prod:
	docker compose up --build -d
down:
	docker compose down -v
remove-image:
	docker rmi tetris-tech-app
