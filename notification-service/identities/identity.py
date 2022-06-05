import typing as t
import os
import logging

from uuid import uuid4
import uuid
from datetime import datetime
from sqlalchemy_utils import EmailType
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy import Integer, ForeignKey, DateTime, String, Boolean

from configuration.database import db

logging.getLogger().setLevel(logging.INFO)

def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False

class Identity(db.Model):
    __tablename__ = 'user_identity'

    id = db.Column(UUID, primary_key=True, default=uuid4)

    slug = db.Column(String(32), unique=True, index=True)
    phone_number = db.Column(String(20), unique=True, nullable=True)
    email = db.Column(EmailType, unique=True)
    phone_verified = db.Column(Boolean, default=False, nullable=False)
    email_verified = db.Column(Boolean, default=False, nullable=False)
    password_hash = db.Column(String(100), default=False, nullable=False, index=True)

    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow)
    deleted_at = db.Column(DateTime, nullable=True)

    @classmethod
    async def find_by_id_or_slug(cls, user_id: t.Union[UUID, str]) -> "Identity":
        """
        Finds user identity by id or slug.

        :param user_id: user id (UUID) or user slug
        :returns: an updated user identity
        :raises: IdentityNotFoundError
        """

        query = Identity.query
        try:
            if is_valid_uuid(user_id):
                query = query.where(Identity.id == user_id)
            else:
                query = query.where(Identity.slug == user_id)
        except Exception:
            raise Exception(f"No identity with id {user_id}")

        identity = await query.gino.first()
        return identity
