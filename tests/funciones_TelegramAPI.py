# test.py

from app.controllers import Pokedex

def test_getUserByTelegram():
    assert Pokedex.getUserByTelegram("Diego") == "user2"
    assert Pokedex.getUserByTelegram("UsuarioQueNoExiste") == None

def test_getEquipoByUser():
    equiposReal = Pokedex.getEquipoByUser("user2")
    assert len(equiposReal) == 1
    assert equiposReal[0].nombre == "BalacalaoAlPilpil"
    pokemons = equiposReal[0].pokemons
    assert len(pokemons) == 3
    chivato = False
    for pokemon in pokemons:
        if pokemon.nombreEspecie == "Voltorb":
            chivato = True
    assert chivato == True

def test_vincularUsuario():
    assert Pokedex.vincularUsuario("user2","Diego") == 1 #Ha funcionado

    assert Pokedex.vincularUsuario("UsuarioQueNoExiste","Diego") == 0 #NO ha encontrado al user "UsuarioQueNoExiste"

if __name__ == "__main__":
    print("Test 1")#Adquirir el username con el username de telegram
    test_getUserByTelegram()
    print("Test 2")#Conseguir los equipos y pokemons de un user (objetos)
    test_getEquipoByUser()
    print("Test 3")#Test de la funcion q se encarga de vincular
    test_vincularUsuario()
