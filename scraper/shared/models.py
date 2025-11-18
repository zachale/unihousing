from typing import Optional, Union, List
from pydantic import BaseModel, field_validator


class Listing(BaseModel):
    """
    Shared Listing model used across the backend.
    All fields are optional because scraped data is not always complete.
    """

    listing_id: Optional[str] = None 
    id: Optional[str] = None         

    # Basic listing details
    headline: Optional[str] = None
    address: Optional[str] = None
    price: Optional[str] = None
    description: Optional[str] = None
    photos: Optional[List[str]] = None

    # Amenities
    no_smoking: Optional[bool] = None
    laundry_facilities: Optional[bool] = None
    parking: Optional[bool] = None
    cooking_facilities: Optional[bool] = None

    # Misc fields
    category: Optional[str] = None
    date_available: Optional[str] = None
    date_posted: Optional[str] = None

    shared: Optional[Union[str, bool]] = None
    sublet: Optional[Union[str, bool]] = None

    beds: Optional[str] = None

    # Scraper checksum fields
    check_sum_json: Optional[int] = None
    check_sum_description: Optional[int] = None