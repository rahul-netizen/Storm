from pydantic import BaseModel as PydanticBaseModel, ConfigDict

class BaseModel(PydanticBaseModel):
    """Base model for all data models"""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


class BaseModelOrm(PydanticBaseModel):
    """Base model for all data models"""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
        from_attributes=True,
    )
