from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


class BigBotherAPIClient(object):

    def __init__(self):
        http_transport = RequestsHTTPTransport(
            'https://bigbother.oliviervg.com/graphql', use_json=True
        )
        self.client = Client(
            transport=http_transport, fetch_schema_from_transport=True
        )

    def list_people(self):
        query = gql('''
        query {
            allPeople {
                edges {
                    node {
                        fullName
                    }
                }
            }
        }
        ''')
        response = self.client.execute(query)
        return [
            edge['node']["fullName"] for edge in response["allPeople"]["edges"]
        ]

    def list_rooms(self):
        query = gql('''
        query {
            allRooms {
                edges {
                    node {
                        name
                        city
                    }
                }
            }
        }
        ''')
        response = self.client.execute(query)
        return [
            edge['node'] for edge in response["allRooms"]["edges"]
        ]

    def find_person(self, full_name):
        query = gql('''
        query {{
            findPerson(name: "{full_name}") {{
                fullName
                lastSeen
                room {{
                    name
                    city
                }}
            }}
        }}
        '''.format(full_name=full_name))
        response = self.client.execute(query)
        assert len(response['findPerson']) == 1, 'Person not found...'
        return response['findPerson'][0]

    def list_people_in_room(self, room_name, room_city):
        query = gql('''
        query {{
            findRoom(room: {{name: "{name}", city: "{city}"}}) {{
                people {{
                    edges {{
                        node {{
                            fullName
                            lastSeen
                        }}
                    }}
                }}
            }}
        }}
        '''.format(name=room_name, city=room_city))
        response = self.client.execute(query)
        return [
            edge['node']['fullName']
            for edge in response['findRoom']['people']['edges']
        ]

    def update_person_location(self, full_name, room_name, room_city):
        mutation = gql('''
        mutation {{
            updatePerson(input: {{fullName: "{full_name}", roomName: "{room_name}", roomCity: "{room_city}"}}) {{
                person {{
                    fullName
                    lastSeen
                    room {{
                        name
                        city
                    }}
                }}
            }}
        }}
        '''.format(full_name=full_name, room_name=room_name, room_city=room_city))
        response = self.client.execute(mutation)
        return response["updatePerson"]["person"]


def main():
    client = BigBotherAPIClient()
    print 'list_people:', client.list_people()
    print 'list_rooms:', client.list_rooms()
    print 'find_person:', client.find_person('alice springs')
    print 'list_people_in_room:', client.list_people_in_room('kitchen', 'london')
    print 'update_person_location', client.update_person_location('alice springs', 'juannex', 'london')


if __name__ == '__main__':
    main()
