from typing import Any, Dict, Tuple

ALLOWED_SORT_FIELDS = {"title", "director", "genre", "year", "rating"}
ALLOWED_SORT_ORDERS = {"asc", "desc"}

def parse_query_params(args: Dict[str, Any]) -> Tuple[Dict[str, Any], int, int, str, str]:
    filters: Dict[str, Any] = {}

    for key in ["title", "director", "genre"]:
        value = args.get(key)
        if value:
            filters[key] = str(value)

    year = args.get("year")
    if year:
        try:
            filters["year"] = int(year)
        except (ValueError, TypeError):
            raise ValueError("Year must be an integer")

    rating = args.get("rating")
    if rating:
        try:
            filters["rating"] = float(rating)
        except (ValueError, TypeError):
            raise ValueError("Rating must be a float")

    # Valid pagination parameters
    try:
        limit = int(args.get("limit", 10))
        offset = int(args.get("offset", 0))
    except (ValueError, TypeError):
        raise ValueError("Limit and offset must be integers")

    sort_by = str(args.get("sort_by", "title"))
    if sort_by not in ALLOWED_SORT_FIELDS:
        raise ValueError(f"Invalid sort_by field. Allowed values: {', '.join(ALLOWED_SORT_FIELDS)}")

    order = str(args.get("order", "asc")).lower()
    if order not in ALLOWED_SORT_ORDERS:
        raise ValueError("Invalid order. Allowed values are 'asc' or 'desc'")

    return filters, limit, offset, sort_by, order
