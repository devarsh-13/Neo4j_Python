from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
user = "neo4j"
password = "12345678"


# Connect to Neo4j
driver = GraphDatabase.driver(uri, auth=(user, password))

def create_person(name):
    with driver.session() as session:
        result = session.run("CREATE (p:Person {name: $name}) RETURN id(p)", name=name)
        return result.single()[0]

def create_pet(name):
    with driver.session() as session:
        result = session.run("CREATE (p:Pet {name: $name}) RETURN id(p)", name=name)
        return result.single()[0]

def create_owns_pet_relationship(person_id, pet_id, amount):
    with driver.session() as session:
        session.run(
            "MATCH (person:Person), (pet:Pet) "
            "WHERE id(person) = $person_id AND id(pet) = $pet_id "
            "CREATE (person)-[r:OWNS_PET {amount: $amount}]->(pet)",
            person_id=person_id,
            pet_id=pet_id,
            amount=amount
        )


def get_all_pets():
    with driver.session() as session:
        result = session.run("MATCH (pet:Pet) RETURN pet.name AS name")
        return [record["name"] for record in result]

def get_all_persons():
    with driver.session() as session:
        result = session.run("MATCH (person:Person) RETURN person.name AS name")
        return [record["name"] for record in result]

def update_person_node_name(node_id, new_name):
    with driver.session() as session:
        session.run("MATCH (person:Person) WHERE id(person) = $node_id SET person.name = $new_name", node_id=node_id, new_name=new_name)

    return new_name

def update_pet_node_name(node_id, new_name):
    with driver.session() as session:
        session.run("MATCH (pet:Pet) WHERE id(pet) = $node_id SET pet.name = $new_name", node_id=node_id, new_name=new_name)

    return new_name

def delete_person_node(node_id):
    with driver.session() as session:
        session.run("MATCH (person:Person) WHERE id(person) = $node_id DETACH DELETE person", node_id=node_id)

    return node_id

def delete_pet_node(node_id):
    with driver.session() as session:
        session.run("MATCH (pet:Pet) WHERE id(pet) = $node_id DETACH DELETE pet", node_id=node_id)

    return node_id

if __name__ == "__main__":

    person_id = create_person("Jake")
    pet_id = create_pet("Cat")

    amount_of_pet = 2000  # For example, indicating ownership strength
    create_owns_pet_relationship(person_id, pet_id, amount_of_pet)
    print("Created 'OWNS_PET' relationship with amount:", amount_of_pet)

    pets = get_all_pets()
    print("All Pets:", pets)

    persons = get_all_persons()
    print("All Persons:", persons)

    new_person_name = update_person_node_name(0, "John")
    print("Person node updated with new name:", new_person_name)

    
    new_pet_name = update_pet_node_name(1, "Dog")
    print("Pet node updated with new name:", new_pet_name)

    person_id =  delete_person_node(2)
    print("Pet node deleted with ID:", person_id)

    pet_id =  delete_pet_node(3)
    print("Pet node deleted with ID:", pet_id)