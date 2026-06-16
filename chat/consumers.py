import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class PresenceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'presence'
        user = self.scope['user']

        if user.is_authenticated and user.role in ['AGENT', 'ADMIN']:
            await self.set_user_online(user, True)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        if user.is_authenticated:
            await self.broadcast_presence(user.id, user.username, True)

    async def disconnect(self, close_code):
        user = self.scope['user']
        if user.is_authenticated and user.role in ['AGENT', 'ADMIN']:
            await self.set_user_online(user, False)

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        if user.is_authenticated:
            await self.broadcast_presence(user.id, user.username, False)

    async def receive(self, text_data):
        pass

    async def presence_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'presence',
            'user_id': event['user_id'],
            'username': event['username'],
            'is_online': event['is_online'],
        }))

    async def broadcast_presence(self, user_id, username, is_online):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'presence_update',
                'user_id': user_id,
                'username': username,
                'is_online': is_online,
            }
        )

    @database_sync_to_async
    def set_user_online(self, user, online):
        from django.utils import timezone
        user.is_online = online
        if not online:
            user.last_seen = timezone.now()
        user.save(update_fields=['is_online', 'last_seen'] if not online else ['is_online'])


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'

        user = self.scope['user']
        if user.is_authenticated:
            await self.set_user_online(user, True)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        if user.is_authenticated and user.role in ['AGENT', 'ADMIN']:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'presence_update',
                    'user_id': user.id,
                    'username': user.username,
                    'is_online': True,
                }
            )

    async def disconnect(self, close_code):
        user = self.scope['user']
        if user.is_authenticated:
            await self.set_user_online(user, False)

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        if user.is_authenticated and user.role in ['AGENT', 'ADMIN']:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'presence_update',
                    'user_id': user.id,
                    'username': user.username,
                    'is_online': False,
                }
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        msg_type = data.get('type', 'message')

        if msg_type == 'typing':
            await self.handle_typing(data)
        elif msg_type == 'stop_typing':
            await self.handle_stop_typing(data)
        elif msg_type == 'message':
            await self.handle_message(data)

    async def handle_message(self, data):
        contenu = data.get('contenu', '').strip()
        if not contenu:
            return

        user = self.scope['user']
        message = await self.save_message(self.conversation_id, user, contenu)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': {
                    'id': message.id,
                    'auteur': getattr(user, 'id', 0),
                    'auteur_nom': getattr(user, 'username', 'Anonyme'),
                    'contenu': contenu,
                    'timestamp': message.timestamp.isoformat(),
                    'lu': False,
                }
            }
        )

    async def handle_typing(self, data):
        user = self.scope['user']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'typing_indicator',
                'user_id': user.id,
                'username': user.username,
                'conversation_id': int(self.conversation_id),
            }
        )

    async def handle_stop_typing(self, data):
        user = self.scope['user']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'stop_typing_indicator',
                'user_id': user.id,
                'username': user.username,
                'conversation_id': int(self.conversation_id),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['message']))

    async def typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'user': event['username'],
            'conversation_id': event['conversation_id'],
        }))

    async def stop_typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            'type': 'stop_typing',
            'user_id': event['user_id'],
            'conversation_id': event['conversation_id'],
        }))

    async def presence_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'presence',
            'user_id': event['user_id'],
            'username': event['username'],
            'is_online': event['is_online'],
        }))

    @database_sync_to_async
    def set_user_online(self, user, online):
        from django.utils import timezone
        user.is_online = online
        if not online:
            user.last_seen = timezone.now()
        user.save(update_fields=['is_online', 'last_seen'] if not online else ['is_online'])

    @database_sync_to_async
    def save_message(self, conversation_id, user, contenu):
        from .models import Conversation, Message
        from django.contrib.auth import get_user_model
        User = get_user_model()
        conv = Conversation.objects.get(id=conversation_id)
        if not user.is_authenticated:
            user = User.objects.filter(role__in=['AGENT', 'ADMIN']).first()
        return Message.objects.create(
            conversation=conv,
            auteur=user,
            contenu=contenu,
        )
