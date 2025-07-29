from datetime import datetime
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, field_validator, field_serializer
from app.domain.models.object_id import ObjectId
import re as regular_expression

class Movie(BaseModel):
    id: Optional[ObjectId] | str = None
    title: str
    plot: str
    release_date: datetime
    genre: List[str] | str
    director: List[str] | str
    rating: float
    poster: str

    @field_validator('release_date', mode='before')
    @classmethod
    def validate_release_date(cls, release_date: str) -> datetime:
        if isinstance(release_date, datetime):
            return release_date

        try:
            return datetime.strptime(release_date, '%Y')
        except ValueError:
            raise ValueError("Release date must be in the format YYYY")

    @field_validator('poster')
    @classmethod
    def validate_poster(cls, poster_url: str) -> str:
        # Only allow URLs from m.media-amazon.com
        if not regular_expression.match(r'^https://m.media-amazon.com/images/', poster_url):
            raise ValueError('Poster URL must be from m.media-amazon.com')
        return poster_url
    
    @field_validator('rating')
    @classmethod
    def validate_rating(cls, rating: float) -> float:
        if not (0 <= rating <= 5):
            raise ValueError('Rating must be between 0 and 5')

        # Rating must be separated by a dot, not a comma
        if ',' in str(rating):
            raise ValueError('Rating must use a dot as a decimal separator')
        
        # If rating got more than 2 decimal places, round it to 2
        if len(str(rating).split('.')[-1]) > 2:
            rating = round(rating, 2)
        return rating
    
    # Mode 'before' ensures that the validation runs before the field is set
    @field_validator('director', mode='before')
    @classmethod
    def validate_director(cls, director: Union[str, List[str]]) -> List[str]:
        if isinstance(director, str):
            return [director]
        elif isinstance(director, list):
            return list(set(director))
        raise ValueError('Director must be a string or a list of strings')
    
    @field_validator('genre', mode='before')
    @classmethod
    def validate_genre(cls, genre: Union[str, List[str]]) -> List[str]:
        if isinstance(genre, str):
            return [genre]
        elif isinstance(genre, list):
            return list(set(genre))
        raise ValueError('Genre must be a string or a list of strings')

    @field_serializer('id', when_used='json')
    def serialize_object_id(self, obj_id: Optional[ObjectId], _info) -> str | None:
        return str(obj_id) if obj_id else None
    
    @classmethod
    def from_mongo(cls, mongo_document: Dict) -> "Movie":
        # Convert MongoDB document to Movie instance
        return cls(
            id=str(mongo_document.get('_id')),
            **{key: value for key, value in mongo_document.items() if key != '_id'}
        )