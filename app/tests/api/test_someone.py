from sqlalchemy.orm import Session, aliased
from app.models import City, Country, User


def test_user(db: Session, models) -> None:
    model = aliased(User, name="user")
    user = db.query(model).filter(model.id == models.test_user.id).first()

    assert user, "User not found"
    assert user.name == "Василий Игнатыч", "Wrong user name"


def test_country(db: Session, models) -> None:
    model = aliased(Country, name="country")
    country = db.query(model).filter(model.id == models.test_country.id).first()

    assert country, "Country not found"
    assert country.name == "Interplanet Federation", "Wrong country name"
    assert country.locale == "if_IF", "Wrong country locale"


def test_update_user(db: Session, models) -> None:
    model = aliased(User, name="user")
    user = db.query(model).filter(model.id == models.test_user.id).first()
    city = City(name="Cosmopolis")

    db.add(city)
    db.commit()
    db.refresh(city)

    user.name = "Вселен Владленович"
    user.city_id = city.id

    db.add(user)
    db.commit()
    db.refresh(user)

    updated_user = db.query(model).filter(model.id == models.test_user.id).first()

    assert updated_user, "User not found"
    assert updated_user.name == "Вселен Владленович", "Wrong user name"
    assert updated_user.country_id == 15, "Wrong user name"
    assert updated_user.city_id == city.id, "Wrong user name"
