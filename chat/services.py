from tortoise import Tortoise, run_async
from django.conf import settings
from .tortoise_models import ChatMessage
from Crypto.Cipher import AES
from base64 import b64encode
from base64 import b64decode

async def chat_save_message(username, room_id, message, message_type, image_caption):

    """ function to store chat message in sqlite """
    key = b'\xa8|Bc\xf8\xba\xac\xca\xdc/5U0\xe3\xd6f'
    cipher = AES.new(key, AES.MODE_CTR)
    nonce = b64encode(cipher.nonce).decode('utf-8')

    def encrypt_msg(message, *args, **kwargs):
        raw = message
        msg = str.encode(raw)
        ct_bytes = cipher.encrypt(msg)
        ct = b64encode(ct_bytes).decode('utf-8')
        message=ct
        return message

    await Tortoise.init(**settings.TORTOISE_ORM)
    await Tortoise.generate_schemas()

    await ChatMessage.create(room_id=room_id,
                            username=username,
                            nonce=nonce,
                            message=encrypt_msg(message),
                            message_type=message_type,
                            image_caption=image_caption
                       )

    await Tortoise.close_connections()
