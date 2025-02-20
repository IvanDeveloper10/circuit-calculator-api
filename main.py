from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Circuit Calculator API",
    description="API for basic electrical circuit calculations.",
    version="1.0.0"
)

class CircuitCalculations(BaseModel):
    voltage: Optional[float] = None
    resistance: Optional[float] = None
    current: Optional[float] = None
    resistance_values: List[float] = []
    circuit_type: str = "series"

@app.get("/equivalent_resistance")
def equivalent_resistance(values: List[float], circuit_type: str):
    if not values:
        raise HTTPException(status_code=400, detail="You must provide at least one resistance value.")
    
    if circuit_type == "series":
        return {"equivalent_resistance": sum(values)}
    elif circuit_type == "parallel":
        try:
            return {"equivalent_resistance": 1 / sum(1/r for r in values)}
        except ZeroDivisionError:
            raise HTTPException(status_code=400, detail="Division by zero is not allowed in resistance calculation.")
    else:
        raise HTTPException(status_code=400, detail="Invalid type, use 'series' or 'parallel'.")

@app.get("/ohms_law")
def ohms_law(voltage: Optional[float] = None, resistance: Optional[float] = None, current: Optional[float] = None):
    if voltage is None and resistance is not None and current is not None:
        return {"voltage": resistance * current}
    elif resistance is None and voltage is not None and current is not None:
        return {"resistance": voltage / current}
    elif current is None and voltage is not None and resistance is not None:
        return {"current": voltage / resistance}
    else:
        raise HTTPException(status_code=400, detail="Provide only two values to calculate the third.")

@app.get("/power")
def power(voltage: float, current: float):
    return {"power": voltage * current}

@app.post("/calculations")
def calculations(data: CircuitCalculations):
    results = {}

    if data.voltage and data.resistance:
        results["current"] = data.voltage / data.resistance
    if data.voltage and data.current:
        results["power"] = data.voltage * data.current
    if data.resistance_values:
        if data.circuit_type == "series":
            results["equivalent_resistance"] = sum(data.resistance_values)
        else:
            try:
                results["equivalent_resistance"] = 1 / sum(1/r for r in data.resistance_values)
            except ZeroDivisionError:
                raise HTTPException(status_code=400, detail="Division by zero is not allowed in resistance calculation.")

    return results
