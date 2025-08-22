#game/config.py
import json
import os
import sys

# As configurações começam vazias e são carregadas por uma função.

def is_running_as_exe():
    """Verifica se o programa está rodando como executável compilado"""
    return getattr(sys, 'frozen', False)

def get_base_path():
    """Retorna o caminho base apropriado"""
    if is_running_as_exe():
        # Se for executável, usa o diretório do executável
        return os.path.dirname(sys.executable)
    else:
        # Se for script, usa o diretório do projeto
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_db_path():
    """Retorna o caminho completo para o banco de dados"""
    base_path = get_base_path()
    # Para desenvolvimento: project/data/database.db
    # Para executável: dist/data/database.db
    return os.path.join(base_path, 'data', 'database.db')

def print_path_info():
    """Imprime informações de caminho para debug"""
    print("=" * 50)
    print("Informações de caminho do sistema:")
    print(f"Executável: {sys.executable}")
    print(f"Argumentos: {sys.argv}")
    print(f"Base path: {get_base_path()}")
    print(f"DB path: {get_db_path()}")
    print("=" * 50)

# Mapeamento de atributos para nomes completos
ATTR_MAP = {
    "FOR": "strength",
    "DES": "dexterity",
    "CON": "constitution",
    "INT": "intelligence",
    "SAB": "wisdom",
    "CAR": "charisma"
}

 # Classificar culturas em comuns e fantasiosas (usando minúsculas)
culturas_comuns = [
    'medieval', 'japanese', 'hispanic', 'russian', 'germany', 
    'arabic', 'nordic', 'celtic', 'chinese', 'egyptian', 
    'indian', 'african'
]

culturas_fantasiosas = [
    'darkfantasy', 'elfica', 'orc', 'anão', 'fada', 'dragao',
    'vampiro', 'lobisomem', 'mago', 'demonio'
]
DIFFICULTY_MODIFIERS = {
    "Aventura Leve": {  # Antigo "Fácil"
        "description": "Para viajantes curiosos que desejam explorar sem grandes riscos. Os inimigos são mais frágeis e as recompensas vêm em abundância.",
        "exp_multiplier": 1.25,
        "gold_multiplier": 1.5,
        "damage_received": 0.75,
        "damage_dealt": 1.1,
        "healing_received": 1.2,
        "attribute_reduction": 0,
        "monster_hp_multiplier": 0.8
    },
    "Desafio Justo": {  # Antigo "Normal"
        "description": "A forma pura da aventura: equilíbrio entre perigo e glória. Nenhuma vantagem, nenhuma pena — apenas sua coragem contra a escuridão.",
        "exp_multiplier": 1.0,
        "gold_multiplier": 1.0,
        "damage_received": 1.0,
        "damage_dealt": 1.0,
        "healing_received": 1.0,
        "attribute_reduction": 0,
        "monster_hp_multiplier": 1.0
    },
    "Provação Maldita": {  # Antigo "Difícil"
        "description": "Somente os tolos e os audaciosos escolhem este caminho. Cada golpe recebido pesa mais, cada cura vale menos. A vitória é amarga, mas gloriosa.",
        "exp_multiplier": 0.8,
        "gold_multiplier": 0.7,
        "damage_received": 1.3,
        "damage_dealt": 0.9,
        "healing_received": 0.8,
        "attribute_reduction": 2,
        "monster_hp_multiplier": 1.3
    },
    "Caminho da Dor": {  # Antigo "Hardcore"
        "description": "O aço se forja sob pressão. Aqui, cada batalha é um fardo mortal, e apenas guerreiros obstinados caminham adiante.",
        "exp_multiplier": 0.6,
        "gold_multiplier": 0.5,
        "damage_received": 1.7,
        "damage_dealt": 0.8,
        "healing_received": 0.6,
        "attribute_reduction": 4,
        "monster_hp_multiplier": 1.5
    },
    "Maldição de Ferro": {  # NOVO – para os masoquistas
        "description": "Um juramento de sangue contra a própria sobrevivência. Monstros de ferro, curas escassas e golpes devastadores. Poucos retornam.",
        "exp_multiplier": 0.5,
        "gold_multiplier": 0.4,
        "damage_received": 2.0,
        "damage_dealt": 0.75,
        "healing_received": 0.5,
        "attribute_reduction": 6,
        "monster_hp_multiplier": 2.0
    },
    "Inferno Vivo": {  # NOVO – insano
        "description": "Não é uma dificuldade, é uma sentença. Fogo eterno, inimigos cruéis e um mundo que deseja sua aniquilação. Este é o limite da loucura.",
        "exp_multiplier": 0.3,
        "gold_multiplier": 0.3,
        "damage_received": 2.5,
        "damage_dealt": 0.6,
        "healing_received": 0.4,
        "attribute_reduction": 8,
        "monster_hp_multiplier": 2.5,
        "enemy_crit_chance_bonus": 0.15  # inimigos têm mais chance de critar
    }
}



CITY_DATA = {
    "lindenrock": {
        "name": "Lindenrock",
        "description": "Uma pequena vila nas montanhas",
        "min_level": 1,
        "shops": {
            "market": [11, 12, 19],
            "blacksmith": [1, 2, 3, 4, 13]
        }
    },
    "vallengar": {
        "name": "Vallengar",
        "description": "Cidade portuária movimentada",
        "min_level": 5,
        "shops": {
            "market": [1, 2, 3],
            "shipyard": [1, 2]
        }
    }
}

locations = {
    "forest": "Floresta Sombria",
    "mountains": "Montanhas Gélidas",
    "plains": "Planícies Ventosas",
    "swamp": "Pântano Assombrado",
    "desert": "Deserto Abrasador"
}