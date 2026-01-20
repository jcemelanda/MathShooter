# Math Shooter

Math Shooter é um jogo arcade educativo projetado para ajudar crianças (e adultos!) a praticar operações aritméticas básicas de uma forma divertida e desafiadora. 

![Math Shooter Icon](src/data/sprites/icone.png)

## 🚀 Como Executar

### Pré-requisitos
- Python 3.10 ou superior
- Pygame CE (ou Pygame padrão)

### Instalação
1. Clone o repositório ou baixe os arquivos.
2. No diretório raiz, instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### Iniciando o Jogo
Execute o script principal:
```bash
python src/main.py
```

## 🎮 Como Jogar
- **Setas do Teclado:** Movimentam sua nave pela arena.
- **Espaço:** Dispara o laser.
- **Objetivo:** Uma operação matemática aparecerá no canto superior esquerdo. Você deve destruir o inimigo que carrega o **número correto** que resolve a operação.
- **Pontuação:** 
  - Acertos: +10 pontos.
  - Erros: -10 pontos.
  - O jogo termina se sua pontuação chegar a -100.

## 🛠️ Arquitetura e Engenharia de Software
Este projeto foi recentemente refatorado para exemplificar as melhores práticas de desenvolvimento Python moderno ("Pythonic") e padrões avançados do livro **"Fluent Python"**:

- **Arquitetura Modular:** Código dividido em módulos lógicos (`entities`, `ui`, `operations`, `assets`, `game`).
- **Configuração Centralizada:** Todas as constantes de balanceamento e sistema estão em `src/config.py`.
- **Tipagem Estrutural (Protocols):** Uso de `typing.Protocol` para definir interfaces flexíveis (`Drawable`, `Updatable`).
- **Geradores para Scripting:** O modo treinamento usa geradores Python para gerenciar sequências de eventos sem bloquear o loop principal.
- **Propriedades Reativas:** Uso de `@property` para gerenciamento automático de estado e renderização na UI.
- **Carregamento de Assets:** Sistema centralizado de singletons para imagens, sons e fontes, garantindo eficiência e facilidade de acesso.

## 📝 Licença
Distribuído sob a licença **GPL v3**. Consulte o cabeçalho dos arquivos para mais detalhes.

## 👥 Créditos
- **Desenvolvedor Original:** Júlio César Eiras Melanda.
- **Música:** "Stone Fortress" de [opengameart.org](http://opengameart.org/content/stone-fortress).
- **Inspirado por:** Trabalho original de Tyler Gray & Chad Haley.
