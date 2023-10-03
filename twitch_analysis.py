from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
user = "neo4j"
password = "12345678"

# Connect to Neo4j
driver = GraphDatabase.driver(uri, auth=(user, password))
#get all users
def get_all_users():
    with driver.session() as session:
        result = session.run("MATCH (u:User) RETURN u.name AS name LIMIT 25")
        return [record["name"] for record in result]

# get streamers with highest followers.
def get_users_with_highest_followers():

    with driver.session() as session:

        result = session.run("MATCH (u:User) WHERE u.followers IS NOT NULL RETURN u.name AS name, u.followers AS followers  ORDER BY followers DESC LIMIT 25")
        return [dict(record) for record in result]
    

#  get all languages
def get_all_languages():
    with driver.session() as session:
        result = session.run("MATCH (l:Language) RETURN l.name AS name")
        return [record["name"] for record in result]

# get recommended game by streamer
def get_user_game_preference(user_name):
    with driver.session() as session:
        result = session.run("""
            MATCH (u:User {name: $user_name})-[:PLAYS]->(g:Game)
            RETURN g.name as name
            ORDER BY rand()
            LIMIT 10;
        """, user_name=user_name)
        return [record["name"] for record in result]

# get popular languages
def get_popular_language():
    with driver.session() as session:
        result = session.run("""
            MATCH (s:Stream)-[:HAS_LANGUAGE]->(l:Language)
            RETURN l.name AS language, COUNT(s) AS stream_count
            ORDER BY stream_count DESC;
        """)
        return [dict(record) for record in result]

# get Moderators of a Streamer
def get_moderators_of_streamer(user_name):
    with driver.session() as session:
        result = session.run("""
            MATCH (u:User {name: $user_name})<-[:MODERATOR]-(m:User)
            RETURN m.name AS moderator_name
        """, user_name=user_name)
        return [record["moderator_name"] for record in result]
    
#get team info
def get_team_info():
    with driver.session() as session:
        result = session.run("""
            MATCH (t:Team)<-[:HAS_TEAM]-(u:User)
            OPTIONAL MATCH (u)-[:PLAYS]->(g:Game)
            WHERE u.followers IS NOT NULL
            WITH t, u, g, SUM(u.followers) AS total_followers
            ORDER BY total_followers DESC
            WITH t, COLLECT(DISTINCT { name: u.name, followers: u.followers }) AS team_members, COLLECT(DISTINCT g.name) AS games_played, total_followers
            RETURN t.name AS team_name, team_members, games_played, total_followers
            ORDER BY total_followers DESC LIMIT 3
        """)
        return [dict(record) for record in result]
#get stramer for a game
def get_streams_for_game(game_name):
    with driver.session() as session:
        result = session.run("""
            MATCH (g:Game {name: $game_name})<-[:PLAYS]-(s:Stream)
            WHERE s.followers IS NOT NULL
            RETURN g.name AS game_name, COLLECT(DISTINCT s.name) AS streams
        """, game_name=game_name)
        return [dict(record) for record in result]
    
def display_menu():
    print("\nMenu:")
    print("1.get all users")
    print("2.get users with highest followers")
    print("3.get all languages")
    print("4.get recommonded game by streamer")
    print("5.get populer languages used by streamers")
    print("6.get moderator of a streamer")
    print("7.get team info by total followers")
    print("8.get streams by game")

    print()

def main():
    while True:
        display_menu()

        choice = input("Enter your choice: ")

        if choice == '1':
            result = get_all_users()
            print(result)
            
        elif choice == '2':
            result = get_users_with_highest_followers()
            print(result)

        elif choice == '3':
            result = get_all_languages()
            print(result)

        elif choice == '4':
            name = input("Enter streamer name: ")
            result = get_user_game_preference(name)
            print(result)

        elif choice == '5':
        
            result = get_popular_language()
            print(result)

        elif choice == '6':
            name = input("Enter streamer name: ")
            result = get_moderators_of_streamer(name)
            print(result)

        elif choice == '7':
            result = get_team_info()
            print(result)

        elif choice == '8':
            name = input("Enter game name:")
            result =  get_streams_for_game(name)
            print(result)



if __name__ == "__main__":
    main()