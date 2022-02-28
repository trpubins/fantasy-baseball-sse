# Fantasy-Baseball

Fantasy-Baseball is a Python project that utilizes microservices to generate
player values (in auction $$) for use in a fantasy baseball auction draft.

## Motivation

Downloading and consolidating projection data online is cumbersome and time-consuming.
Additionally, projections are continually updated as the season approaches rendering previously generated player values out-of-date.

A tool to automate the auction value generation process is paramount to fantasy draft success.

## Architecture

This project was architected as a client-server application, whereby the server downloads and persists projection spreadsheets from the internet and exposes the data over a RESTful API. The client makes http *GET* requests to the API to retrieve the projection data.

## Requirements

The project requires Python 3.9. Dependencies are captured in *requirements.txt* files, which are intended to be installed using pip like so:

```bash
# Download dependencies
pip install -r requirements.txt
```

## Usage

### Server

The server shall be launched before the client app. It is necessary to launch the server from the specified directory. From the project's root directory, navigate to *server/service-api/* and run the following command from a terminal:

```bash
# Run API microservice
python api.py
```

### Client

Next, the client app can be launched. It is necessary to launch the client from the specified directory. From the project's root directory, navigate to *client/src/* and run the following command from a terminal:

```bash
# Run client application
python main.py
```

### Network Config File

This project contains a network config file *network_cfg.json*. The config file contains two properties: "address" and "port".

#### Address

The address refers to the server IP address. The value for the IP address can be internal such as localhost (i.e. "127.0.0.1") or it can be external such as "192.168.1.5".

#### Port

The port refers to the server port number. Ensure the port number is not already in use.
