# Front end of integration app 2023

This is the front end of the application for the integration evening. 

## Getting Started

To run the app locally, please [install flutter](https://docs.flutter.dev/get-started/install) and move to the **front/** directory

To run the app type: ```flutter run -d chrome```


## Init

Add the following environment variables to an .env file at the root of the project:

```
# Secret partagé entre le front et le back
FRONT_TOKEN=token

# Variable d'environnement
API_SRV_HOSTNAME=api_inte
API_SRV_PORT=80
API_SRV_PROTOCOL=http
```

Then execute the following command : `$source .env`