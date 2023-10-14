import os
from pyfair import FairModel
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import numpy as np

# Get the host and port from the environment variables, or use defaults
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', '8000'))

# Initialize FastAPI with a title and a description
app = FastAPI(
    title="FAIR Model Simulation API",
    description="A web API to simulate risk assessment based on the FAIR model using various input parameters."
)

# Define request models to validate input parameters
class ThreatEventFrequency(BaseModel):
    low: float = 0.5
    mode: float = 1.25
    high: float = 2.0

class SecondaryLossEventFrequency(BaseModel):
    low: float = 0.95
    mode: float = 0.97
    high: float = 0.99

class SecondaryLossEventMagnitude(BaseModel):
    low: float = 3350000.0
    mode: float = 3850000.0
    high: float = 8000000.0

class ThreatCapability(BaseModel):
    low: float = 0.6
    mode: float = 0.85
    high: float = 0.99

class PrimaryLoss(BaseModel):
    low: float = 4000.0
    mode: float = 16000.0
    high: float = 216000.0

class ControlStrength(BaseModel):
    low: float = 0.75
    mode: float = 0.85
    high: float = 0.95

class SimulationInput(BaseModel):
    n_simulations: int = 10000
    threat_event_frequency: ThreatEventFrequency
    secondary_loss_event_frequency: SecondaryLossEventFrequency
    secondary_loss_event_magnitude: SecondaryLossEventMagnitude
    threat_capability: ThreatCapability
    primary_loss: PrimaryLoss
    control_strength: ControlStrength

# Define the API endpoint
@app.post("/simulate/")
async def simulate(data: SimulationInput):
    # Limit the number of simulations
    if data.n_simulations > 100000:
        raise HTTPException(status_code=400, detail="n_simulations value exceeds the limit of 100,000.")

    # Initialize the FAIR model with provided inputs
    model = FairModel(name='FAIR Model', n_simulations=data.n_simulations)
    model.input_data('Threat Event Frequency', **data.threat_event_frequency.dict())
    model.input_data('Secondary Loss Event Frequency', **data.secondary_loss_event_frequency.dict())
    model.input_data('Secondary Loss Event Magnitude', **data.secondary_loss_event_magnitude.dict())
    model.input_data('Threat Capability', **data.threat_capability.dict())
    model.input_data('Primary Loss', **data.primary_loss.dict())
    model.input_data('Control Strength', **data.control_strength.dict())

    # Calculate the results
    model.calculate_all()
    results = model.export_results()

    # Prepare statistics for the response
    statistics = {
        "loss_magnitude": {
            "minimum": int(results['Loss Magnitude'].min()),
            "maximum": int(results['Loss Magnitude'].max()),
            "average": int(results['Loss Magnitude'].mean())
        },
        "primary_loss": {
            "minimum": int(results['Primary Loss'].min()),
            "maximum": int(results['Primary Loss'].max()),
            "average": int(results['Primary Loss'].mean())
        },
        "secondary_loss": {
            "minimum": int(results['Secondary Loss'].min()),
            "maximum": int(results['Secondary Loss'].max()),
            "average": int(results['Secondary Loss'].mean())
        },
        "loss_event_frequency": {
            "minimum": round(results['Loss Event Frequency'].min(), 2),
            "maximum": round(results['Loss Event Frequency'].max(), 2),
            "average": round(results['Loss Event Frequency'].mean(), 2)
        },
        "secondary_loss_event_frequency": {
            "minimum": round(results['Secondary Loss Event Frequency'].min(), 2),
            "maximum": round(results['Secondary Loss Event Frequency'].max(), 2),
            "average": round(results['Secondary Loss Event Frequency'].mean(), 2)
        },
        "vulnerability": {
            "average": round(results['Vulnerability'].mean(), 2)
        }
    }

    # Process and add loss exceedance data
    sorted_losses = results['Loss Magnitude'].sort_values(ascending=False).values
    probabilities = [i / len(sorted_losses) for i in range(1, len(sorted_losses) + 1)]
    sample_indices = np.linspace(0, len(sorted_losses) - 1, 100, dtype=int)
    sampled_losses = sorted_losses[sample_indices]
    sampled_probabilities = [probabilities[i] for i in sample_indices]
    ale_data = [{"Probability of Loss or Greater": round(p, 2), "Loss Exposure": round(loss, 2)} for p, loss in zip(sampled_probabilities, sampled_losses)]

    statistics["lossExceedanceData"] = ale_data

    return statistics

# Run the application with Uvicorn when the script is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
