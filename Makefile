build:
	pack build maxtet1703/tetris-backend-v1:latest --buildpack paketo-buildpacks/python --builder paketobuildpacks/builder-jammy-base
up:
	docker compose up --build
up_prod:
	docker compose up --build -d
down:
	docker compose down -v
remove-image:
	docker rmi tetris-tech-app
