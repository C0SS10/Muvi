from pydantic import BaseModel

class ObjectId(BaseModel):
    id: str

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not isinstance(value, str):
            raise TypeError(f"ObjectId must be a string, got {type(value).__name__}")
        if len(value) != 24:
            raise ValueError("ObjectId must be a 24-character hexadecimal string")
        return cls(id=value)