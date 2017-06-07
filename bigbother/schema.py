import graphene
import datetime

from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from .models import Room as RoomModel
from .models import Person as PersonModel

from .db import Session


class RoomInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    city = graphene.String(required=True)


class Room(SQLAlchemyObjectType):

    class Meta:
        model = RoomModel
        interfaces = (relay.Node, )


class Person(SQLAlchemyObjectType):

    class Meta:
        model = PersonModel
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_rooms = SQLAlchemyConnectionField(Room)
    all_people = SQLAlchemyConnectionField(Person)

    find_room = graphene.Field(Room, room=RoomInput())
    find_person = graphene.List(Person, name=graphene.String())

    def resolve_find_room(self, args, context, info):
        session = Session()
        room = args['room']
        return session.query(
            RoomModel
        ).filter_by(name=room['name'], city=room['city']).one()

    def resolve_find_person(self, args, context, info):
        session = Session()
        return session.query(
            PersonModel
        ).filter(PersonModel.full_name.like('%{}%'.format(args['name']))).all()


class UpdatePerson(relay.ClientIDMutation):

    class Input:
        full_name = graphene.String(required=True)
        room_name = graphene.String(required=True)
        room_city = graphene.String(required=True)

    person = graphene.Field(Person)

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):
        session = Session()
        room = session.query(
            RoomModel
        ).filter_by(name=args['room_name'], city=args['room_city']).one()
        person = session.query(
            PersonModel
        ).filter_by(full_name=args['full_name']).one()
        person.room = room
        person.last_seen = datetime.datetime.utcnow()
        try:
            session.commit()
        except:
            session.rollback()
            raise
        return UpdatePerson(person=person)


class Mutation(graphene.ObjectType):
    update_person = UpdatePerson.Field()


schema = graphene.Schema(query=Query, mutation=Mutation, types=[Person, Room])
