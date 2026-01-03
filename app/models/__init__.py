# -*- coding: utf-8 -*-
"""
Data models for Pokedex application.
Represent domain entities according to data model.
"""
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class Usuario:
    """Represents a system user."""
    username: str
    email: str
    contrasena: str
    foto: Optional[str] = None
    esAdmin: bool = False
    aprobado: bool = False
    cuentaTelegram: Optional[str] = None


@dataclass
class Tipo:
    """Represents a Pokemon type (Fire, Water, etc.)."""
    nombreTipo: str


@dataclass
class Especie:
    """Represents a Pokemon species with base stats."""
    nombreEspecie: str
    ataque: int
    ataqueEsp: int
    def_: int  # 'def' is reserved word in Python
    defEsp: int
    vida: int
    velocidad: int
    foto: Optional[str] = None
    esLegendario: bool = False
    shiny: bool = False
    tipos: List[str] = None  # List of type names
    
    def __post_init__(self):
        if self.tipos is None:
            self.tipos = []


@dataclass
class Ataque:
    """Represents an attack that a Pokemon can learn."""
    nombreAtaque: str
    damage: int
    descripcion: Optional[str] = None
    nombreTipo: Optional[str] = None


@dataclass
class Pokemon:
    """Represents an individual Pokemon with specific stats."""
    idPokemon: Optional[int]
    nombre: str
    ataque: int
    ataqueEsp: int
    def_: int
    defEsp: int
    vel: int
    vida: int
    nombreEspecie: str
    ataques: List[str] = None  # List of attack names
    
    def __post_init__(self):
        if self.ataques is None:
            self.ataques = []


@dataclass
class Equipo:
    """Represents a Pokemon team of a user."""
    idEquipo: Optional[int]
    nombre: str
    fechaCreacion: str
    username: str
    pokemons: List[Pokemon] = None
    
    def __post_init__(self):
        if self.pokemons is None:
            self.pokemons = []


@dataclass
class Notificacion:
    """Represents a notification for a user."""
    username: str
    fecha: str
    tipo: str
    texto: Optional[str] = None


@dataclass
class Afectado:
    """Represents type effectiveness against another type."""
    afectaTipo: str
    afectadoTipo: str
    multiplo: float  # 0.5 = not very effective, 1.0 = normal, 2.0 = super effective

