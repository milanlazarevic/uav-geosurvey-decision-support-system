# UAV Flight Decision System

## Prerequisites
- Java 11+
- Maven
- Node.js 16+
- Python 3.8+


## 1. Backend (Spring Boot + Drools)

```
cd model
../mvnw clean install

cd ../kjar
../mvnw clean install

cd service
mvn spring-boot:run
```

Backend runs on: http://localhost:8080

## 2. Frontend (React)

cd frontend
npm install
npm start

Frontend runs on: http://localhost:5173

## 3. Python CLI

cd python-cli
pip install -r requirements.txt
python cli.py

## How Drools Rules Work

CSV files with thresholds:
- src/main/resources/data/battery-thresholds.csv
- src/main/resources/data/gnss-thresholds.csv

Template generates rules at startup:
- src/main/resources/templates/threshold-template.drt

Rules trigger when values cross thresholds:
- Battery < 10% = CRITICAL
- Battery < 20% = LOW
- Battery < 30% = WARNING
- HDOP > 5.0 = POOR GNSS
- Satellites < 4 = FEW SATELLITES
- Satellites < 6 = MARGINAL

## Testing

- CEP unit tests
- python cli script has all 17 cases covered up
  (uses websocket for communication and frontend is subscribed to the topic so progress can be watched real-time from the frontend app) 
