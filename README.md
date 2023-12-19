# Benchmark File Parser and Digital Circuit Simulator

This repository contains a set of endpoints designed to parse benchmark files for digital circuits and simulate their behavior based on input parameters and fault configurations.

## Deployment

Install the requirements using the following command:
```bash
pip install -r requirements.txt
```

## Start the Application
To start the API, run the following command:
```bash
python3 main.py
```
## Endpoints

### 1. Parse and Build

Endpoint: `/parse-and-build`

Description: Parses the specified benchmark file into a custom class and returns the build object in a dictionary format.


### 2. Simulate

Endpoint: `/simulate`

Description: Simulates the digital circuit with specified input parameters and potential stuck-at fault.

Request Body:
```json
{
  "file_name": "example.txt",
  "input_params": [
    {
      "wire_name": "string",
      "value": true
    }
  ],
  "stuck_at": {
    "wire_name": "string",
    "value": true
  }
}
```

### 2. Serial Simulation

Endpoint: `/serial_simulation`

Description: Perform serial simulation
Request Body:
```json
{
  "file_name": "example.benchmark",
  "input_params": [
    {
      "wire_name": "string",
      "value": true
    }
  ],
  "stuck_at": [
    {
      "wire_name": "string",
      "value": true
    }
  ]
}
```

