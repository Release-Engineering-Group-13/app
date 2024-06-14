# Application

The application consists of an app-frontend and an app-service. The frontend is an HTML/JSS page served through Flask. It communicates with the app-service API.


## app-frontend
The frontend is a simple HTML/JSS that querries the result from the app-service API and displays it.

### environment veriables
The frontend has the following environment options:
- API_URL - To change the app-service URL
- LAYOUT - choose the layout of the frontend, the options are "standard" and "colorfull"


## app-service
The app-service asks the model-service for the prediction and returns it to the app-frontend.

### environment veriables
The app-service has the following environment veriable:
- MODEL_SERVICE_URL - To change the model-service URL


## How to run
To run the application, you need to have docker and docker-compose installed. Then you can run the following command:
```bash
docker-compose up
```

This will start the app-frontend, app-service, and model-service. The app-frontend will be available at http://localhost:5000



