"""
Defining sql models in line with the fastapi documentation. This model
is not a pydantic model, but a sqlalchemy model.
"""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from cml_auth.database.database import Base
