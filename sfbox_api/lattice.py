from typing import Literal, Optional

from pydantic import (BaseModel, ValidationError, field_validator,
                      model_validator)

# import warnings
# warnings.filterwarnings('ignore')


class Lat(BaseModel):
    name: str = "name"
    gradients: Literal[1, 2] = 1
    geometry: Literal["flat", "cylindrical", "spherical"] = "flat"
    n_layers: Optional[int] = None
    n_layers_x: Optional[int] = None
    n_layers_y: Optional[int] = None
    lambda1: str = "0.16666666666666666667"
    latticetype: Literal["standard", "stencils"] = "standard"
    bondlength: float = 3.1e-10
    offset_first_layer: Optional[float] = None
    offset_first_layer_x: Optional[float] = None
    offset_first_layer_y: Optional[float] = None
    lowerbound: Literal["surface", "mirror1", "mirror2", "periodic", "bulk"] = "mirror1"
    upperbound: Literal["surface", "mirror1", "mirror2", "periodic", "bulk"] = "mirror1"

    @field_validator("lambda1")
    @classmethod
    def validate_lambda1(cls, value):
        if any([not x.isdigit() for x in value.split(".")]):
            raise ValueError("Lat: format of lambda1 is not correct")
        return value

    @model_validator(mode="after")
    @classmethod
    def validate_gradients_dependencies(cls, fields):
        if fields.gradients == 1:
            if (not fields.n_layers) or fields.n_layers_x or fields.n_layers_y:
                raise ValueError(
                    "Lat: by gradients=1 n_layers must be set without n_layers_x or n_layers_y"
                )
            if not (0 < float(fields.lambda1) <= 0.5):
                raise ValueError("Lat: valid values 0 < lambda1 <= 0.5")
        if fields.gradients == 2:
            if fields.n_layers or not (fields.n_layers_x and fields.n_layers_y):
                raise ValueError(
                    "Lat: by gradients=2 n_layers_x and n_layers_y must be set without n_layers"
                )
            if not (0 < float(fields.lambda1) <= 0.25):
                raise ValueError("Lat: valid values 0 < lambda1 <= 0.25")
        return fields

    @field_validator("n_layers", "n_layers_x", "n_layers_y")
    @classmethod
    def validate_n_layers(cls, value):
        if value and value < 1:
            raise ValueError("Lat: n_layers(x/y) < 1")
        return value

    @field_validator(
        "bondlength",
        "offset_first_layer",
        "offset_first_layer_x",
        "offset_first_layer_y",
    )
    @classmethod
    def validate_negative_values(cls, value):
        if value and value < 0.0:
            raise ValueError("Lat: n_layers(x/y) < 1")
        return value


if __name__ == "__main__":
    input = {"n_layers_x": 100, "n_layers_y": 100, "geometry": "flat", "gradients": 2}
    try:
        lattice = Lat.model_validate(input)
        for p in lattice:
            if p[1]:
                print(f"lat : {lattice.name} : {p[0]} : {str(p[1])}")
    except ValidationError as err:
        print(err.json(indent=4))
