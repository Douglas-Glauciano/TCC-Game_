import random
import re
import os
import json
import time

def roll_dice(dice_str):
    """Rola dados no formato 'XdY+Z'"""
    match = re.match(r"(\d+)d(\d+)([+-]\d+)?", dice_str)
    if not match:
        print(f"[WARN] Formato de dado inválido: {dice_str}. Retornando 0.")
        return 0
        
    num = int(match.group(1))
    sides = int(match.group(2))
    modifier = int(match.group(3)) if match.group(3) else 0
    
    total = sum(random.randint(1, sides) for _ in range(num)) + modifier
    return total

def roll_d6():
    """Rola um dado de 6 faces"""
    return random.randint(1, 6)

def roll_attribute():
    """Rola um atributo usando o sistema 4d6 (descarta o menor)"""
    rolls = [roll_d6() for _ in range(4)]
    rolls.sort(reverse=True)
    return sum(rolls[:3])  # Soma os 3 maiores valores

def modifier(score):
    """Calcula modificador de atributo"""
    return (score - 10) // 2

def roll_dice_max(dice_str):
    """Retorna o valor máximo possível para um dado"""
    match = re.match(r"(\d+)d(\d+)([+-]\d+)?", dice_str)
    if not match:
        print(f"[WARN] Formato de dado inválido para max: {dice_str}. Retornando 0.")
        return 0
        
    num = int(match.group(1))
    sides = int(match.group(2))
    modifier_val = int(match.group(3)) if match.group(3) else 0 # Renomeado para evitar conflito
    
    return (num * sides) + modifier_val

def rows_to_dicts(cursor):
    """Converte os resultados de uma consulta SQL em dicionários"""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def get_display_name(item):
    """Retorna o nome do item com informações de melhoria"""
    name = item['name']
    
    enhancement_level = item.get('enhancement_level', 0)
    enhancement_type = item.get('enhancement_type')
    
    if enhancement_level > 0:
        name += f" +{enhancement_level}"
    
    if enhancement_type:
        # Adiciona um emoji baseado no tipo de melhoria
        type_emojis = {
            'fire': '🔥',
            'ice': '❄️',
            'lightning': '⚡',
            'poison': '☠️',
            'holy': '✨',
            'sharp': '🔪',
            'durable': '🛡️',
            'lucky': '🍀',
            'normal': ''
        }
        emoji = type_emojis.get(enhancement_type, '')
        name += f" {emoji}"
    
    return name

def calculate_enhanced_value(item):
    """Calcula o valor aprimorado do item"""
    base_value = item.get('value', 0)
    enhancement_level = item.get('enhancement_level', 0)
    
    # Valor aumenta 50% por nível de melhoria
    return int(base_value * (1 + 0.5 * enhancement_level))

def calculate_enhanced_damage(item):
    """Calcula o dano aprimorado para armas"""
    base_dice = item.get('damage_dice', '1d4')
    enhancement_level = item.get('enhancement_level', 0)
    
    # Para armas: cada nível de aprimoramento adiciona +1 de dano fixo
    # e +1d2 nos níveis ímpares (1, 3, 5)
    bonus_dice = ""
    
    # Adiciona dados de dano extra para níveis ímpares
    for level in range(1, enhancement_level + 1):
        if level % 2 == 1:  # Níveis ímpares
            if bonus_dice:
                bonus_dice += f"+1d{2 * level}"
            else:
                bonus_dice = f"1d{2 * level}"
    
    # Combina o dano base com os bônus
    if bonus_dice:
        return f"{base_dice}+{bonus_dice}"
    
    return base_dice

def calculate_enhanced_resistances(item):
    """Calcula as resistências aprimoradas para armaduras."""
    phys_res = item.get('physical_resistance', 0)
    mag_res = item.get('magical_resistance', 0)
    enhancement_level = item.get('enhancement_level', 0)
    
    # Cada nível de aprimoramento aumenta ambas as resistências em 1
    return {
        'physical_resistance': phys_res + enhancement_level,
        'magical_resistance': mag_res + enhancement_level
    }

def calculate_enhanced_armor_bonus(item):
    """Calcula o bônus de armadura aprimorado para escudos"""
    base_bonus = item.get('armor_bonus', 0)
    enhancement_level = item.get('enhancement_level', 0)
    
    # Cada nível de aprimoramento adiciona +1 ao bônus de armadura
    return base_bonus + enhancement_level

def calculate_attack_bonus(item):
    """Calcula o bônus de ataque para armas aprimoradas"""
    enhancement_level = item.get('enhancement_level', 0)
    
    # Para armas: cada nível par de aprimoramento adiciona +1 de bônus de ataque
    attack_bonus = 0
    for level in range(1, enhancement_level + 1):
        if level % 2 == 0:  # Níveis pares
            attack_bonus += 1
    
    return attack_bonus

def can_enhance(item):
    """Verifica se um item pode ser melhorado"""
    return item.get('category') in ['weapon', 'armor', 'shield']

# game/utils.py
def is_weapon(item):
    return item.get('category') == 'weapon'

def is_armor(item):
    return item.get('category') == 'armor'

def is_shield(item):
    return item.get('category') == 'shield'