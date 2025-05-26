from config import Conexion

db = Conexion()
users_collection = db["usuarios"]
games_collection = db["games"]

class Game:
    def __init__(self, game, descripcion, categoria):
        self.game = game
        self.descripcion = descripcion
        self.categoria = categoria
        self.profile_game = {
            "img_logo": "",
            "img_portada": "",
            "desarrollador": "",         # Ej: Riot Games
            "editor": "",                # Ej: Valve
            "modo_juego": [],            # Ej: 5v5, 1v1, escuadras
            "plataformas": [],             # Ej: ['PC', 'PS5', 'Xbox']
            "formato_torneo": [],        # Ej: Individual, Equipos, Mixto
            "ranking_global": [],        # Opcional, si enlazas con alguna API o sistema propio
            "sitio_oficial": ""          # Link al sitio web del juego
        }

    def save_game(self):
        game_data={
            "game":self.game,
            "descripcion":self.descripcion,
            "categoria":self.categoria,
            "profile_game":self.profile_game
        }

        games_iniciales=[
  {
    "game": "Valorant",
    "descripcion": "Shooter táctico 5v5 con agentes que usan habilidades especiales.",
    "categoria": "Shooter (FPS/TPS)",
    "profile_game": {
      "img_logo": "valorant_logo.png",
      "img_portada": "valorant_portada.jpg",
      "desarrollador": "Riot Games",
      "editor": "Riot Games",
      "modo_juego": ["5v5"],
      "plataformas": ["PC"],
      "formato_torneo": ["Equipos"],
      "ranking_global": [],
      "sitio_oficial": "https://playvalorant.com"
    }
  },
  {
    "game": "Call of Duty: Modern Warfare II",
    "descripcion": "FPS militar con múltiples modos PvP competitivos.",
    "categoria": "Shooter (FPS/TPS)",
    "profile_game": {
      "img_logo": "codmw2_logo.png",
      "img_portada": "codmw2_portada.jpg",
      "desarrollador": "Infinity Ward",
      "editor": "Activision",
      "modo_juego": ["6v6", "Battle Royale"],
      "plataformas": ["PC", "PS5", "Xbox"],
      "formato_torneo": ["Individual", "Equipos"],
      "ranking_global": [],
      "sitio_oficial": "https://www.callofduty.com"
    }
  },
  {
    "game": "League of Legends",
    "descripcion": "MOBA competitivo donde dos equipos de cinco campeones compiten en la Grieta del Invocador.",
    "categoria": "MOBA",
    "profile_game": {
      "img_logo": "lol_logo.png",
      "img_portada": "lol_portada.jpg",
      "desarrollador": "Riot Games",
      "editor": "Riot Games",
      "modo_juego": ["5v5"],
      "plataformas": ["PC"],
      "formato_torneo": ["Equipos"],
      "ranking_global": [],
      "sitio_oficial": "https://www.leagueoflegends.com"
    }
  },
  {
    "game": "Dota 2",
    "descripcion": "MOBA estratégico con héroes únicos y competencias de alto nivel.",
    "categoria": "MOBA",
    "profile_game": {
      "img_logo": "dota2_logo.png",
      "img_portada": "dota2_portada.jpg",
      "desarrollador": "Valve",
      "editor": "Valve",
      "modo_juego": ["5v5"],
      "plataformas": ["PC"],
      "formato_torneo": ["Equipos"],
      "ranking_global": [],
      "sitio_oficial": "https://www.dota2.com"
    }
  },
  {
    "game": "Fortnite",
    "descripcion": "Battle Royale con construcción y combate rápido.",
    "categoria": "Battle Royale",
    "profile_game": {
      "img_logo": "fortnite_logo.png",
      "img_portada": "fortnite_portada.jpg",
      "desarrollador": "Epic Games",
      "editor": "Epic Games",
      "modo_juego": ["Individual", "Escuadra"],
      "plataformas": ["PC", "PS5", "Xbox", "Switch"],
      "formato_torneo": ["Individual", "Equipos"],
      "ranking_global": [],
      "sitio_oficial": "https://www.fortnite.com"
    }
  },
  {
    "game": "Apex Legends",
    "descripcion": "Battle Royale por escuadras con leyendas que poseen habilidades únicas.",
    "categoria": "Battle Royale",
    "profile_game": {
      "img_logo": "apex_logo.png",
      "img_portada": "apex_portada.jpg",
      "desarrollador": "Respawn Entertainment",
      "editor": "Electronic Arts",
      "modo_juego": ["3v3", "Battle Royale"],
      "plataformas": ["PC", "PS5", "Xbox"],
      "formato_torneo": ["Equipos"],
      "ranking_global": [],
      "sitio_oficial": "https://www.ea.com/games/apex-legends"
    }
  },
  {
    "game": "Street Fighter 6",
    "descripcion": "Clásico juego de lucha con personajes emblemáticos y torneos 1v1.",
    "categoria": "Lucha (Fighting)",
    "profile_game": {
      "img_logo": "sf6_logo.png",
      "img_portada": "sf6_portada.jpg",
      "desarrollador": "Capcom",
      "editor": "Capcom",
      "modo_juego": ["1v1"],
      "plataformas": ["PC", "PS5", "Xbox"],
      "formato_torneo": ["Individual"],
      "ranking_global": [],
      "sitio_oficial": "https://www.streetfighter.com/6/"
    }
  },
  {
    "game": "Tekken 8",
    "descripcion": "Juego de lucha 3D con personajes únicos y estilo agresivo.",
    "categoria": "Lucha (Fighting)",
    "profile_game": {
      "img_logo": "tekken8_logo.png",
      "img_portada": "tekken8_portada.jpg",
      "desarrollador": "Bandai Namco",
      "editor": "Bandai Namco",
      "modo_juego": ["1v1"],
      "plataformas": ["PC", "PS5", "Xbox"],
      "formato_torneo": ["Individual"],
      "ranking_global": [],
      "sitio_oficial": "https://tekken.com"
    }
  },
  {
    "game": "StarCraft II",
    "descripcion": "RTS de ciencia ficción con razas únicas y combates intensos.",
    "categoria": "Estrategia (RTS/TBS)",
    "profile_game": {
      "img_logo": "sc2_logo.png",
      "img_portada": "sc2_portada.jpg",
      "desarrollador": "Blizzard Entertainment",
      "editor": "Blizzard Entertainment",
      "modo_juego": ["1v1", "2v2"],
      "plataformas": ["PC"],
      "formato_torneo": ["Individual", "Equipos"],
      "ranking_global": [],
      "sitio_oficial": "https://starcraft2.com"
    }
  },
  {
    "game": "Age of Empires IV",
    "descripcion": "Juego de estrategia histórica en tiempo real.",
    "categoria": "Estrategia (RTS/TBS)",
    "profile_game": {
      "img_logo": "aoe4_logo.png",
      "img_portada": "aoe4_portada.jpg",
      "desarrollador": "Relic Entertainment",
      "editor": "Xbox Game Studios",
      "modo_juego": ["1v1", "4v4"],
      "plataformas": ["PC"],
      "formato_torneo": ["Individual", "Equipos"],
      "ranking_global": [],
      "sitio_oficial": "https://www.ageofempires.com/games/age-of-empires-iv/"
    }
  },
  {
    "game": "FIFA 24",
    "descripcion": "Simulador de fútbol con modos en línea competitivos, ideal para torneos individuales y por clubes.",
    "categoria": "Deportes",
    "profile_game": {
      "img_logo": "fifa24_logo.png",
      "img_portada": "fifa24_portada.jpg",
      "desarrollador": "EA Sports",
      "editor": "Electronic Arts",
      "modo_juego": ["1v1", "Clubes Pro (11v11)"],
      "plataformas": ["PC", "PS5", "Xbox"],
      "formato_torneo": ["Individual", "Equipos"],
      "ranking_global": [],
      "sitio_oficial": "https://www.ea.com/games/ea-sports-fc"
    }
  },
  {
    "game": "NBA 2K24",
    "descripcion": "Simulador de baloncesto competitivo con partidas rápidas o ligas completas.",
    "categoria": "Deportes",
    "profile_game": {
      "img_logo": "nba2k24_logo.png",
      "img_portada": "nba2k24_portada.jpg",
      "desarrollador": "Visual Concepts",
      "editor": "2K Sports",
      "modo_juego": ["1v1", "5v5", "3v3"],
      "plataformas": ["PC", "PS5", "Xbox"],
      "formato_torneo": ["Individual", "Equipos"],
      "ranking_global": [],
      "sitio_oficial": "https://nba.2k.com/2k24/"
    }
  },
  {
    "game": "Gran Turismo 7",
    "descripcion": "Simulador de carreras con física realista y torneos online.",
    "categoria": "Carreras",
    "profile_game": {
      "img_logo": "gt7_logo.png",
      "img_portada": "gt7_portada.jpg",
      "desarrollador": "Polyphony Digital",
      "editor": "Sony Interactive Entertainment",
      "modo_juego": ["1v1", "Carreras Multijugador"],
      "plataformas": ["PS5"],
      "formato_torneo": ["Individual"],
      "ranking_global": [],
      "sitio_oficial": "https://www.gran-turismo.com"
    }
  },
  {
    "game": "iRacing",
    "descripcion": "Simulador de carreras online muy utilizado en eSports por su realismo.",
    "categoria": "Carreras",
    "profile_game": {
      "img_logo": "iracing_logo.png",
      "img_portada": "iracing_portada.jpg",
      "desarrollador": "iRacing.com Motorsport Simulations",
      "editor": "iRacing.com",
      "modo_juego": ["Carreras Online"],
      "plataformas": ["PC"],
      "formato_torneo": ["Individual"],
      "ranking_global": [],
      "sitio_oficial": "https://www.iracing.com"
    }
  },
  {
    "game": "World of Warcraft Arena",
    "descripcion": "Modo PvP competitivo en equipos dentro del MMORPG más popular.",
    "categoria": "RPG Competitivo (MMORPG, ARPG PvP)",
    "profile_game": {
      "img_logo": "wow_logo.png",
      "img_portada": "wow_portada.jpg",
      "desarrollador": "Blizzard Entertainment",
      "editor": "Blizzard Entertainment",
      "modo_juego": ["2v2", "3v3"],
      "plataformas": ["PC"],
      "formato_torneo": ["Equipos"],
      "ranking_global": [],
      "sitio_oficial": "https://worldofwarcraft.com"
    }
  },
  {
    "game": "Lost Ark PvP",
    "descripcion": "ARPG con combate dinámico y modos PvP por equipos e individuales.",
    "categoria": "RPG Competitivo (MMORPG, ARPG PvP)",
    "profile_game": {
      "img_logo": "lostark_logo.png",
      "img_portada": "lostark_portada.jpg",
      "desarrollador": "Smilegate RPG",
      "editor": "Amazon Games",
      "modo_juego": ["1v1", "3v3 PvP"],
      "plataformas": ["PC"],
      "formato_torneo": ["Individual", "Equipos"],
      "ranking_global": [],
      "sitio_oficial": "https://www.playlostark.com"
    }
  },
  {
    "game": "Fall Guys",
    "descripcion": "Party game multijugador donde compiten hasta 60 jugadores en pruebas de eliminación.",
    "categoria": "Party Games Competitivos",
    "profile_game": {
      "img_logo": "fallguys_logo.png",
      "img_portada": "fallguys_portada.jpg",
      "desarrollador": "Mediatonic",
      "editor": "Epic Games",
      "modo_juego": ["Individual", "Escuadra"],
      "plataformas": ["PC", "PS5", "Xbox", "Switch"],
      "formato_torneo": ["Individual", "Equipos"],
      "ranking_global": [],
      "sitio_oficial": "https://www.fallguys.com"
    }
  },
  {
    "game": "Super Smash Bros. Ultimate",
    "descripcion": "Juego de lucha estilo party competitivo con personajes de distintas franquicias.",
    "categoria": "Party Games Competitivos",
    "profile_game": {
      "img_logo": "smash_logo.png",
      "img_portada": "smash_portada.jpg",
      "desarrollador": "Nintendo",
      "editor": "Nintendo",
      "modo_juego": ["1v1", "Todos contra todos"],
      "plataformas": ["Switch"],
      "formato_torneo": ["Individual", "Equipos"],
      "ranking_global": [],
      "sitio_oficial": "https://www.smashbros.com"
    }
  },
  {
    "game": "Hearthstone",
    "descripcion": "Juego de cartas online basado en el universo de Warcraft.",
    "categoria": "Juego de Cartas Competitivo",
    "profile_game": {
      "img_logo": "hearthstone_logo.png",
      "img_portada": "hearthstone_portada.jpg",
      "desarrollador": "Blizzard Entertainment",
      "editor": "Blizzard Entertainment",
      "modo_juego": ["1v1"],
      "plataformas": ["PC", "Mobile"],
      "formato_torneo": ["Individual"],
      "ranking_global": [],
      "sitio_oficial": "https://playhearthstone.com"
    }
  },
  {
    "game": "Legends of Runeterra",
    "descripcion": "Juego de cartas estratégico ambientado en el mundo de League of Legends.",
    "categoria": "Juego de Cartas Competitivo",
    "profile_game": {
      "img_logo": "lor_logo.png",
      "img_portada": "lor_portada.jpg",
      "desarrollador": "Riot Games",
      "editor": "Riot Games",
      "modo_juego": ["1v1"],
      "plataformas": ["PC", "Mobile"],
      "formato_torneo": ["Individual"],
      "ranking_global": [],
      "sitio_oficial": "https://playruneterra.com"
    }
  }
]

        games_collection.insert_many(games_iniciales)

        return games_collection.insert_one(game_data)
        
