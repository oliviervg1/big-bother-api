import graphene

from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from models import Room as RoomModel
from models import Person as PersonModel

from db import Session


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


class UpdatePerson(relay.ClientIDMutation):

    class Input:
        name = graphene.String(required=True)
        city = graphene.String(required=True)

    person = graphene.Field(Person)

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):
        name = args['name']
        city = args['city']
        return UpdatePerson(name=name, city=city)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_rooms = SQLAlchemyConnectionField(Room)
    all_people = SQLAlchemyConnectionField(Person)

    room = graphene.Field(Room, room=RoomInput())
    person = graphene.List(Person, name=graphene.String())

    def resolve_room(self, args, context, info):
        session = Session()
        room = args['room']
        return session.query(
            RoomModel
        ).filter_by(name=room['name'], city=room['city']).one()

    def resolve_person(self, args, context, info):
        session = Session()
        return session.query(
            PersonModel
        ).filter(PersonModel.full_name.like('%{}%'.format(args['name']))).all()


schema = graphene.Schema(query=Query, types=[Person, Room])
