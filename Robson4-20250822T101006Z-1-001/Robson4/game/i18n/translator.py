import json
import os
import sys

class Translator:
    def __init__(self, language: str = None):
        # Obter caminho absoluto para o arquivo de configuração na raiz do projeto
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.config_file = os.path.join(base_dir, "config.json")
        self.language = language or self._load_config()
        self.translations = self._load_translations()
        print(f"Tradutor inicializado com idioma: {self.language}")
    
    def _load_config(self):
        """Carrega o idioma do arquivo de configuração, se existir"""
        print(f"Verificando arquivo de configuração: {self.config_file}")
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    lang = config.get('language', 'pt-br')
                    print(f"Idioma carregado do arquivo: {lang}")
                    return lang
            except Exception as e:
                print(f"Erro ao ler arquivo de configuração: {str(e)}")
                return 'pt-br'
        
        print("Arquivo de configuração não encontrado. Usando padrão 'pt-br'.")
        return 'pt-br'
    
    def _save_config(self):
        """Salva o idioma atual no arquivo de configuração"""
        print(f"Salvando idioma '{self.language}' em {self.config_file}")
        
        try:
            # Cria o diretório se necessário
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump({'language': self.language}, f, ensure_ascii=False, indent=2)
            print("Configuração salva com sucesso!")
        except Exception as e:
            print(f"Erro grave ao salvar configuração: {str(e)}")
    
    def _load_translations(self) -> dict:
        """Carrega as traduções com fallback robusto"""
        print(f"Carregando traduções para: {self.language}")
        
        # Tenta carregar o idioma solicitado
        trans = self._load_language_file(self.language)
        if trans:
            print(f"Carregadas {len(trans)} traduções para {self.language}")
            return trans
        
        # Fallback para português
        if self.language != "pt-br":
            print("Tentando fallback para pt-br")
            trans = self._load_language_file("pt-br")
            if trans:
                print(f"Carregadas {len(trans)} traduções do fallback")
                return trans
        
        print("Usando dicionário de tradução vazio")
        return {}
    
    def _load_language_file(self, lang: str) -> dict:
        """Tenta carregar um arquivo de idioma específico"""
        try:
            # Caminho completo para o arquivo
            file_path = os.path.join(os.path.dirname(__file__), f"{lang}.py")
            
            # Verifica se o arquivo existe
            if not os.path.exists(file_path):
                print(f"Arquivo de tradução não encontrado: {file_path}")
                return {}
            
            # Lê o conteúdo do arquivo
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Executa o código em um namespace isolado
            namespace = {}
            exec(content, namespace)
            
            # Retorna as traduções
            return namespace.get('translations', {})
            
        except Exception as e:
            print(f"Erro ao carregar {lang}: {str(e)}")
            return {}
    
    def set_language(self, new_lang: str):
        print(f"Trocando idioma para: {new_lang}")
        self.language = new_lang
        self.translations = self._load_translations()
        self._save_config()  # Garante o salvamento imediato
    
    def t(self, key: str, **kwargs) -> str:
        """Obtém a tradução com substituição de variáveis"""
        # Fallback: usa a chave se não encontrar tradução
        template = self.translations.get(key, key)
        
        try:
            # Tenta formatar se houver parâmetros
            return template.format(**kwargs) if kwargs else template
        except:
            return template
    
    def get_current_language_name(self):
        """Retorna o nome amigável do idioma atual"""
        if self.language == "pt-br":
            return "Português"
        elif self.language == "en-us":
            return "English"
        return self.language


translator = Translator()  # Exportado como 'translator'