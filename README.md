# Jumper Frog

Um jogo de plataforma 2D desenvolvido em Python com **Pygame**, onde o jogador controla um sapo que precisa pular entre plataformas para alcançar o troféu em cada fase.

---

## Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Como Executar](#como-executar)
- [Controles](#controles)
- [Arquitetura](#arquitetura)
  - [Visão Geral](#visão-geral)
  - [Estrutura de Pastas](#estrutura-de-pastas)
  - [Fluxo de Dados](#fluxo-de-dados)
- [Módulos](#módulos)
  - [Core](#core)
  - [Entidades](#entidades)
  - [Cenas](#cenas)
  - [Níveis](#níveis)
  - [UI](#ui)
  - [Manager](#manager)
- [Assets](#assets)
- [Criando um Novo Nível](#criando-um-novo-nível)
- [Gerar Executável](#gerar-executável)
- [Qualidade de Código](#qualidade-de-código)
- [Tecnologias](#tecnologias)
- [Autor](#autor)

---

## Sobre o Projeto

**Jumper Frog** é um jogo de plataforma onde o jogador controla um sapo que deve saltar entre plataformas estáticas e móveis para alcançar um troféu que completa cada fase. O jogo possui mecânica de pulo com carga (segurar espaço para pular mais longe), animações de sprite, plataformas móveis, sistema de progressão com desbloqueio de fases e overlays de pausa e vitória.

### Características

- **Mecânica de pulo com carga** — segure espaço para carregar e solte para pular. Quanto mais tempo segurar, mais longe o sapo vai.
- **Animações de sprite** — o sapo possui 8 estados visuais diferentes (parado, andando, preparando pulo, pulando, caindo, overcharge, olhando bordas).
- **Plataformas móveis** — plataformas que se movem horizontal ou verticalmente, com o sapo acompanhando o movimento quando está em cima.
- **Sistema de progressão** — fases são desbloqueadas ao completar a anterior. Fases completadas exibem um mini troféu.
- **Hot reload** — alterações no código-fonte são detectadas automaticamente e recarregadas em tempo real durante o desenvolvimento.
- **Efeito visual de carga** — o sprite do sapo muda de tonalidade progressivamente durante o carregamento do pulo (aquecimento de cor + brilho).

---

## Como Executar

### Pré-requisitos

- Python 3.12+
- Pygame 2.5+

### Instalação

```bash
# Clonar o repositório
git clone <url-do-repositório>
cd Jumper-Frog

# Instalar dependências
pip install -r requirements.txt

# Executar o jogo
python -m src.main
```

### Com Docker

```bash
docker-compose up --build
```

---

## Controles

| Tecla | Ação |
|-------|------|
| `A` / `←` | Mover para a esquerda |
| `D` / `→` | Mover para a direita |
| `ESPAÇO` (segurar) | Carregar pulo |
| `ESPAÇO` (soltar) | Pular |
| `A` / `D` durante carga | Escolher direção do pulo |
| `ESC` | Pausar / Retomar o jogo |

---

## Arquitetura

### Visão Geral

O projeto segue uma arquitetura **Game Loop + OOP** com separação clara de responsabilidades:

```
Game → GameLoop → SceneManager → Scene ativa
         ↓              ↓
    InputHandler    Renderer
```

- **Game Loop** — ciclo principal que orquestra input → update → render a 60 FPS.
- **Scene Manager** — controla transições entre cenas (menu, seleção de fases, jogo, comandos).
- **Entities** — objetos do jogo (sapo, paredes, plataformas, troféu) com posição, colisão e renderização.
- **Levels** — cada fase define seus obstáculos, posição de spawn e posição do troféu.
- **UI Components** — botões, textboxes e overlays reutilizáveis.

### Estrutura de Pastas

```
Jumper-Frog/
├── assets/
│   ├── background/          # Imagens de fundo (menu, level1-3)
│   ├── frogs/               # Sprites do sapo (11 imagens)
│   └── icons/               # Ícones (troféu, cadeado, mini troféu)
├── src/
│   ├── main.py              # Ponto de entrada
│   ├── game.py              # Inicialização e orquestração
│   ├── core/                # Sistemas centrais do engine
│   │   ├── settings.py      # Constantes globais (tela, cores)
│   │   ├── game_loop.py     # Loop principal (input → update → render)
│   │   ├── renderer.py      # Gerenciamento da superfície de display
│   │   ├── input_handler.py # Captura de input (teclado + mouse)
│   │   ├── collision.py     # Resolução de colisão AABB
│   │   ├── progress.py      # Progressão (fases desbloqueadas/completadas)
│   │   └── hot_reloader.py  # Recarga automática de módulos
│   ├── entities/            # Objetos do jogo
│   │   ├── entity.py        # Classe base abstrata
│   │   ├── frog.py          # Jogador (estados, sprites, física)
│   │   ├── wall.py          # Parede estática
│   │   ├── moving_platform.py # Plataforma móvel (horizontal/vertical)
│   │   └── trophy.py        # Troféu (objetivo da fase)
│   ├── scenes/              # Telas do jogo
│   │   ├── scene.py         # Classe base abstrata
│   │   ├── menu_scene.py    # Menu principal
│   │   ├── commands_scene.py # Tela de comandos
│   │   ├── levels_scene.py  # Seleção de fases
│   │   └── game_scene.py    # Gameplay principal
│   ├── levels/              # Definição de fases
│   │   ├── level.py         # Classe base abstrata
│   │   ├── level_registry.py # Registry/factory de fases
│   │   ├── level_1.py       # Fase 1 (introdutória)
│   │   ├── level_2.py       # Fase 2 (intermediária)
│   │   └── level_3.py       # Fase 3 (desafiadora)
│   ├── manager/
│   │   └── scene_manager.py # Gerenciador de cenas
│   └── ui/                  # Componentes de interface
│       ├── button.py        # Botão clicável com hover
│       ├── back_button.py   # Botão de voltar (←)
│       ├── textbox.py       # Caixa de texto estática
│       ├── pause_overlay.py # Overlay de pausa
│       └── victory_overlay.py # Overlay de vitória
├── tests/                   # Testes unitários
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

### Fluxo de Dados

```
┌─────────┐   poll()   ┌──────────────┐
│  Pygame  │ ────────→  │ InputHandler │
│  Events  │            │ (keys, mouse)│
└─────────┘            └──────┬───────┘
                              │
                              ▼
               ┌────────────────────────┐
               │       GameLoop         │
               │  handle_events()       │
               │  update(dt)            │
               │  render(screen)        │
               └───────────┬────────────┘
                           │
                           ▼
               ┌────────────────────────┐
               │     SceneManager       │
               │  delegates to active   │
               │  Scene                 │
               └───────────┬────────────┘
                           │
            ┌──────────────┼──────────────┐
            ▼              ▼              ▼
       ┌─────────┐  ┌───────────┐  ┌──────────┐
       │MenuScene│  │LevelsScene│  │GameScene  │
       └─────────┘  └───────────┘  │ ┌──────┐  │
                                   │ │ Frog  │  │
                                   │ │Solids │  │
                                   │ │Trophy │  │
                                   │ └──────┘  │
                                   └──────────┘
```

---

## Módulos

### Core

#### `settings.py`
Constantes globais do jogo:
- **Tela**: 800 × 600 pixels, 60 FPS
- **Cores**: WHITE, BLACK, RED, GREEN (variações), GRAY (variações), BLUE (variações)

#### `game_loop.py`
Loop principal do jogo. Executa o ciclo `clock.tick(FPS)` → `input_handler.poll()` → `handle_events()` → `update(dt)` → `render()` → `present()`. Suporta hot reload opcional.

#### `input_handler.py`
Captura e organiza o input por frame:
- `keys_pressed` — teclas mantidas pressionadas (contínuo)
- `keys_down` — teclas pressionadas neste frame (edge-triggered)
- `keys_up` — teclas soltas neste frame (edge-triggered)
- `mouse_pos`, `mouse_clicked` — estado do mouse

#### `collision.py`
Resolução de colisão AABB por penetração mínima. A função `resolve_collisions(entity, solids)` empurra a entidade para fora de cada sólido sobreposto pelo eixo de menor penetração.

#### `progress.py`
Rastreamento de progressão em memória:
- `get_unlocked()` — nível mais alto desbloqueado
- `unlock_next(level)` — desbloqueia o próximo nível
- `mark_completed(level)` — marca nível como completado
- `is_completed(level)` — verifica se nível foi completado

#### `hot_reloader.py`
Usa `watchdog` para monitorar alterações em arquivos `.py` dentro de `src/`. Quando detecta mudanças, recarrega todos os módulos `src.*` e reconstrói a cena ativa.

### Entidades

#### `Entity` (base abstrata)
Classe base para todos os objetos do jogo. Define posição (`x`, `y`), dimensões (`width`, `height`), cor, `pygame.Rect`, e métodos `update()`, `draw()`, `collides_with()`.

#### `Frog` (jogador)
O sapo controlado pelo jogador, com 4 estados físicos:

| Estado | Descrição |
|--------|-----------|
| `GROUNDED` | No chão, pode andar e iniciar pulo |
| `CHARGING` | Carregando pulo (segurando espaço) |
| `AIRBORNE` | No ar após pular |
| `FALLING` | Caindo após sair de uma plataforma |

8 estados visuais com sprites dedicados: `default`, `walking` (3 frames), `preparing`, `jumping`, `falling`, `overcharge`, `on_edge_front`, `on_edge_back`.

Parâmetros configuráveis: velocidade, ângulo de pulo, carga máxima, potência min/max, gravidade.

#### `Wall` (parede estática)
Obstáculo retangular sólido imóvel. Usado para bordas do nível e plataformas fixas.

#### `MovingPlatform` (plataforma móvel)
Plataforma sólida que oscila entre dois pontos:
- `AXIS_HORIZONTAL` — movimento horizontal
- `AXIS_VERTICAL` — movimento vertical
- Expõe `dx`/`dy` por frame para que a cena possa carregar entidades.

#### `Trophy` (troféu)
Objeto coletável que marca o objetivo da fase. Carrega e renderiza o sprite `assets/icons/trophy.png`.

### Cenas

#### `MenuScene`
Menu principal com título "Jumper frog", 3 botões (Iniciar, Comandos, Sair) e créditos. Usa background de `assets/background/menu.png`.

#### `CommandsScene`
Exibe os controles do jogo em layout de duas colunas (tecla | ação). Botão de voltar retorna ao menu.

#### `LevelsScene`
Grade de seleção de fases. Fases bloqueadas exibem ícone de cadeado (`padlock.png`), fases completadas exibem mini troféu (`mini_trophy.png`). Hover destaca a fase.

#### `GameScene`
Cena principal de gameplay. Ordem de atualização por frame:
1. Atualiza plataformas móveis
2. Carrega sapo com plataforma (se estiver em cima)
3. Atualiza sapo (input + física)
4. Resolve colisões AABB
5. Reações de colisão aérea (bounce, land, ceiling)
6. Verificação de suporte no chão (início de queda)
7. Colisão com troféu → vitória

Overlays: **Pausa** (ESC) com Retornar/Reiniciar/Menu e **Vitória** com Próxima Fase/Menu.

### Níveis

Cada nível herda de `Level` e define:
- `_build_obstacles()` — lista de `Wall` e `MovingPlatform`
- `get_spawn_position()` — posição inicial do sapo
- `get_trophy_position()` — posição do troféu

Background carregado automaticamente de `assets/background/level<N>.png`.

| Fase | Dificuldade | Destaques |
|------|-------------|-----------|
| 1 | Introdutória | Plataformas estáticas + móvel horizontal |
| 2 | Intermediária | Elevador vertical + plataforma rápida |
| 3 | Desafiadora | Ascensão vertical em zigzag, timing preciso |

### UI

- **`Button`** — botão clicável com hover, sombra e callback.
- **`BackButton`** — botão ← no canto superior esquerdo.
- **`TextBox`** — caixa de texto estática com fundo e borda.
- **`PauseOverlay`** — overlay translúcido com 3 botões (Retornar, Reiniciar, Menu).
- **`VictoryOverlay`** — overlay de parabéns / jogo completo com navegação.

### Manager

- **`SceneManager`** — mantém a cena ativa e delega `handle_events`, `update` e `render`.

---

## Assets

```
assets/
├── background/
│   ├── menu.png          # Fundo do menu e seleção de fases
│   ├── level1.png        # Fundo da fase 1
│   ├── level2.png        # Fundo da fase 2
│   └── level3.png        # Fundo da fase 3
├── frogs/
│   ├── default.png       # Sapo parado
│   ├── walking_1.png     # Andando (frame 1)
│   ├── walking_2.png     # Andando (frame 2)
│   ├── walking_3.png     # Andando (frame 3)
│   ├── preparing.png     # Preparando pulo
│   ├── overcharge.png    # Carga acima de 80%
│   ├── jumping.png       # No ar (18×17, aspecto diferente)
│   ├── screaming.png     # Caindo
│   ├── looking_front.png # Olhando borda frontal
│   └── looking_back.png  # Olhando borda traseira
└── icons/
    ├── trophy.png        # Troféu (objetivo da fase)
    ├── mini_trophy.png   # Mini troféu (fase completada)
    └── padlock.png       # Cadeado (fase bloqueada)
```

Os sprites do sapo têm resolução base de 18×13 pixels (exceto `jumping.png` que é 18×17) e são escalados para 36×26 no jogo.

---

## Criando um Novo Nível

1. Crie `src/levels/level_N.py`:

```python
from src.entities.entity import Entity
from src.entities.moving_platform import MovingPlatform
from src.entities.wall import Wall
from src.levels.level import Level


class LevelN(Level):
    def __init__(self):
        super().__init__(level_number=N)

    def _build_obstacles(self) -> list[Entity]:
        return [
            Wall(x, y, width, height),
            MovingPlatform(
                x, y, width, height,
                axis=MovingPlatform.AXIS_HORIZONTAL,
                distance=200, speed=100,
            ),
        ]

    def get_spawn_position(self) -> tuple[float, float]:
        from src.entities.frog import Frog
        return (100, 500 - Frog.DEFAULT_HEIGHT)

    def get_trophy_position(self) -> tuple[float, float]:
        from src.entities.trophy import Trophy
        return (600, 100 - Trophy.DEFAULT_SIZE)
```

2. Registre em `src/levels/level_registry.py`:

```python
from src.levels.level_N import LevelN
_REGISTRY[N] = LevelN
```

3. Adicione o background em `assets/background/levelN.png`.

A área jogável é **800×600** com bordas de 20px em cada lado (área útil: 20–780 horizontal, 20–580 vertical).

---

## Gerar Executável

O projeto inclui um arquivo de configuração [jumper_frog.spec](jumper_frog.spec) para gerar um executável standalone com **PyInstaller**. O executável empacota todo o código e os assets em um único arquivo, dispensando a instalação de Python ou dependências no computador de destino.

### Pré-requisitos para Build

```bash
pip install pyinstaller
```

No Linux, o pacote `binutils` também é necessário:

```bash
sudo apt install binutils
```

### Gerar o Executável

```bash
pyinstaller jumper_frog.spec
```

O executável será gerado em `dist/JumperFrog` (Linux/macOS) ou `dist/JumperFrog.exe` (Windows).

### Executar

```bash
# Linux / macOS
./dist/JumperFrog

# Windows
dist\JumperFrog.exe
```

### Como Funciona

O arquivo `jumper_frog.spec` configura:

- **Ponto de entrada**: `src/main.py`
- **Assets incluídos**: todas as imagens de `assets/background/`, `assets/frogs/` e `assets/icons/` são empacotadas dentro do executável.
- **Hidden imports**: todos os módulos de `src/` são listados explicitamente para garantir que o PyInstaller os inclua.
- **Modo onefile**: gera um único arquivo executável (`console=False` suprime o terminal no Windows).
- **Resolução de assets**: em modo `--onefile`, o PyInstaller extrai os assets para um diretório temporário (`sys._MEIPASS`). O código detecta isso automaticamente via `BASE_DIR` em `settings.py`.

> **Nota**: no diretório `dist/` gerado pelo PyInstaller esterá presente o `.exe`.

### Build para Outro Sistema Operacional

O PyInstaller gera executáveis **nativos para o sistema onde o build é executado**. Para gerar um `.exe` do Windows, execute o build em uma máquina Windows. O mesmo vale para macOS.

---

## Qualidade de Código

O projeto utiliza **pylint** para validação de qualidade:

```bash
pylint src/
```

Regras do projeto:
- Manter arquitetura **Game Loop + OOP**
- Reutilizar componentes de UI existentes
- Docstrings em classes e funções
- Nomes explícitos e descritivos

---

## Tecnologias

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| Python | 3.12+ | Linguagem principal |
| Pygame | 2.5+ | Engine gráfico e input |
| Watchdog | 4.0+ | Hot reload de módulos |
| Pytest | 7.4+ | Testes unitários |
| Pylint | 3.0+ | Análise estática de código |
| Docker | — | Containerização |

---

## Autor

**Igor Fuchs Pereira**
