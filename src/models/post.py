from datetime import datetime
from config import Conexion
from bson.objectid import ObjectId

db = Conexion()
posts_collection = db["publicaciones"]
comments_collection = db["comentarios"]
reactions_collection = db["reacciones"]

class Post:
    def __init__(self, titulo, contenido, autor_id, tipo, juego_id=None, img_url=None, imagen=None):
        self.titulo = titulo
        self.contenido = contenido
        self.autor_id = ObjectId(autor_id)
        self.tipo = tipo  # 'logro', 'estrategia', 'noticia'
        self.juego_id = ObjectId(juego_id) if juego_id else None
        self.img_url = img_url
        self.imagen = imagen
        self.fecha_creacion = datetime.utcnow()
        self.likes = 0
        self.comentarios = 0
        # Extraer hashtags del contenido
        self.hashtags = self._extract_hashtags(contenido)

    def _extract_hashtags(self, text):
        """Extrae hashtags del texto (palabras que empiezan con #)"""
        return [word.strip('#') for word in text.split() if word.startswith('#')]

    def save(self):
        post_data = {
            "titulo": self.titulo,
            "contenido": self.contenido,
            "autor_id": self.autor_id,
            "tipo": self.tipo,
            "juego_id": self.juego_id,
            "img_url": self.img_url,
            "imagen": self.imagen,
            "fecha_creacion": self.fecha_creacion,
            "likes": self.likes,
            "comentarios": self.comentarios,
            "hashtags": self.hashtags
        }
        return posts_collection.insert_one(post_data)

    @staticmethod
    def get_all(limit=10, skip=0):
        return list(posts_collection.find().sort("fecha_creacion", -1).skip(skip).limit(limit))

    @staticmethod
    def get_by_id(post_id):
        return posts_collection.find_one({"_id": ObjectId(post_id)})

    @staticmethod
    def get_by_author(author_id, limit=10):
        return list(posts_collection.find({"autor_id": ObjectId(author_id)}).sort("fecha_creacion", -1).limit(limit))

    @staticmethod
    def get_by_type(tipo, limit=10):
        return list(posts_collection.find({"tipo": tipo}).sort("fecha_creacion", -1).limit(limit))

    @staticmethod
    def get_by_game(game_id, limit=10):
        return list(posts_collection.find({"juego_id": ObjectId(game_id)}).sort("fecha_creacion", -1).limit(limit))

    @staticmethod
    def get_by_hashtag(hashtag, limit=10):
        """Obtiene publicaciones por hashtag"""
        return list(posts_collection.find(
            {"hashtags": hashtag}
        ).sort("fecha_creacion", -1).limit(limit))

    @staticmethod
    def update_post(post_id, update_data):
        return posts_collection.update_one(
            {"_id": ObjectId(post_id)},
            {"$set": update_data}
        )

    @staticmethod
    def delete_post(post_id):
        # Eliminar comentarios y reacciones asociados
        comments_collection.delete_many({"post_id": ObjectId(post_id)})
        reactions_collection.delete_many({"post_id": ObjectId(post_id)})
        return posts_collection.delete_one({"_id": ObjectId(post_id)})

    @staticmethod
    def increment_comments(post_id):
        return posts_collection.update_one(
            {"_id": ObjectId(post_id)},
            {"$inc": {"comentarios": 1}}
        )

    @staticmethod
    def decrement_comments(post_id):
        return posts_collection.update_one(
            {"_id": ObjectId(post_id)},
            {"$inc": {"comentarios": -1}}
        )

class Comment:
    def __init__(self, contenido, autor_id, post_id):
        self.contenido = contenido
        self.autor_id = ObjectId(autor_id)
        self.post_id = ObjectId(post_id)
        self.fecha_creacion = datetime.utcnow()
        self.likes = 0

    def save(self):
        comment_data = {
            "contenido": self.contenido,
            "autor_id": self.autor_id,
            "post_id": self.post_id,
            "fecha_creacion": self.fecha_creacion,
            "likes": self.likes
        }
        result = comments_collection.insert_one(comment_data)
        if result.inserted_id:
            Post.increment_comments(self.post_id)
        return result

    @staticmethod
    def get_by_post(post_id):
        return list(comments_collection.find({"post_id": ObjectId(post_id)}).sort("fecha_creacion", -1))

    @staticmethod
    def delete_comment(comment_id):
        comment = comments_collection.find_one({"_id": ObjectId(comment_id)})
        if comment:
            Post.decrement_comments(comment["post_id"])
            return comments_collection.delete_one({"_id": ObjectId(comment_id)})
        return None

class Reaction:
    def __init__(self, usuario_id, post_id, tipo="like"):
        self.usuario_id = ObjectId(usuario_id)
        self.post_id = ObjectId(post_id)
        self.tipo = tipo
        self.fecha_creacion = datetime.utcnow()

    def save(self):
        # Verificar si ya existe una reacción
        existing = reactions_collection.find_one({
            "usuario_id": self.usuario_id,
            "post_id": self.post_id
        })

        if existing:
            # Si ya existe y es del mismo tipo, eliminarla
            if existing["tipo"] == self.tipo:
                reactions_collection.delete_one({"_id": existing["_id"]})
                posts_collection.update_one(
                    {"_id": self.post_id},
                    {"$inc": {"likes": -1}}
                )
                return False
            # Si es de diferente tipo, actualizar
            else:
                reactions_collection.update_one(
                    {"_id": existing["_id"]},
                    {"$set": {"tipo": self.tipo}}
                )
                return True
        else:
            # Si no existe, crear nueva
            reaction_data = {
                "usuario_id": self.usuario_id,
                "post_id": self.post_id,
                "tipo": self.tipo,
                "fecha_creacion": self.fecha_creacion
            }
            reactions_collection.insert_one(reaction_data)
            posts_collection.update_one(
                {"_id": self.post_id},
                {"$inc": {"likes": 1}}
            )
            return True

    @staticmethod
    def get_by_post(post_id):
        return list(reactions_collection.find({"post_id": ObjectId(post_id)}))

    @staticmethod
    def get_by_user_and_post(usuario_id, post_id):
        return reactions_collection.find_one({
            "usuario_id": ObjectId(usuario_id),
            "post_id": ObjectId(post_id)
        }) 