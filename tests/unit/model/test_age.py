from app import db
from app.models import Age
import sqlalchemy as sa
from tests.unit.model.conftest import create_age


class TestAgeModelCase:
    def test_create_age(self):
        # Arrange
        year = 1
        age = create_age(year=year)

        # Act
        age_from_db = db.session.scalar(sa.select(Age).where(Age.year == age.year))

        # Assert
        assert age_from_db.year == age.year
