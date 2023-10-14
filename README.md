# FAIR Model Simulation API

This project serves as an API to simulate FAIR (Factor Analysis of Information Risk) models using various user-defined parameters. Please note that this project simply provides the convenience of an API and optional Docker wrapper, the underlying simulations rely on the excellent work done by the the Hive-Systems team at [pyFAIR library](https://github.com/Hive-Systems/pyfair).

The feature set is currently limited to a subset of the full FAIR model (see Usage section) that is in use for the [Arco Cyber Platform](https://arcocyber.com). We welcome contributions to expand the feature set to cover the full FAIR model.

## Prerequisites

- Python 3.8+
- Docker (optional)

## Installation

### Using pip

1. Clone the repository:

   ```bash
   git clone https://github.com/arcocyber/fair-simulation-api.git
   cd fair-simulation-api
   ```

2. Create a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: .\venv\Scripts\activate
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the FastAPI server:

   ```bash
   uvicorn main:app --reload
   ```

### Using Docker

1. Clone the repository:

   ```bash
   git clone https://github.com/arcocyber/fair-simulation-api.git
   cd fair-simulation-api
   ```

2. Build the Docker image:

   ```bash
   docker build -t fair-simulation-api .
   ```

3. Run the Docker container:

   ```bash
   docker run -p 8000:8000 fair-simulation-api
   ```

### Using Docker Compose

1. Clone the repository:

   ```bash
   git clone https://github.com/arcocyber/fair-simulation-api.git
   cd fair-simulation-api
   ```

2. With `docker-compose`, it's straightforward to start the service:

   ```bash
   docker-compose up
   ```

   To run in detached mode:

   ```bash
   docker-compose up -d
   ```

3. If you ever need to stop the service:

   ```bash
   docker-compose down
   ```


## Usage

Once the server is running, you can:

- Visit the FastAPI documentation at `http://127.0.0.1:8000/docs` to see the available endpoints and test them out.
- Send requests to `http://127.0.0.1:8000/simulate` (or whichever endpoint you've set up) with the desired parameters.

Example Payload:

```json
{
    "n_simulations": 100000,
    "threat_event_frequency": {
        "low": 0.5,
        "mode": 1.25,
        "high": 2
    },
    "secondary_loss_event_frequency": {
        "low": 0.95,
        "mode": 0.97,
        "high": 0.99
    },
    "secondary_loss_event_magnitude": {
        "low": 3350000,
        "mode": 3850000,
        "high": 8000000
    },
    "threat_capability": {
        "low": 0.6,
        "mode": 0.85,
        "high": 0.99
    },
    "primary_loss": {
        "low": 4000,
        "mode": 16000,
        "high": 216000
    },
    "control_strength": {
        "low": 0.75,
        "mode": 0.85,
        "high": 0.95
    }
}
```

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## Licensing

This project is licensed under the MIT License.