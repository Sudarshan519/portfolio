from fastapi import HTTPException
from sqlmodel import SQLModel


class RecordService(SQLModel):
    @classmethod
    def by_id(cls, id: int, session):
        obj = session.get(cls, id)
        if obj is None:
            raise HTTPException(status_code=404, detail=f"{cls.__name__} with id {id} not found")
        return obj

    @classmethod
    def all(cls, session):
        return session. query(cls).limit(100).all()

    @classmethod
    def create(cls, source: dict  , SQLModel, session):
        if isinstance(source, SQLModel):
            obj = cls.from_orm(source)
        elif isinstance(source, dict):
            obj = cls.parse_obj(source)
        session.add(obj)
        session.commit()
        session.refresh(obj)
 
        return obj

    def save(self, session):
        session.add(self)
        session.commit()
        session.refresh(self)

    def update(self, source: dict| SQLModel, session):
        if isinstance(source, SQLModel):
            source = source.dict(exclude_unset=True)

        for key, value in source.items():
            setattr(self, key, value)
        self.save(session)

    def delete(self, session):
        session.delete(self)
        session.commit()

