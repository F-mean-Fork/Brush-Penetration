from typing import Literal, Optional

from pydantic import BaseModel, field_validator, model_validator

# import warnings
# warnings.filterwarnings('ignore')

MINIMAL_VALUE = 1e-9


class Mon(BaseModel):
    name: str = ""
    freedom: Literal["free", "pinned", "frozen"] = "free"
    pinned_range: Optional[str] = None
    frozen_range: Optional[str] = None
    valence: Optional[float] = None
    epsilon: Optional[float] = None

    @field_validator("epsilon")
    @classmethod
    def validate_epsilon(cls, value):
        if value and value < 1.0:
            raise ValueError("Mon: epsilon < 1.0")
        return value

    @model_validator(mode="after")
    @classmethod
    def validate_restrictions(cls, fields):
        if fields.freedom == "free":
            if fields.pinned_range or fields.frozen_range:
                raise ValueError("Mon: free does not require pinned or frozen range")
        elif fields.freedom == "pinned":
            if fields.frozen_range or not fields.pinned_range:
                raise ValueError("Mon: pinned requires pinned range")
        else:
            if fields.freedom == "frozen":
                if fields.pinned_range or not fields.frozen_range:
                    raise ValueError("Mon: pinned requires pinned range")
        return fields

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if value == "" or value[0].isdigit():
            raise ValueError("Mon: molecule has incorrect name")
        return value
