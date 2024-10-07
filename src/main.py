from database import database
from models import models


models.Base.metadata.create_all(bind=database.engine) # create tbales

