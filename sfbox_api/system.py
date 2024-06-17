from typing import Literal, Optional

from pydantic import BaseModel, ValidationError, field_validator


class Sys(BaseModel):
    name: str = "name"
    temperature: float = 298.15
    overflow_protection: Optional[Literal["true", "false"]] = None  # default false
    super_iteration: Optional[Literal["true", "false"]] = None  # default false
    super_fuction_value: Optional[float] = None
    super_tolerance: Optional[float] = None

    @field_validator("temperature")
    @classmethod
    def validate_temperature(cls, value):
        if value and value < 0.0:
            raise ValueError("Sys: temperature < 0.0")
        return value


if __name__ == "__main__":
    input = {"temperature": 300.0}
    try:
        syst = Sys.model_validate(input)
        for p in syst:
            if p[1]:
                print(f"lat : {syst.name} : {p[0]} : {str(p[1])}")
    except ValidationError as err:
        print(err.json(indent=4))
