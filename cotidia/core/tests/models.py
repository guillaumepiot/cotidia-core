from django.db import models

from cotidia.core.models import BaseModel
from cotidia.core.mixins import StatusModelMixin


class GenericItem(BaseModel, StatusModelMixin):
    pass
