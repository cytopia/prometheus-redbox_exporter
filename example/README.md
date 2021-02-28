# Example usage

This directory contains a fully dockerized (Docker Compose) ready-to-go setup with **Prometheus**, **Grafana** and the **redbox** exporter.


## 1. Create `redbox` config

* Navigate to `volumes/redbox/`
* Copy `conf.yml-example` to `conf.yml`
* Populate `conf.yml` as needed


## 2. Build image
```bash
docker-compose build
```


## 3. Start setup
```bash
docker-compose up
```


## 4. View Dashoard

Open Grafana
* URL: http://localhost:3000
* User: admin
* Pass: admin

Open Pre-build `redbox` dashboard
* Click on `Search` on the left menu
* Click on `HTTP status` under general folder
