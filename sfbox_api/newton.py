from typing import Literal, Optional

from pydantic import BaseModel, ValidationError, field_validator


class Newton(BaseModel):
    name: str = "isaac"
    method: Literal[
        "hessian", "pseudohessian", "LBFGS", "CG", "SD", "TN", "BRR", "Pure_DIIS"
    ] = "pseudohessian"
    tolerance: float = 1e-7
    iterationlimit: Optional[int] = 10000000
    deltamax: float = 0.5
    deltamin: float = 0.0
    DIIS: Optional[int] = None  # 1, 2 ..
    m: Optional[int] = None  # 32, 64 ..

    @field_validator("tolerance", "deltamax")
    @classmethod
    def validate_params(cls, value):
        if value and value <= 0:
            raise ValueError("Newton: some integer parameter <= 0")
        return value


if __name__ == "__main__":
    input = {"DIIS": 1}
    try:
        newton = Newton.model_validate(input)
        for p in newton:
            if p[1]:
                print(f"newton : {newton.name} : {p[0]} : {str(p[1])}")
    except ValidationError as err:
        print(err.json(indent=4))
