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
      "img_logo": "https://cdn.freelogovectors.net/wp-content/uploads/2023/01/valorant-logo-freelogovectors.net_.png",
      "img_portada": "https://www.riotgames.com/darkroom/1440/8d5c497da1c2eeec8cffa99b01abc64b:5329ca773963a5b739e98e715957ab39/ps-f2p-val-console-launch-16x9.jpg",
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
      "img_logo": "https://seeklogo.com/images/C/call-of-duty-modern-warfare-ii-logo-28DD453EFD-seeklogo.com.png",
      "img_portada": "https://media.vandal.net/m/10-2022/202210231735180_1.jpg",
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
      "img_logo": "https://prezentidealny.com/784-medium_default/e-karta-podarunkowa-league-of-legends-40-zl.jpg",
      "img_portada": "https://cloudfront-us-east-1.images.arcpublishing.com/infobae/CNTWUAMXZRF3BPIYPCNPFHOMJQ.jpg",
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
      "img_logo": "https://upload.wikimedia.org/wikipedia/de/e/ef/Dota_2_logo.jpg",
      "img_portada": "https://i.pcmag.com/imagery/reviews/00XEmE7YBg1AOLEzZFQxhJV-3.fit_lim.size_1050x591.v1569475078.jpg",
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
      "img_logo": "https://cdn2.unrealengine.com/12br-delay-social-news-header-02-1920x1080-119208936.jpg",
      "img_portada": "https://cdn2.unrealengine.com/fortnite-disney-star-wars-all-1920x1080-296e87fd5954.jpg",
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
      "img_logo": "https://purepng.com/public/uploads/large/apex-legends-logo-high-resolution-dli.png",
      "img_portada": "https://cdn.wccftech.com/wp-content/uploads/2024/02/WCCFapexlegends98.jpg",
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
      "img_logo": "https://www.streetfighter.com/35_assets/images/35th/history/logo_sf6.png",
      "img_portada": "https://image.api.playstation.com/vulcan/ap/rnd/202211/1407/XFU0aPBvtm3W2od1ZvhByAOv.png",
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
      "img_logo": "https://cdn2.steamgriddb.com/logo/b6a9c87f9232d1b666ca857676a3a038.png",
      "img_portada": "https://image.api.playstation.com/vulcan/ap/rnd/202308/0312/aff71a0ced271048f5079b1fcf715bcb45110efc13e9704a.png",
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
      "img_logo": "https://bnetcmsus-a.akamaihd.net/cms/blog_header/ci/CIGT53U8ZP6M1509744317189.jpg",
      "img_portada": "https://blz-contentstack-images.akamaized.net/v3/assets/blt0e00eb71333df64e/blt987607ec059cdd8e/6621cf091b77b95867a01428/game_features_races.webp",
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
      "img_logo": "https://icon2.cleanpng.com/20180611/ixl/aa8n7yy34.webp",
      "img_portada": "https://sm.ign.com/ign_es/screenshot/default/age-of-empires-iv-19-10-2021-16-07-18_vx4x.png",
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
      "img_logo": "https://logowik.com/content/uploads/images/ea-sports-fc-246887.logowik.com.webp",
      "img_portada": "https://media.vandal.net/m/7-2023/20237101734547_1.jpg",
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
      "img_logo": "https://cdn.prgloo.com/media/e7810ff82a02494da13967aec9f1e414.png?width=1200&height=1800",
      "img_portada": "https://tecnogaming.com/wp-content/uploads/2023/09/NBA-2K24-portada-1392x872.jpg",
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
      "img_logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Gran_Turismo_7_logo.svg/512px-Gran_Turismo_7_logo.svg.png",
      "img_portada": "https://locosxlosjuegos.com/wp-content/uploads/2021/09/gran-turismo-7-principal-1021x580.jpg",
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
      "img_logo": "https://heusinkveld.com/wp-content/uploads/iRacing-Logo-Blue-Square-R_canv130-1-600x569.jpg",
      "img_portada": "https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/266410/header.jpg?t=1745351096",
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
      "img_logo": "https://www.zonammorpg.com/wp-content/uploads/2017/03/WoW_Arena_WC_Logo-810x400.jpg",
      "img_portada": "https://bnetcmsus-a.akamaihd.net/cms/blog_header/w6/W6VO7TJHHAXW1527698166151.jpg",
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
      "img_logo": "https://www.fraggi.de/wp-content/uploads/2022/02/lost-ark-logo.png",
      "img_portada": "https://static0.gamerantimages.com/wordpress/wp-content/uploads/2022/09/lost-ark-pvp-logo.jpg",
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
      "img_logo": "https://1000marcas.net/wp-content/uploads/2023/05/Fall-Guys-Logo.jpg",
      "img_portada": "https://cdn2.unrealengine.com/fgss04-keyart-offerimagelandscape-2560x1440-2560x1440-89c8edd4ffe307f5d760f286a28c3404-2560x1440-e9d811eebce7.jpg",
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
      "img_logo": "https://fontmeme.com/images/super-smash-bros-latest-logo-min.png",
      "img_portada": "https://gaming-cdn.com/images/news/articles/2357/cover/1000x563/la-suite-de-super-smash-bros-ultimate-n-est-pas-pour-tout-de-suite-cover64c7ab16c8d41.jpg",
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
      "img_logo": "https://1000logos.net/wp-content/uploads/2021/08/Hearthstone-Logo.jpg",
      "img_portada": "https://cdn.hobbyconsolas.com/sites/navi.axelspringer.es/public/media/image/2016/07/hearthstone-cabecera.jpg?tf=3840x",
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
      "img_logo": "https://upload.wikimedia.org/wikipedia/commons/e/e1/Logo_Legends_of_Runeterra.png",
      "img_portada": "https://cmsassets.rgpub.io/sanity/images/dsfx7636/news_live/69c109d43fbd655550360be103aa627fda4d3dba-1920x1080.jpg",
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
        
