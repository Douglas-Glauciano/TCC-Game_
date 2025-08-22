def populate_races(conn, insert_race):
    """Popula a tabela de raças com descrições mais profundas"""
    races = [
        ("Humano", 0, 0, 0, 0, 0, 0,
        "Versáteis e resilientes, os humanos são a raça que molda o mundo à sua imagem. Podem se destacar em qualquer profissão ou classe, com sociedades complexas, cidades prósperas e uma curiosidade insaciável que os leva à aventura."),

        ("Elfo", -1, +2, -1, +2, +1, 0,
        "Seres graciosos e longevos, os elfos vivem em sintonia com a natureza e a magia. Suas sociedades são repletas de arte, música e sabedoria antiga. Dotados de visão aguçada e agilidade sobrenatural, raramente são surpreendidos, mas tendem à melancolia devido à sua longevidade."),

        ("Anão", +2, -1, +2, 0, +1, -1,
        "Robustos e resistentes, os anões são mestres artesãos e guerreiros inflexíveis. Suas fortalezas subterrâneas guardam riquezas e segredos ancestrais. Orgulhosos e teimosos, prezam pela honra e pelo trabalho árduo, sendo aliados leais e inimigos formidáveis."),

        ("Orc", +3, 0, +2, -2, -1, -2,
        "Ferocidade e força definem os orcs. Vivem em tribos guerreiras e cultivam um código de bravura e sobrevivência. Apesar de sua reputação brutal, muitos orcs possuem honra própria e laços de família fortes. Em batalha, são imprevisíveis e devastadores."),

        ("Halfling", -2, +3, 0, 0, +2, +1,
        "Pequenos e ágeis, os halflings possuem uma sorte notável e uma disposição alegre. Suas aldeias são comunidades unidas, e eles se destacam em furtividade, arrombamentos e viagens discretas. Frequentemente subestimados, são surpreendentemente corajosos quando a situação exige."),

        ("Draconato", +2, 0, +1, 0, 0, +2,
        "Descendentes diretos dos dragões, os draconatos exalam imponência. Orgulhosos, leais e guiados por códigos de honra ancestrais, possuem habilidades mágicas e um sopro elemental devastador. São símbolos de poder e tradição em qualquer sociedade que integrem."),

        ("Tiefling", 0, +1, -1, +2, 0, +2,
        "Marcados por herança infernal, os tieflings enfrentam preconceito e desconfiança. Inteligentes e carismáticos, usam sua astúcia e magia para prosperar em mundos que muitas vezes os rejeitam. São mestres em persuasão, manipulação e sobrevivência urbana."),

        ("Goblin", -2, +3, 0, +1, 0, -1,
        "Astutos e ágeis, os goblins vivem de truques e estratégias rápidas. Preferem emboscadas, armadilhas e táticas de guerrilha. Apesar de sua pequena estatura, sua inteligência coletiva e senso de oportunidade os torna inimigos inesperadamente perigosos."),

        ("Gigante", +4, -2, +3, -3, -2, -2,
        "Herança dos titãs, os gigantes são colossais, fortes e resistentes. Seu tamanho impõe respeito, mas muitas vezes sofrem em ambientes sociais e estratégicos. Costumam ter culturas próprias, ligadas à natureza e à força bruta, venerando forças ancestrais."),

        ("Fada", -3, +4, -2, +2, +3, +2,
        "Seres encantados de magia sutil, as fadas possuem inteligência e carisma excepcionais, embora sejam fisicamente frágeis. Vivem em sociedades místicas, guardando segredos arcanos e manipulando acontecimentos com sutileza, encanto e astúcia."),

        ("Súcubo/Íncubo", 0, +1, -2, 0, 0, +4,
        "Demônios sedutores, mestres da manipulação emocional. Sua beleza e carisma são armas, mas sua fragilidade física exige astúcia e estratégia. Vivem em sombras, influenciando acontecimentos e corações à distância."),

        ("Autômato", +1, 0, +2, +1, -2, -3,
        "Criaturas mecânicas de civilizações antigas, programadas para precisão e eficiência. Sem emoções humanas, são resistentes e capazes de suportar condições extremas, mas carecem de intuição ou empatia, tornando sua interação social complicada."),

        ("Meio-Orc", +2, 0, +1, -1, 0, 0,
        "Filhos de duas culturas distintas, os meio-orcs mesclam força e adaptabilidade. Frequentemente marginalizados, desenvolvem resiliência, coragem e habilidades de sobrevivência excepcionais, tornando-se guerreiros formidáveis e diplomatas inesperados."),

        ("Meio-Elfo", 0, +1, 0, +1, +1, +1,
        "Combinam a sensibilidade, graça e magia dos elfos com a adaptabilidade humana. Meio-elfos transitam entre mundos, frequentemente se tornando embaixadores, bardos ou aventureiros, capazes de unir diferentes culturas com charme e inteligência."),
    ]
    
    for race in races:
        insert_race(conn, *race)


def populate_monsters(conn, insert_monster, Monster):
    # (name, level, hp_max, ac, damage_dice, exp_reward, gold_dice, str, dex, con, int, wis, cha, main_attr, attack_type, physical_resistance, magical_resistance, description)
    monsters_data = [
        ("Rato Gigante", 1, 10, 12, "1d4", 5, "1d2", 4, 10, 6, 1, 2, 1, "dexterity", "physical", 1, 1,
        "Um rato enorme e agressivo, comum em masmorras."),
        
        ("Esqueleto", 2, 15, 13, "1d6", 12, "1d4", 10, 8, 10, 2, 3, 1, "strength", "physical", 3, 1,
        "Um esqueleto reanimado que vaga sem rumo."),
        
        ("Goblin", 2, 12, 14, "1d6", 15, "1d6", 6, 14, 8, 4, 3, 2, "dexterity", "physical", 1, 1,
        "Criatura pequena e astuta, gosta de emboscadas."),
        
        ("Zumbi", 3, 25, 10, "1d8", 20, "1d4", 14, 4, 14, 1, 1, 0, "constitution", "physical", 5, 2,
        "Cadáver reanimado, lento mas resistente."),
        
        ("Lobo", 3, 20, 14, "1d6", 18, "1d6", 10, 14, 10, 2, 3, 4, "dexterity", "physical", 2, 1,
        "Lobo selvagem que ataca em bando."),
        
        ("Batedor Kobold", 4, 22, 15, "1d6", 25, "1d6", 8, 16, 8, 3, 4, 3, "dexterity", "physical", 1, 1,
        "Kobold ágil especializado em emboscadas."),
        
        ("Slime Ácido", 4, 30, 8, "1d6", 28, "1d4", 6, 6, 14, 1, 1, 0, "constitution", "magical", 8, 1,
        "Massa gelatinosa que dissolve tudo que toca."),
        
        ("Bandido", 5, 40, 12, "1d8", 30, "2d4", 12, 12, 10, 6, 6, 8, "strength", "physical", 2, 2,
        "Criminoso humano que assalta viajantes."),
        
        ("Feiticeiro Caótico", 6, 35, 11, "1d10", 40, "2d6", 4, 8, 6, 16, 10, 12, "intelligence", "magical", 1, 5,
        "Um mago imprevisível e perigoso."),
        
        ("Arqueiro Sombrio", 6, 45, 15, "1d8", 42, "2d6", 8, 16, 10, 8, 8, 6, "dexterity", "physical", 3, 2,
         "Atirador furtivo especializado em ataques à distância."),
        
        ("Urso Pardo", 7, 60, 13, "1d10", 50, "2d4", 18, 10, 14, 2, 3, 2, "strength", "physical", 4, 2,
        "Urso enorme e agressivo que protege seu território."),
        
        ("Espírito Atormentado", 7, 50, 11, "1d8", 48, "1d8", 4, 12, 6, 10, 16, 10, "wisdom", "magical", 1, 6,
        "Alma perdida cheia de dor e raiva."),
        
        ("Golem de Pedra", 8, 80, 16, "2d6", 60, "1d10", 20, 6, 18, 1, 1, 0, "constitution", "physical", 10, 1,
        "Construto gigante feito de pedra, extremamente resistente."),
        
        ("Súcubo", 8, 55, 12, "1d8", 65, "2d8", 6, 14, 8, 10, 12, 18, "charisma", "magical", 2, 7,
        "Demônio sedutor que manipula vítimas com charme."),
        
        ("Aranha Gigante", 9, 65, 16, "2d6", 70, "2d6", 12, 18, 10, 1, 6, 2, "dexterity", "physical", 3, 3,
        "Aranha enorme, venenosa e ágil."),
        
        ("Cavaleiro Negro", 10, 85, 17, "2d8", 80, "3d6", 18, 10, 16, 6, 6, 4, "strength", "physical", 7, 4,
        "Guerreiro sombrio montado em cavalo negro."),
        
        ("Draconato Selvagem", 11, 100, 15, "2d10", 95, "3d8", 16, 12, 16, 8, 6, 6, "constitution", "magical", 5, 8,
        "Dragão humanoide selvagem e perigoso."),
        
        ("Lich", 12, 90, 14, "3d6", 110, "3d10", 6, 10, 10, 20, 18, 16, "intelligence", "magical", 2, 10,
        "Mago morto-vivo com poderes arcanos devastadores."),
        
        ("Quimera", 13, 120, 15, "3d8", 130, "4d6", 20, 14, 18, 6, 6, 6, "strength", "physical", 6, 6,
        "Monstro híbrido com múltiplas cabeças e ataques variados."),
        
        ("Dragão Vermelho Jovem", 14, 150, 18, "3d10", 150, "5d6", 22, 16, 20, 10, 12, 18, "constitution", "magical", 8, 8,
        "Dragão jovem, feroz e cuspidor de fogo.")
    ]
    
    for data in monsters_data:
        monster = Monster(
            name=data[0],
            level=data[1],
            hp_max=data[2],
            ac=data[3],
            damage_dice=data[4],
            exp_reward=data[5],
            gold_dice=data[6],
            strength=data[7],
            dexterity=data[8],
            constitution=data[9],
            intelligence=data[10],
            wisdom=data[11],
            charisma=data[12],
            main_attack_attribute=data[13],
            attack_type=data[14],
            physical_resistance=data[15],
            magical_resistance=data[16],
            description=data[17]
        )
        insert_monster(conn, monster)
        print(f"{monster.name} - HP: {monster.hp_max}, AC: {monster.ac}, Atk: +{monster.attack_bonus}, Resistência Física: {monster.physical_resistance}, Resistência Mágica: {monster.magical_resistance}")


def populate_components(conn, insert_component):
    components = [
        # conn, culture, gender, component_type, value, weight=1, is_required=0):
        ('medieval', 'masc', 'prefix', 'Sir', 1, 1),
        ('medieval', 'masc', 'prefix', 'Lord', 1, 1),
        ('medieval', 'fem', 'prefix', 'Lady', 1, 1),
        ('medieval', 'fem', 'prefix', 'Dame', 1, 1),
        ('medieval', 'neutro', 'prefix', 'The', 1, 1),
        
        # Partes do meio (opcionais)
        ('medieval','unisex', 'middle', 'von', 1, 0),
        ('medieval','unisex', 'middle', 'de', 1, 0),
        ('medieval','unisex', 'middle', 'of', 1, 0),
        
        # Sufixos obrigatórios
        ('medieval', 'masc', 'suffix', 'bert', 1, 1),
        ('medieval', 'masc', 'suffix', 'win', 1, 1),
        ('medieval', 'fem', 'suffix', 'gwen', 1, 1),
        ('medieval', 'fem', 'suffix', 'wynn', 1, 1),
        ('medieval', 'neutro', 'suffix', 'wood', 1, 1),
        

        # Cultura japanese
        ('japanese', 'masc', 'prefix', 'Tak', 1, 1),
        ('japanese', 'fem', 'prefix', 'Yuki', 1, 1),
        ('japanese', 'neutro', 'prefix', 'Kai', 1, 1),

        ('japanese','unisex', 'middle', 'no', 1, 0),  # partícula comum em títulos antigos (ex: Aoi no Ue)

        ('japanese', 'masc', 'suffix', 'hiro', 1, 1),
        ('japanese', 'fem', 'suffix', 'ko', 1, 1),
        ('japanese', 'neutro', 'suffix', 'sora', 1, 1),


        # Cultura hispânica
        ('Hispanic', 'masc', 'prefix', 'Don', 1, 1),
        ('Hispanic', 'fem', 'prefix', 'Doña', 1, 1),
        ('Hispanic', 'neutro', 'prefix', 'El', 1, 1),

        ('Hispanic','unisex', 'middle', 'del', 1, 0),
        ('Hispanic','unisex', 'middle', 'de la', 1, 0),

        ('Hispanic', 'masc', 'suffix', 'quez', 1, 1),
        ('Hispanic', 'fem', 'suffix', 'dia', 1, 1),
        ('Hispanic', 'neutro', 'suffix', 'ado', 1, 1),


        # Cultura russian
        ('russian', 'masc', 'prefix', 'Ivan', 1, 1),
        ('russian', 'fem', 'prefix', 'Anya', 1, 1),
        ('russian', 'neutro', 'prefix', 'Niko', 1, 1),

        ('russian','unisex', 'middle', 'ovich', 1, 0),
        ('russian','unisex', 'middle', 'ovna', 1, 0),

        ('russian', 'masc', 'suffix', 'sky', 1, 1),
        ('russian', 'fem', 'suffix', 'ska', 1, 1),
        ('russian', 'neutro', 'suffix', 'ov', 1, 1),


        # Cultura germany
        ('germany', 'masc', 'prefix', 'Herr', 1, 1),
        ('germany', 'fem', 'prefix', 'Frau', 1, 1),
        ('germany', 'neutro', 'prefix', 'Meister', 1, 1),

        ('germany','unisex', 'middle', 'von', 1, 0),
        ('germany','unisex', 'middle', 'zum', 1, 0),

        ('germany', 'masc', 'suffix', 'rich', 1, 1),
        ('germany', 'fem', 'suffix', 'linde', 1, 1),
        ('germany', 'neutro', 'suffix', 'stein', 1, 1),


        # Cultura árabe
        ('arabic', 'masc', 'prefix', 'Malik', 1, 1),
        ('arabic', 'fem', 'prefix', 'Zahra', 1, 1),
        ('arabic', 'neutro', 'prefix', 'Amir', 1, 1),

        ('arabic','unisex', 'middle', 'al', 1, 0),
        ('arabic','unisex', 'middle', 'ibn', 1, 0),  # filho de

        ('arabic', 'masc', 'suffix', 'ad-din', 1, 1),  # "da fé"
        ('arabic', 'fem', 'suffix', 'rahma', 1, 1),    # "misericórdia"
        ('arabic', 'neutro', 'suffix', 'mir', 1, 1),


        # Cultura nórdica
        ('nordic', 'masc', 'prefix', 'Bjorn', 1, 1),
        ('nordic', 'fem', 'prefix', 'Astrid', 1, 1),
        ('nordic', 'neutro', 'prefix', 'Eira', 1, 1),

        ('nordic','unisex', 'middle', 'son of', 1, 0),
        ('nordic','unisex', 'middle', 'shield of', 1, 0),

        ('nordic', 'masc', 'suffix', 'son', 1, 1),    # filho de
        ('nordic', 'fem', 'suffix', 'dottir', 1, 1),  # filha de
        ('nordic', 'neutro', 'suffix', 'heim', 1, 1), # lar

        # Cultura celta
        ('celtic', 'masc', 'prefix', 'Aed', 1, 1),
        ('celtic', 'fem', 'prefix', 'Niamh', 1, 1),
        ('celtic', 'neutro', 'prefix', 'Bran', 1, 1),

        ('celtic','unisex', 'middle', 'mac', 1, 0),  # filho de
        ('celtic','unisex', 'middle', 'of the Glen', 1, 0),

        ('celtic', 'masc', 'suffix', 'an', 1, 1),
        ('celtic', 'fem', 'suffix', 'wyn', 1, 1),
        ('celtic', 'neutro', 'suffix', 'dhu', 1, 1),

        # Cultura chinesa
        ('chinese', 'masc', 'prefix', 'Wei', 1, 1),
        ('chinese', 'fem', 'prefix', 'Mei', 1, 1),
        ('chinese', 'neutro', 'prefix', 'Li', 1, 1),

        ('chinese','unisex', 'middle', 'of the Jade', 1, 0),

        ('chinese', 'masc', 'suffix', 'long', 1, 1),
        ('chinese', 'fem', 'suffix', 'hua', 1, 1),
        ('chinese', 'neutro', 'suffix', 'shan', 1, 1),

        # Cultura egípcia antiga
        ('egyptian', 'masc', 'prefix', 'Set', 1, 1),
        ('egyptian', 'fem', 'prefix', 'Nefer', 1, 1),
        ('egyptian', 'neutro', 'prefix', 'Khepri', 1, 1),

        ('egyptian','unisex', 'middle', 'sa', 1, 0),  # filho de

        ('egyptian', 'masc', 'suffix', 'hotep', 1, 1),
        ('egyptian', 'fem', 'suffix', 'tari', 1, 1),
        ('egyptian', 'neutro', 'suffix', 'khamun', 1, 1),

        # Cultura indiana (hindustani)
        ('indian', 'masc', 'prefix', 'Raj', 1, 1),
        ('indian', 'fem', 'prefix', 'Laxmi', 1, 1),
        ('indian', 'neutro', 'prefix', 'Devi', 1, 1),

        ('indian','unisex', 'middle', 'bin', 1, 0),

        ('indian', 'masc', 'suffix', 'deep', 1, 1),
        ('indian', 'fem', 'suffix', 'mala', 1, 1),
        ('indian', 'neutro', 'suffix', 'esh', 1, 1),

        # Cultura africana (inspirada em Bantu/Iorubá)
        ('african', 'masc', 'prefix', 'Kwame', 1, 1),
        ('african', 'fem', 'prefix', 'Zola', 1, 1),
        ('african', 'neutro', 'prefix', 'Oba', 1, 1),

        ('african','unisex', 'middle', 'ya', 1, 0),

        ('african', 'masc', 'suffix', 'bayo', 1, 1),
        ('african', 'fem', 'suffix', 'lina', 1, 1),
        ('african', 'neutro', 'suffix', 'diba', 1, 1),

        # Fantasia sombria
        ('darkfantasy', 'masc', 'prefix', 'Mor', 1, 1),
        ('darkfantasy', 'fem', 'prefix', 'Lil', 1, 1),
        ('darkfantasy', 'neutro', 'prefix', 'Ash', 1, 1),

        ('darkfantasy','unisex', 'middle', 'of the Void', 1, 0),

        ('darkfantasy', 'masc', 'suffix', 'grim', 1, 1),
        ('darkfantasy', 'fem', 'suffix', 'shade', 1, 1),
        ('darkfantasy', 'neutro', 'suffix', 'mourn', 1, 1),



        ('elven', 'masc', 'prefix', 'Elar', 1, 1),
        ('elven', 'masc', 'prefix', 'Faer', 1, 1),
        ('elven', 'fem',  'prefix', 'Aera', 1, 1),
        ('elven', 'fem',  'prefix', 'Luth', 1, 1),
        ('elven', 'neutro', 'prefix', 'Sil', 1, 1),

        # Meio (opcional)
        ('elven','unisex', 'middle', 'thal', 1, 0),
        ('elven','unisex', 'middle', 'mir', 1, 0),
        ('elven','unisex', 'middle', 'iel', 1, 0),

        # Sufixos obrigatórios
        ('elven', 'masc', 'suffix', 'ion', 1, 1),
        ('elven', 'fem',  'suffix', 'wyn', 1, 1),
        ('elven', 'neutro', 'suffix', 'riel', 1, 1),

        ### ANÃO ###
        ('dwarf', 'masc', 'prefix', 'Thrain', 1, 1),
        ('dwarf', 'masc', 'prefix', 'Bald', 1, 1),
        ('dwarf', 'fem',  'prefix', 'Grun', 1, 1),
        ('dwarf', 'fem',  'prefix', 'Dora', 1, 1),
        ('dwarf', 'neutro', 'prefix', 'Stone', 1, 1),

        ('dwarf','unisex', 'middle', 'rock', 1, 0),
        ('dwarf','unisex', 'middle', 'brew', 1, 0),
        ('dwarf','unisex', 'middle', 'forge', 1, 0),

        ('dwarf', 'masc', 'suffix', 'in', 1, 1),
        ('dwarf', 'fem',  'suffix', 'a', 1, 1),
        ('dwarf', 'neutro', 'suffix', 'grum', 1, 1),

        ### ORC ###
        ('orc', 'masc', 'prefix', 'Gor', 1, 1),
        ('orc', 'masc', 'prefix', 'Maug', 1, 1),
        ('orc', 'fem',  'prefix', 'Urza', 1, 1),
        ('orc', 'fem',  'prefix', 'Grash', 1, 1),
        ('orc', 'neutro', 'prefix', 'Krug', 1, 1),

        ('orc','unisex', 'middle', 'nak', 1, 0),
        ('orc','unisex', 'middle', 'zar', 1, 0),
        ('orc','unisex', 'middle', 'mog', 1, 0),

        ('orc', 'masc', 'suffix', 'thar', 1, 1),
        ('orc', 'fem',  'suffix', 'ka', 1, 1),
        ('orc', 'neutro', 'suffix', 'nagh', 1, 1),

        ### VAMPÍRICO ###
        ('vampire', 'masc', 'prefix', 'Val', 1, 1),
        ('vampire', 'masc', 'prefix', 'Luc', 1, 1),
        ('vampire', 'fem',  'prefix', 'Sel', 1, 1),
        ('vampire', 'fem',  'prefix', 'Lil', 1, 1),
        ('vampire', 'neutro', 'prefix', 'Noct', 1, 1),

        ('vampire','unisex', 'middle', 'drak', 1, 0),
        ('vampire','unisex', 'middle', 'von', 1, 0),
        ('vampire','unisex', 'middle', 'al', 1, 0),

        ('vampire', 'masc', 'suffix', 'ar', 1, 1),
        ('vampire', 'fem',  'suffix', 'ira', 1, 1),
        ('vampire', 'neutro', 'suffix', 'an', 1, 1),

        ### DRACÔNICO ###
        ('draconic', 'masc', 'prefix', 'Zar', 1, 1),
        ('draconic', 'masc', 'prefix', 'Thra', 1, 1),
        ('draconic', 'fem',  'prefix', 'Myth', 1, 1),
        ('draconic', 'fem',  'prefix', 'Xyra', 1, 1),
        ('draconic', 'neutro', 'prefix', 'Vyr', 1, 1),

        ('draconic','unisex', 'middle', 'ga', 1, 0),
        ('draconic','unisex', 'middle', 'zor', 1, 0),
        ('draconic','unisex', 'middle', 'rax', 1, 0),

        ('draconic', 'masc', 'suffix', 'gon', 1, 1),
        ('draconic', 'fem',  'suffix', 'thys', 1, 1),
        ('draconic', 'neutro', 'suffix', 'mir', 1, 1),

         ### HALFLING ###
        # Prefixos obrigatórios
        ('halfling', 'masc', 'prefix', 'Bil', 1, 1),
        ('halfling', 'masc', 'prefix', 'Tob', 1, 1),
        ('halfling', 'fem',  'prefix', 'Mira', 1, 1),
        ('halfling', 'fem',  'prefix', 'Penny', 1, 1),
        ('halfling', 'neutro', 'prefix', 'Wig', 1, 1),

        # Meio (opcional)
        ('halfling','unisex', 'middle', 'bur', 1, 0),
        ('halfling','unisex', 'middle', 'leef', 1, 0),
        ('halfling','unisex', 'middle', 'plop', 1, 0),

        # Sufixos obrigatórios
        ('halfling', 'masc', 'suffix', 'o', 1, 1),
        ('halfling', 'fem',  'suffix', 'a', 1, 1),
        ('halfling', 'neutro', 'suffix', 'berry', 1, 1),

        ### TIEFLING ###
        ('tiefling', 'masc', 'prefix', 'Az', 1, 1),
        ('tiefling', 'masc', 'prefix', 'Rhaz', 1, 1),
        ('tiefling', 'fem',  'prefix', 'Zera', 1, 1),
        ('tiefling', 'fem',  'prefix', 'Nyx', 1, 1),
        ('tiefling', 'neutro', 'prefix', 'Vex', 1, 1),

        ('tiefling','unisex', 'middle', 'kar', 1, 0),
        ('tiefling','unisex', 'middle', 'vul', 1, 0),
        ('tiefling','unisex', 'middle', 'shar', 1, 0),

        ('tiefling', 'masc', 'suffix', 'ius', 1, 1),
        ('tiefling', 'fem',  'suffix', 'ira', 1, 1),
        ('tiefling', 'neutro', 'suffix', 'eth', 1, 1),

        ### succubus / INCUBUS ###
        ('succubus', 'masc', 'prefix', 'Amon', 1, 1),
        ('succubus', 'masc', 'prefix', 'Laz', 1, 1),
        ('succubus', 'fem',  'prefix', 'Lil', 1, 1),
        ('succubus', 'fem',  'prefix', 'Sava', 1, 1),
        ('succubus', 'neutro', 'prefix', 'Des', 1, 1),

        ('succubus','unisex', 'middle', 'vel', 1, 0),
        ('succubus','unisex', 'middle', 'ira', 1, 0),
        ('succubus','unisex', 'middle', 'lux', 1, 0),

        ('succubus', 'masc', 'suffix', 'an', 1, 1),
        ('succubus', 'fem',  'suffix', 'ia', 1, 1),
        ('succubus', 'neutro', 'suffix', 'is', 1, 1),

        ### AUTÔMATO ###
        ('automaton', 'masc', 'prefix', 'Unit-', 1, 1),
        ('automaton', 'masc', 'prefix', 'MK-', 1, 1),
        ('automaton', 'fem',  'prefix', 'Model-', 1, 1),
        ('automaton', 'fem',  'prefix', 'Proto-', 1, 1),
        ('automaton', 'neutro', 'prefix', 'AX-', 1, 1),

        ('automaton','unisex', 'middle', 'B7', 1, 0),
        ('automaton','unisex', 'middle', 'X9', 1, 0),
        ('automaton','unisex', 'middle', '0Z', 1, 0),

        ('automaton', 'masc', 'suffix', '42', 1, 1),
        ('automaton', 'fem',  'suffix', '21', 1, 1),
        ('automaton', 'neutro', 'suffix', '001', 1, 1),
        ]
    for comp in components:
        # Desempacota os valores da tupla e passa para a função
        insert_component(conn, *comp)

def populate_weapons(conn, insert_item):
    weapons_data = [
        # ID, Name, Weight, Value, Damage Dice, Damage Type,
        # Weapon Type, Two Handed, Main Attribute, Level, Description

        # ===== Nível 1–2 =====
        (1, "Espada Curta", 2.5, 30, "1d6", "physical", "one_handed", False, "strength", 1,
        "Espada leve e versátil"),

        (2, "Adaga", 0.5, 20, "1d4", "physical", "one_handed", False, "dexterity", 1,
        "Pequena e fácil de ocultar"),

        (3, "Arco Curto", 2.0, 60, "1d6", "physical", "bow", False, "dexterity", 1,
        "Arco leve para ataques rápidos"),
        
        (4, "Lança", 2.5, 40, "1d6", "physical", "two_handed", False, "strength", 2,
        "Arma de alcance médio"),

        (5, "Maça Simples", 3.0, 35, "1d6", "physical", "one_handed", False, "strength", 2,
        "Arma contundente básica"),

        (6, "Clava Reforçada", 3.2, 45, "1d8", "physical", "one_handed", False, "strength", 2,
        "Clava pesada feita de madeira reforçada"),

        # ===== Nível 3–4 =====
        (7, "Espada Longa", 4.0, 80, "1d10", "physical", "two_handed", True, "strength", 3,
        "Espada de duas mãos"),

        (8, "Rapieira", 1.5, 70, "1d8", "physical", "one_handed", False, "dexterity", 3,
        "Arma elegante e veloz"),

        (9, "Besta de Mão", 1.8, 90, "1d6", "physical", "crossbow", False, "dexterity", 3,
        "Arma de fogo leve e portátil"),

        (10, "Martelo de Guerra", 5.5, 130, "1d10", "physical", "two_handed", True, "strength", 4,
        "Martelo de impacto poderoso"),

        (11, "Arco Longo", 2.5, 100, "1d8", "physical", "bow", True, "dexterity", 4,
        "Alcance elevado e boa precisão"),

        (12, "Machado Duplo", 4.8, 120, "1d10", "physical", "two_handed", True, "strength", 4,
        "Machado de batalha de duas lâminas"),

        # ===== Nível 5–6 (Mágico/Avançado) =====
        (13, "Varinha de Fogo", 1.0, 150, "1d10", "magical", "wand", False, "intelligence", 5,
        "Dispara rajadas de fogo"),

        (14, "Cajado de Gelo", 2.0, 180, "1d8", "magical", "staff", False, "intelligence", 5,
        "Convoca ventos congelantes"),

        (15, "Espada Flamejante", 3.5, 200, "2d6", "magical", "one_handed", False, "strength", 5,
        "Espada com lâmina envolta em chamas"),

        (16, "Chicote Espinhoso", 2.0, 120, "1d8", "physical", "one_handed", False, "dexterity", 5,
        "Ataques em área curta"),

        (17, "Varinha Elétrica", 1.2, 200, "1d12", "magical", "wand", False, "intelligence", 6,
        "Conduz energia elétrica"),

        (18, "Espada Bastarda", 4.5, 180, "1d10", "physical", "two_handed", True, "strength", 6,
        "Pesada, mas eficaz"),

        (19, "Lança Longa", 3.5, 160, "1d10", "physical", "two_handed", True, "strength", 6,
        "Perfurante de longo alcance"),

        (20, "Arco Recurvo", 2.8, 140, "1d10", "physical", "bow", True, "dexterity", 6,
        "Arco otimizado para impacto"),

        # ===== Nível 7+ (Elite/Mágico) =====
        (21, "Espada Rúnica", 3.8, 300, "2d8", "magical", "one_handed", False, "strength", 7,
        "Arma encantada com runas antigas"),

        (22, "Martelo Celestial", 6.0, 350, "2d6", "magical", "two_handed", True, "strength", 7,
        "Forjado com poder divino"),

        (23, "Arco Sombrio", 2.5, 280, "1d12", "magical", "bow", True, "dexterity", 8,
        "Arco corrompido com energia das sombras"),

        (24, "Cajado Cósmico", 3.0, 400, "2d10", "magical", "staff", False, "intelligence", 8,
        "Canaliza magia pura do éter"),

        (25, "Lâmina Etérea", 3.2, 500, "2d12", "magical", "one_handed", False, "dexterity", 9,
        "Uma espada feita de energia etérea pura"),
    ]

    for w in weapons_data:
        item_dict = {
            'id': w[0],
            'name': w[1],
            'category': 'weapon',
            'equip_slot': 'main_hand',
            'level': w[9],
            'description': w[10],
            'weight': w[2],
            'value': w[3],
            'damage_dice': w[4],
            'damage_type': w[5],
            'weapon_type': w[6],
            'two_handed': w[7],
            'main_attribute': w[8]
        }
        insert_item(conn, item_dict)



def populate_armors_and_shields(conn, insert_item):
    # Armaduras agora têm: physical_resistance, magical_resistance, dexterity_penalty
    armors_data = [
    # ID, Name, Description, Weight, Value,
    # Physical Res, Magical Res, Dex Penalty,
    # Armor Class, Strength Req, Slot, Level

    # ====== NÍVEL 1 - Kit Leve: Couro Básico ======
    (101, "Elmo de Couro", "Proteção simples para a cabeça", 2.0, 10, 1, 0, 0, "light", 0, "head", 1),
    (102, "Armadura de Couro", "Proteção básica de couro", 10.0, 25, 2, 0, 0, "light", 0, "body", 1),
    (103, "Luvas de Couro", "Luvas simples e flexíveis", 0.5, 5, 1, 0, 0, "light", 0, "hands", 1),
    (104, "Botas de Couro", "Botas leves para movimentação rápida", 1.0, 10, 1, 0, 0, "light", 0, "feet", 1),

    # ====== NÍVEL 2 - Kit Médio: Malha Flexível ======
    (105, "Elmo de Malha", "Proteção de anéis entrelaçados", 3.0, 20, 2, 1, 1, "medium", 8, "head", 2),
    (106, "Camisa de Malha", "Cota de malha para o torso", 20.0, 50, 4, 1, 2, "medium", 10, "body", 2),
    (107, "Manoplas de Malha", "Luvas resistentes com boa mobilidade", 1.0, 15, 2, 1, 1, "medium", 9, "hands", 2),
    (108, "Botas de Malha", "Botas de couro com reforço de malha", 2.0, 20, 2, 1, 1, "medium", 8, "feet", 2),

    # ====== NÍVEL 3 - Kit Leve: Roupas Místicas ======
    (109, "Chapéu Arcano", "Chapéu de tecido com proteção mágica", 0.5, 30, 0, 2, 0, "light", 0, "head", 3),
    (110, "Robe Místico", "Roupas reforçadas com encantamentos", 2.0, 0, 0, 3, 0, "light", 0, "body", 3),
    (111, "Luvas Arcanas", "Melhoram o controle de feitiços", 0.3, 40, 0, 2, 0, "light", 0, "hands", 3),
    (112, "Sandálias Élficas", "Permitem movimentos silenciosos", 0.7, 50, 0, 1, 0, "light", 0, "feet", 3),

    # ====== NÍVEL 4 - Kit Médio: Escamas Negras ======
    (113, "Elmo de Escamas", "Feito de escamas endurecidas", 4.0, 50, 3, 1, 2, "medium", 11, "head", 4),
    (114, "Cota de Escamas", "Armadura resistente e articulada", 45.0, 75, 2, 2, 0, "medium", 11, "body", 4),
    (115, "Manoplas de Escamas", "Bom equilíbrio entre força e flexibilidade", 2.0, 30, 1, 1, 2, "medium", 10, "hands", 4),
    (116, "Botas de Escamas", "Reforçadas, ideais para terrenos difíceis", 3.0, 35, 3, 1, 2, "medium", 10, "feet", 4),

    # ====== NÍVEL 5 - Kit Pesado: Armadura Real ======
    (117, "Elmo Real", "Elmo ornamentado e resistente", 5.0, 150, 4, 1, 3, "heavy", 14, "head", 5),
    (118, "Armadura de Placas", "Cobertura completa de placas metálicas", 65.0, 1500, 8, 3, 5, "heavy", 15, "body", 5),
    (119, "Manoplas de Guerra", "Protegem mãos e braços", 3.0, 120, 3, 2, 3, "heavy", 13, "hands", 5),
    (120, "Grevas de Titânio", "Botas pesadas e resistentes", 4.0, 100, 3, 2, 3, "heavy", 13, "feet", 5),
    ]

    for a in armors_data:
        item_dict = {
            'id': a[0],
            'name': a[1],
            'category': 'armor',
            'equip_slot': a[10],
            'level': a[11],
            'description': a[2],
            'weight': a[3],
            'value': a[4],
            'physical_resistance': a[5],
            'magical_resistance': a[6],
            'dexterity_penalty': a[7],
            'armor_class': a[8],
            'strength_requirement': a[9]
        }
        insert_item(conn, item_dict)

    # Escudos mantêm armor_bonus
    shields_data = [
        # id, name, description, weight, value, 
        # armor_bonus, strength_requirement, level
        (201, "Escudo de Madeira", "Escudo básico de madeira",
        6.0, 10, 1, 0, 1),
        
        (202, "Escudo de Aço", "Escudo resistente de aço temperado",
        10.0, 50, 2, 11, 2),
        
        (203, "Broquel", "Pequeno escudo para duelos",
        3.0, 40, 1, 0, 1),
    ]

    for s in shields_data:
        item_dict = {
            'id': s[0],
            'name': s[1],
            'category': 'shield',
            'equip_slot': 'off_hand',
            'level': s[7],
            'description': s[2],
            'weight': s[3],
            'value': s[4],
            'armor_bonus': s[5],
            'strength_requirement': s[6]
        }
        insert_item(conn, item_dict)

def populate_classes(conn, insert_class):
    classes_data = [
        # Formato: (name, hit_dice, mana_dice, base_ac, description, starting_weapon_id, starting_armor_id)
        ("Guerreiro", "1d10", "1d2", 10, "Mestre em combate corpo a corpo.", 1, 114),
        ("Bárbaro", "1d12", "1d2", 11, "Guerreiro selvagem e brutal.", 2, 114),
        ("Paladino", "1d10", "1d4", 10, "Combina fé e força para proteger aliados.", 7, 118),
        
        ("Mago", "1d6", "1d8", 10, "Conjurador de feitiços arcanos.", 6, 110),
        ("Feiticeiro", "1d6", "1d8", 10, "Domina magias de destruição elementar.", 11, 110),
        ("Clérigo", "1d8", "1d6", 10, "Canaliza poderes divinos para curar ou punir.", 9, 106),

        ("Ladrão", "1d8", "1d4", 11, "Ágil e furtivo.", 5, 102),
        ("Arqueiro", "1d8", "1d4", 11, "Especialista em combate à distância.", 4, 102),
        ("Caçador", "1d8", "1d6", 11, "Rastreador e domador da natureza.", 3, 106),
    ]
    
    for char_class in classes_data:
        insert_class(conn, *char_class)
    print("Classes populadas.")

def populate_skills(conn, insert_skills):
    SKILLS_DATA = [
        # FORÇA (6)
        {"name": "Atletismo", "description": "Capacidade de correr, saltar e escalar obstáculos.", "attribute": "FOR"},
        {"name": "Briga", "description": "Combate corpo a corpo desarmado usando socos, chutes e agarramentos.", "attribute": "FOR"},
        {"name": "Armas de Uma Mão", "description": "Habilidade com espadas, machados e maças empunhadas com uma só mão.", "attribute": "FOR"},
        {"name": "Armas de Duas Mãos", "description": "Domínio de grandes armas como espadas longas, maças de guerra e montantes.", "attribute": "FOR"},
        {"name": "Armaduras Médias", "description": "Combate eficiente usando armaduras de malha e couro batido.", "attribute": "FOR"},


        # DESTREZA (9)
        {"name": "Acrobacia", "description": "Realizar manobras ágeis, saltos e manter equilíbrio em situações adversas.", "attribute": "DES"},
        {"name": "Furtividade", "description": "Mover-se silenciosamente e permanecer oculto de inimigos.", "attribute": "DES"},
        {"name": "Prestidigitação", "description": "Habilidade manual para truques, furtos e manipulação de objetos.", "attribute": "DES"},
        {"name": "Fechaduras", "description": "Abrir fechaduras e desarmar mecanismos de segurança.", "attribute": "DES"},
        {"name": "Arquearia", "description": "Precisão com arcos tradicionais e recurvos.", "attribute": "DES"},
        {"name": "Bestas", "description": "Manejo eficiente de bestas de todos os tipos.", "attribute": "DES"},
        {"name": "Esquiva", "description": "Evitar ataques com movimentos ágeis e reflexos rápidos.", "attribute": "DES"},
        {"name": "Iniciativa", "description": "Reagir rapidamente ao perigo, determinando vantagem tática.", "attribute": "DES"},
        {"name": "Armaduras Leves", "description": "Combate eficiente usando armaduras de couro e tecido reforçado.", "attribute": "DES"},  # Nova perícia

        # CONSTITUIÇÃO (3)
        {"name": "Resiliência", "description": "Resistir a venenos, doenças e condições físicas extremas.", "attribute": "CON"},
        {"name": "Armaduras Pesadas", "description": "Movimentação e combate usando armaduras de placas e malha pesada.", "attribute": "CON"},  # Nova perícia
        {"name": "Escudos", "description": "Capacidade de bloquear e desviar ataques usando escudos.", "attribute": "CON"},  # Nova perícia

        # INTELIGÊNCIA (5)
        {"name": "Arcanismo", "description": "Conhecimento de magias, itens mágicos e entidades sobrenaturais.", "attribute": "INT"},
        {"name": "História", "description": "Saber sobre eventos passados, reinos antigos e culturas perdidas.", "attribute": "INT"},
        {"name": "Natureza", "description": "Conhecimento de flora, fauna e ecossistemas naturais.", "attribute": "INT"},
        {"name": "Engenharia", "description": "Criar e reparar dispositivos mecânicos e estruturas complexas.", "attribute": "INT"},
        {"name": "Investigação", "description": "Encontrar pistas, resolver enigmas e desvendar mistérios.", "attribute": "INT"},

        # SABEDORIA (5)
        {"name": "Percepção", "description": "Notar detalhes sutis, sons baixos e ameaças ocultas.", "attribute": "SAB"},
        {"name": "Intuição", "description": "Perceber intenções ocultas e ler situações sociais complexas.", "attribute": "SAB"},
        {"name": "Sobrevivência", "description": "Navegar em ambientes selvagens, encontrar recursos e evitar perigos naturais.", "attribute": "SAB"},
        {"name": "Medicina", "description": "Tratar ferimentos, diagnosticar doenças e aplicar primeiros socorros.", "attribute": "SAB"},
        {"name": "Religião", "description": "Conhecimento de deuses, ritos sagrados e criaturas divinas.", "attribute": "SAB"},

        # CARISMA (4)
        {"name": "Persuasão", "description": "Convencer outros através da lógica, diplomacia e carisma pessoal.", "attribute": "CAR"},
        {"name": "Intimidação", "description": "Coagir outros através da força física ou presença ameaçadora.", "attribute": "CAR"},
        {"name": "Enganação", "description": "Mentir convincentemente e criar histórias falsas críveis.", "attribute": "CAR"},
        {"name": "Atuação", "description": "Entreter plateias, disfarçar-se e interpretar papéis.", "attribute": "CAR"},
    ]

    for skill_data in SKILLS_DATA:
        insert_skills(conn, skill_data['name'], skill_data['description'], skill_data['attribute'])
    print("Perícias populadas.")

def populate_backgrounds(conn, insert_background, add_background_starting_skill):
    BACKGROUNDS_DATA = [
                {
            "name": "Mercenário",
            "description": "Sobreviveu lutando por moedas. Não importa quem paga, importa o quanto paga.",
            "skills": [
                {"name": "Armas de Uma Mão", "level": 1},
                {"name": "Armaduras Médias", "level": 1},
                {"name": "Intimidação", "level": 1}
            ]
        },
        {
            "name": "Artífice",
            "description": "Mãos calejadas de tanto construir, desmontar e experimentar engenhocas.",
            "skills": [
                {"name": "Engenharia", "level": 1},
                {"name": "Investigação", "level": 1},
                {"name": "Prestidigitação", "level": 1}
            ]
        },
        {
            "name": "Caçador",
            "description": "Rastros, cheiros e pegadas são como livros abertos para você.",
            "skills": [
                {"name": "Sobrevivência", "level": 1},
                {"name": "Natureza", "level": 1},
                {"name": "Armas de duas mãos", "level": 1}
            ]
        },
        {
            "name": "Acolito",
            "description": "Serviu em templos, realizando rituais e aprendendo os caminhos dos deuses.",
            "skills": [
                {"name": "Religião", "level": 1},
                {"name": "Medicina", "level": 1},
                {"name": "Intuição", "level": 1}
            ]
        },
        {
            "name": "Saltimbanco",
            "description": "Fez a vida nas estradas, entretendo multidões e enganando tolos.",
            "skills": [
                {"name": "Atuação", "level": 1},
                {"name": "Enganação", "level": 1},
                {"name": "Acrobacia", "level": 1}
            ]
        },
        {
            "name": "Gladiador",
            "description": "Ganhou fama e cicatrizes nas arenas de combate brutal.",
            "skills": [
                {"name": "Briga", "level": 1},
                {"name": "Esquiva", "level": 1},
                {"name": "Persuasão", "level": 1}
            ]
        },
        {
            "name": "Nobre",
            "description": "Nascido em berço de ouro, habituado aos costumes da corte.",
            "skills": [
                {"name": "Persuasão", "level": 1},
                {"name": "História", "level": 1},
                {"name": "Intuição", "level": 1}
            ]
        },
        {
            "name": "Bandido",
            "description": "Cresceu nas ruas, aprendeu a se virar na base da malandragem.",
            "skills": [
                {"name": "Furtividade", "level": 1},
                {"name": "Prestidigitação", "level": 1},
                {"name": "Arrombamento", "level": 1},
                {"name": "Intimidação", "level": 1}
            ]
        },
        {
            "name": "Eremita",
            "description": "Viveu isolado, em contato com a natureza e o divino.",
            "skills": [
                {"name": "Natureza", "level": 1},
                {"name": "Sobrevivência", "level": 1},
                {"name": "Religião", "level": 1}
            ]
        },
        {
            "name": "Acadêmico",
            "description": "Passou a vida estudando e desvendando mistérios.",
            "skills": [
                {"name": "Arcanismo", "level": 1},
                {"name": "Investigação", "level": 1},
                {"name": "Engenharia", "level": 1}
            ]
        }
    ]

    for bg_data in BACKGROUNDS_DATA:
        bg_id = insert_background(conn, bg_data['name'], bg_data['description'])
        if bg_id:
            for skill in bg_data['skills']:
                add_background_starting_skill(conn, bg_id, skill['name'], skill['level'])
    print("Antecedentes populados e perícias iniciais associadas.")