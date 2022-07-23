# Fantasy Baseball

This project utilizes a server-sent-events (SSE) framework to generate
player values (in auction $$) for use in a fantasy baseball auction draft.

## Motivation

Downloading and consolidating projection data online is cumbersome and time-consuming.
Additionally, projections are continually updated as the season approaches rendering previously generated player values out-of-date.

A tool to automate the auction value generation process is paramount to fantasy draft success.

## Architecture

This project was architected as a client-server application, whereby the server downloads and persists projection spreadsheets from the internet and exposes the data over a RESTful API. The client makes HTTP `GET` requests to the API to retrieve the projection data.

## Virtual Environment (Recommended)

A virtual environment is recommended to separate Python system packages from project-specific packages. The instructions to initialize and activate a Python virtual environment are provided below.

### 1. Create Virtual Environment

Start by creating a Python virtual environment that references a specific Python interpreter accessible to the user. From a terminal inside the project root dir, run

```bash
< path-to-python3.9 > -m venv .venv
```

### 2. Activate Virtual Environment

To activate the Python virtual environment, open a bash terminal from the project root dir, and run the following command

```bash
source .venv/bin/activate
```

Confirm the virtual environment is active by typing

```bash
which python
```

It should be in the .venv dir: `.../.venv/bin/python`.

If the system Python interpreter and its associated packages are needed, deactivating the virtual environment is as simple as running

```bash
deactivate
```

## Requirements

The project was built with `Python 3.9`; other versions of `Python 3` may work but have not been tested. Dependencies are captured in *requirements.txt* files, which are intended to be installed using pip like so

```bash
# Download dependencies
pip install -r requirements.txt
```

If a virtual environment was created, dependencies will be installed only in the virtual environment and will not pollute the Python system package space.

## Usage

### Server

The server shall be launched `before` the client app. From the project root run the following command

```bash
# Run API microservice
python server/api.py
```

### Client

Next, the client app can be launched. From the project root run the following command

```bash
# Run client application
python client/main.py
```

### Network Config File

This project contains a network config file *network_cfg.json*. The config file contains two properties: (1) `address` and (2) `port`.

#### Address

The address refers to the server IP address. The value for the IP address can be internal such as localhost (i.e. "127.0.0.1") or it can be external such as "192.168.1.5".

#### Port

The port refers to the server port number. Ensure the port number is not already in use.
