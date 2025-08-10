from typing import List, Optional

from pydantic import BaseModel, Field


class MovieUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=8)
    plot: Optional[str] = Field(None, min_length=8)
    director: Optional[str] = None
    release_date: Optional[str] = None 
    genre: Optional[List[str]] = None 
    rating: Optional[float] = None
    poster: Optional[str] = None

    class Config:
        extra = "forbid"