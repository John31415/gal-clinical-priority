from src.domain.resource import Resource


class ResourceRequirement:
    resource: Resource
    quantity: float

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError("quantity must be positive")
