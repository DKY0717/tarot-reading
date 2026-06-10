from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .models import Card, Spread, SpreadPosition, Reading
