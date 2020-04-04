from typing import Optional

from sanic import Blueprint
from sanic.request import Request
from sanic.response import json
from database import Photo, db, Assessment
from sqlalchemy.sql import func
from app.helpers.validators import raise_if_empty, raise_if_not_int, raise_if_not_float

blueprint = Blueprint('photo', url_prefix='/photo', strict_slashes=True)


@blueprint.get('')
async def get_photos(request: Request):
    limit = request.args.get('limit')
    offset = request.args.get('offset', default=0)
    raise_if_empty(limit, offset)
    raise_if_not_int(limit, offset)
    photos = limit_query(Photo.query, limit, offset)
    photos = await photos.gino.all()
    return json([photo.to_dict() for photo in photos])


@blueprint.get('/count')
async def get_count(request: Request):  # pylint: disable=unused-argument
    count, *_ = await db \
        .select([func.count(Photo.id)]) \
        .first()
    return json({'photo_count': count})


@blueprint.post('')
async def add_rating_photo(request: Request):
    photo_id = request.json.get('photo_id')
    rating = request.json.get('rating')
    raise_if_empty(photo_id, rating)
    raise_if_not_float(rating)
    await Assessment.create(
        photo_id=photo_id,
        rating=float(rating)
    )
    return json({{'status': 'ok'}})


def limit_query(query, limit: Optional[str] = None, offset: Optional[str] = None):
    if limit:
        raise_if_not_int(limit)
        query = query.limit(int(limit))
    if offset:
        raise_if_not_int(offset)
        query = query.offset(int(offset))
    return query
