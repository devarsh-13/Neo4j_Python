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

def display_menu():
    print("Menu:")
    print("1. Create a Person")
    print("2. Create a Pet")
    print("3. Establish ownership relationship")
    print("4. Get all Pets")
    print("5. Get all Persons")
    print("6. Update a Person's name")
    print("7. Update a Pet's name")
    print("8. Delete a Person")
    print("9. Delete a Pet")
    print("0. Exit")
    print()

def main():
    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            person_name = input("Enter the name of the person: ")
            person_id = create_person(person_name)
            print("Person created with ID:", person_id)
        elif choice == '2':
            pet_name = input("Enter the name of the pet: ")
            pet_id = create_pet(pet_name)
            print("Pet created with ID:", pet_id)
        elif choice == '3':
            person_id = int(input("Enter the ID of the person: "))
            pet_id = int(input("Enter the ID of the pet: "))
            amount_of_pet = int(input("Enter the amount of pet: "))
            create_owns_pet_relationship(person_id, pet_id, amount_of_pet)
            print("Established 'OWNS_PET' relationship with amount:", amount_of_pet)
        elif choice == '4':
            pets = get_all_pets()
            print("All Pets:", pets)
        elif choice == '5':
            persons = get_all_persons()
            print("All Persons:", persons)
        elif choice == '6':
            node_id = int(input("Enter the ID of the person to update: "))
            new_name = input("Enter the new name for the person: ")
            new_person_name = update_person_node_name(node_id, new_name)
            print("Person node updated with new name:", new_person_name)
        elif choice == '7':
            node_id = int(input("Enter the ID of the pet to update: "))
            new_name = input("Enter the new name for the pet: ")
            new_pet_name = update_pet_node_name(node_id, new_name)
            print("Pet node updated with new name:", new_pet_name)
        elif choice == '8':
            node_id = int(input("Enter the ID of the person to delete: "))
            deleted_person_id = delete_person_node(node_id)
            print("Person node deleted with ID:", deleted_person_id)
        elif choice == '9':
            node_id = int(input("Enter the ID of the pet to delete: "))
            deleted_pet_id = delete_pet_node(node_id)
            print("Pet node deleted with ID:", deleted_pet_id)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()