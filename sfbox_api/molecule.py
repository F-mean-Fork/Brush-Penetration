from typing import Literal, Optional

from pydantic import (BaseModel, ValidationError, field_validator,
                      model_validator)

# import warnings
# warnings.filterwarnings('ignore')

MINIMAL_VALUE = 1e-9


class Mol(BaseModel):
    name: str = ""
    freedom: Literal["free", "restricted", "solvent", "neutralizer"] = "free"
    phibulk: Optional[float] = None
    composition: str
    theta: Optional[float] = None

    @model_validator(mode="after")
    @classmethod
    def validate_restrictions(cls, fields):
        if fields.freedom == "free":
            if fields.theta or not fields.phibulk:
                raise ValueError("Mol: free requires theta (not phibulk)")
        elif fields.freedom == "restricted":
            if fields.phibulk or not fields.theta:
                raise ValueError("Mol: restricted requires phibulk (not theta)")
        else:
            if fields.theta or fields.phibulk:
                raise ValueError("Mol: phibulk or theta sould be absent")
        return fields

    @field_validator("phibulk", "theta")
    @classmethod
    def validate_negative_values(cls, value):
        if value and value < MINIMAL_VALUE:
            raise ValueError("Mol: phibulk or theta < 0.0")
        return value

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if value == "" or value[0].isdigit():
            raise ValueError("Mol: molecule has incorrect name")
        return value


if __name__ == "__main__":
    input = {
        "name": "water",
        "freedom": "free",
        "phibulk": 1.0,
        "composition": "(H)2(O)1",
    }
    try:
        mol = Mol.model_validate(input)
        for p in mol:
            if p[1]:
                print(f"mol : {mol.name} : {p[0]} : {str(p[1])}")
    except ValidationError as err:
        print(err.json(indent=4))
