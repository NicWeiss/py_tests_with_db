import yaml

from typing import TypeVar
from sqlalchemy.orm import Session

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)


class YamlToDB:

    def __init__(self, yaml_path: str, models_path: str, db: Session) -> None:
        setattr(self, 'db', db)

        with open(yaml_path, 'r') as ymlfile:
            raw_models = []
            models_from_yaml = yaml.safe_load(ymlfile)

            for allias, data in models_from_yaml.items():
                model_allias = allias
                model_class_name = data[0]
                model_data = {}

                for field, value in data[1].items():
                    model_data[f"{field}"] = value

                if model_data.get('id', None) is None:
                    raise ValueError(f"Missing id in {model_allias} model")

                m = __import__(models_path, fromlist=[model_class_name])
                model_class = m.__dict__[model_class_name]
                model = model_class(**model_data)
                setattr(self, model_allias, model)
                raw_models.append((model_class, model))

            setattr(self, 'models', raw_models)

    def _get_model_by_id(self, model_class: ModelType, id: int) -> ModelType:
        return self.db.query(model_class).get(id)

    def _delete_model(self, model: ModelType) -> ModelType:
        self.db.delete(model)
        self.db.commit()

    def prepare(self):
        for model_class, model in self.models[::-1]:
            if hasattr(model, 'id') and model.id is not None:
                db_object = self._get_model_by_id(model_class, model.id)
                if db_object:
                    self._delete_model(db_object)

    def save_all(self):
        for model_class, model in self.models:
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)

    def cleanup(self):
        for _, model in self.models[::-1]:
            try:
                self.db.delete(model)
                self.db.commit()
            except Exception:
                pass
