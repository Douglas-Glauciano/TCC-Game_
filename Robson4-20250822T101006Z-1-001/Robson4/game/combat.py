import random
import time
from prettytable import PrettyTable
from .character import Character
from .monster import Monster
from .db_queries import load_monsters_by_level, add_item_to_inventory, remove_item_from_inventory
from .utils import modifier, roll_dice, get_display_name, calculate_enhanced_damage, calculate_enhanced_armor_bonus
from .config import DIFFICULTY_MODIFIERS
from .database import delete_character

class Combat:
    def __init__(self, player: Character, db_connection, stdscr):
        self.player = player
        self.conn = db_connection
        self.stdscr = stdscr
        self.difficulty_modifiers = DIFFICULTY_MODIFIERS.get(player.difficulty, DIFFICULTY_MODIFIERS["Desafio Justo"])
        self.monster = self.generate_monster()
        self.permadeath_active = player.permadeath
        self.combat_log = []
        player.recalculate()
        self.add_to_log(f"Um {self.monster.name} selvagem aparece!")

    def add_to_log(self, message):
        """Adiciona mensagem ao log de combate"""
        self.combat_log.append(message)
        # Mantém apenas as últimas 10 mensagens
        if len(self.combat_log) > 10:
            self.combat_log = self.combat_log[-10:]

    def generate_monster(self) -> Monster:
        """Gera um monstro apropriado para o nível do jogador."""
        valid_monsters = load_monsters_by_level(self.conn, self.player.level)

        if not valid_monsters:
            self.add_to_log("Aviso: Nenhum monstro válido encontrado no DB. Usando um Rato Gigante como padrão.")
            return Monster(
                name="Rato Gigante", 
                level=1, 
                hp_max=10, 
                ac=10, 
                damage_dice="1d4", 
                exp_reward=5, 
                gold_dice="1d2",
                attack_type="physical"
            )

        monster_data = random.choice(valid_monsters)
        
        # Aplicar o multiplicador de HP do monstro com base na dificuldade
        hp_max = int(monster_data.get('hp', 10) * self.difficulty_modifiers.get("monster_hp_multiplier", 1.0))
        ac = monster_data.get('ac', 10)
        
        return Monster(
            name=monster_data['name'],
            level=monster_data['level'],
            hp_max=hp_max,
            ac=ac,
            attack_bonus=monster_data.get('attack_bonus', 0),
            damage_dice=monster_data['damage_dice'],
            exp_reward=monster_data['exp_reward'],
            gold_dice=monster_data['gold_dice'],
            strength=monster_data.get('strength', 10),
            dexterity=monster_data.get('dexterity', 10),
            constitution=monster_data.get('constitution', 10),
            intelligence=monster_data.get('intelligence', 10),
            wisdom=monster_data.get('wisdom', 10),
            charisma=monster_data.get('charisma', 10),
            main_attack_attribute=monster_data.get('main_attack_attribute', 'strength'),
            attack_type=monster_data.get('attack_type', 'physical'),
            physical_resistance=monster_data.get('physical_resistance', 0),
            magical_resistance=monster_data.get('magical_resistance', 0)
        )
    
    def get_status_tables(self):
        """Retorna tabelas formatadas com status do jogador e monstro"""
        # Tabela do jogador
        player_table = PrettyTable()
        player_table.field_names = [f"👤 {self.player.name} [Lvl {self.player.level}]", "Valor"]
        player_table.align = "l"
        player_table.border = False
        player_table.header = False
        
        player_hp_percent = min(100, int((self.player.hp / self.player.hp_max) * 100))
        hp_bar = f"[{'█' * (player_hp_percent // 5)}{'░' * (20 - (player_hp_percent // 5))}] {player_hp_percent}%"
        
        player_table.add_row(["❤️ Vida", f"{self.player.hp}/{self.player.hp_max} {hp_bar}"])
        
        if self.player.mana_max > 0:
            mana_percent = min(100, int((self.player.mana / self.player.mana_max) * 100))
            mana_bar = f"[{'▓' * (mana_percent // 5)}{'░' * (20 - (mana_percent // 5))}] {mana_percent}%"
            player_table.add_row(["🔷 Mana", f"{self.player.mana}/{self.player.mana_max} {mana_bar}"])
        
        player_table.add_row(["🛡️ Armadura", f"{self.player.ac}"])
        player_table.add_row(["🛡️ Resistência Física", f"{self.player.physical_resistance}"])
        player_table.add_row(["✨ Resistência Mágica", f"{self.player.magical_resistance}"])
        player_table.add_row(["⚠️ Penalidade Destreza", f"-{self.player.dexterity_penalty}"])

        # Tabela do monstro
        monster_table = PrettyTable()
        monster_table.field_names = [f"👹 {self.monster.name} [Lvl {self.monster.level}]", "Valor"]
        monster_table.align = "l"
        monster_table.border = False
        monster_table.header = False
        
        monster_hp_percent = min(100, int((self.monster.hp / self.monster.hp_max) * 100))
        monster_hp_bar = f"[{'█' * (monster_hp_percent // 5)}{'░' * (20 - (monster_hp_percent // 5))}] {monster_hp_percent}%"
        
        monster_table.add_row(["❤️ Vida", f"{self.monster.hp}/{self.monster.hp_max} {monster_hp_bar}"])
        monster_table.add_row(["🛡️ Armadura", f"{self.monster.ac}"])
        monster_table.add_row(["🛡️ Resistência Física", f"{self.monster.physical_resistance}"])
        monster_table.add_row(["✨ Resistência Mágica", f"{self.monster.magical_resistance}"])
        monster_table.add_row(["⚔️ Tipo de Ataque", f"{self.monster.attack_type}"])

        return player_table, monster_table

    def player_attack(self):
        """Ataque do jogador com feedback melhorado."""
        self.player.recalculate()
        attack_roll, critical, dice_roll = self.player.attack()
        
        self.add_to_log(f"Sua rolagem de ataque: {attack_roll} (Dado: {dice_roll} + Bônus: {attack_roll - dice_roll})")

        if critical:
            self.add_to_log("⚡ CRÍTICO! Dano dobrado!")

        if attack_roll >= self.monster.ac or critical:
            damage, damage_type = self.player.calculate_damage(critical)
            
            # Aplica modificador de dificuldade ao dano causado pelo jogador
            damage = int(damage * self.difficulty_modifiers.get("damage_dealt", 1.0))
            
            # Adicione o dano critico se o inimigo tiver chance de critico
            if critical and "enemy_crit_chance_bonus" in self.difficulty_modifiers:
                damage += damage * 0.15

            # Aplica a resistência do monstro ao dano
            if damage_type == "physical":
                damage_after_resistance = max(1, damage - self.monster.physical_resistance)
            else:
                damage_after_resistance = max(1, damage - self.monster.magical_resistance)
                
            # Reduz o HP do monstro
            self.monster.hp -= damage_after_resistance
            
            # Exibe informações detalhadas
            self.add_to_log(f"🔥 Você acerta o {self.monster.name} causando {damage_after_resistance} de dano {damage_type}!")
            
            if damage > damage_after_resistance:
                resistance_value = damage - damage_after_resistance
                self.add_to_log(f"  🛡️ Resistência do monstro reduziu {resistance_value} de dano!")
            
            # Verifica se o monstro morreu
            return self.monster.hp <= 0
        else:
            self.add_to_log(f"Você erra o ataque! O {self.monster.name} tinha {self.monster.ac} de AC.")
            return False

    def monster_attack(self):
        """Ataque do monstro com feedback visual aprimorado."""
        # Se houver chance de crítico extra para inimigos, aplica aqui
        crit_bonus_chance = self.difficulty_modifiers.get("enemy_crit_chance_bonus", 0)
        is_crit_bonus_active = random.random() < crit_bonus_chance

        attack_roll, critical, dice_roll = self.monster.attack()
        attack_bonus = attack_roll - dice_roll

        # Verifica se o crítico adicional foi ativado
        if is_crit_bonus_active:
            critical = True

        self.add_to_log(f"\n{self.monster.name} ataca!")
        self.add_to_log(f"Rolagem do monstro: {dice_roll} (dado) + {attack_bonus} (bônus) = {attack_roll}")

        if critical:
            self.add_to_log("☠️  CRÍTICO DO MONSTRO! Você sente a dor profunda!")

        if attack_roll >= self.player.ac or critical:
            # O monstro calcula o dano (sem tipo, pois o tipo já está definido)
            raw_damage = self.monster.calculate_damage(critical)
            
            # Aplica modificador de dificuldade ao dano recebido pelo jogador
            modified_damage = int(raw_damage * self.difficulty_modifiers.get("damage_received", 1.0))
            
            # O jogador toma dano com o tipo correto
            is_player_dead, actual_damage, damage_reduced = self.player.take_damage(
                modified_damage, 
                self.monster.attack_type
            )
            
            self.add_to_log(f"💥 O ataque ACERTOU!")
            self.add_to_log(f"  Tipo de dano: {self.monster.attack_type}")
            self.add_to_log(f"  Dano bruto: {modified_damage}")
            
            if damage_reduced > 0:
                self.add_to_log(f"  🛡️ Sua resistência reduziu {damage_reduced} de dano!")
                
            self.add_to_log(f"  Dano efetivo: {actual_damage}")
            return is_player_dead
        else:
            self.add_to_log(f"🛡️ O ataque ERROU!")
            self.add_to_log(f"  Sua AC: {self.player.ac}")
            self.add_to_log(f"  Ataque necessário: {self.player.ac} (rolagem: {attack_roll})")
            return False
            
    def attempt_flee(self):
        """Tentativa de fuga com teste de destreza."""
        self.add_to_log("\nVocê tenta fugir...")

        self.player.recalculate()
        
        player_roll = roll_dice("1d20") + modifier(self.player.get_effective_intelligence())
        monster_roll = roll_dice("1d20") + modifier(self.monster.dexterity)

        self.add_to_log(f"Seu teste de fuga: {player_roll} vs. Teste do monstro: {monster_roll}")

        if player_roll > monster_roll:
            return True
        else:
            self.add_to_log("A fuga falhou! O monstro bloqueia seu caminho!")
            return False

    def get_random_item(self):
        """Retorna um item aleatório apropriado para o nível do jogador."""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM items 
            WHERE category IN ('weapon', 'armor', 'shield', 'consumable', 'misc')
            ORDER BY RANDOM() 
            LIMIT 1
        ''')
        item = cursor.fetchone()
        if not item:
            return None
            
        columns = [column[0] for column in cursor.description]
        return dict(zip(columns, item))
    
    def lose_random_item(self):
        """Remove um item aleatório do inventário do jogador."""
        inventory = self.player.get_inventory()
        unequipped_items = [item for item in inventory if item.get('quantity', 0) > 0]

        if not unequipped_items:
            self.add_to_log("\nVocê não tem itens na mochila para perder!")
            return
            
        item_to_lose = random.choice(unequipped_items)
        success = remove_item_from_inventory(self.conn, item_to_lose['inventory_id'], quantity=1)
        
        if success:
            self.add_to_log(f"\n⚠️ Você perdeu '{get_display_name(item_to_lose)}' durante a batalha!")
        else:
            self.add_to_log(f"\nNão foi possível remover '{get_display_name(item_to_lose)}' do seu inventário.")

    def victory(self):
        """Recompensas por vitória com itens aleatórios."""
        exp_earned = int(self.monster.exp_reward * self.difficulty_modifiers.get("exp_multiplier", 1.0))
        base_gold = self.monster.get_gold_reward()
        gold_earned = int(base_gold * self.difficulty_modifiers.get("gold_multiplier", 1.0))

        self.add_to_log(f"\nO {self.monster.name} desaba sem vida. A vitória é sua.")
        self.add_to_log(f"\n❤️ Vida: {self.player.hp}/{self.player.hp_max}")
        if self.player.mana_max > 0:
            self.add_to_log(f"🔷 Mana: {self.player.mana}/{self.player.mana_max}")
        
        self.add_to_log(f"🛡️ Resistência Física: {self.player.physical_resistance}")
        self.add_to_log(f"✨ Resistência Mágica: {self.player.magical_resistance}")
 
        self.add_to_log(f"\n📦 Recompensas:")
        self.add_to_log(f"✦ EXP Ganha: +{exp_earned}")
        self.add_to_log(f"🪙 Ouro Encontrado: +{gold_earned}")

        if random.random() < 0.4:
            item_base_data = self.get_random_item()
            if item_base_data:
                try:
                    add_item_to_inventory(self.conn, self.player.id, item_base_data['id'], quantity=1, enhancement_level=0, enhancement_type=None)
                    self.add_to_log(f"🎁 Item Encontrado: '{get_display_name(item_base_data)}'!")
                except Exception as e:
                    self.add_to_log(f"ERRO ao adicionar item: {str(e)}")
            else:
                self.add_to_log("Nenhum item encontrado.")
        else:
            self.add_to_log("Nenhum item encontrado.")

        self.player.gain_exp(exp_earned)
        self.player.gold += gold_earned
        
        from game.db_queries import update_character_gold
        update_character_gold(self.conn, self.player.id, self.player.gold)

        self.player.recalculate()

    def defeat(self):
        """Derrota com perda de itens e tratamento de permadeath."""
        self.add_to_log(f"\n☠ Você foi derrotado...")
        self.add_to_log(f"☠ Sua visão escurece enquanto o {self.monster.name} ruge em triunfo.")

        # Verifica se o modo permadeath está ativo (0 para não, 1 para sim)
        if self.player.permadeath == 1:
            self.player.hp = 0
            self.add_to_log(f"\n☠☠☠ A MORTE É PERMANENTE! ☠☠☠")
            self.add_to_log(f"☠ Seu personagem {self.player.name} será apagado para sempre.")
            
            success = delete_character(self.conn, self.player.id)
            
            if success:
                self.add_to_log("Personagem deletado com sucesso do banco de dados.")
            else:
                self.add_to_log("Houve um erro ao deletar o personagem do banco de dados.")
                
            return True
        else:
            if random.random() < 0.3:
                self.lose_random_item()
            
            # Multiplicador de cura recebida também afeta a cura ao ser derrotado
            recovery_hp = int(self.player.hp_max * 0.1 * self.difficulty_modifiers.get("healing_received", 1.0))
            self.player.hp = max(1, recovery_hp)
            
            self.player.recalculate()
            
            self.add_to_log(f"\nPor um triz, você sobrevive e acorda horas depois, com o corpo dolorido.")
        
        return False # Retorna False se o personagem não tiver permadeath