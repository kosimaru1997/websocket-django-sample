import json
import time

import boto3
from boto3.dynamodb.conditions import Key
from ninja import Router

from app.chat.schema.GetChatRoomResponse import GetChatRoomResponse, ChatRoom
from app.chat.schema.createChatRequest import CreateChatRequest
from app.myweb.settings import WEBSOCKET_API

chat_router = Router(tags=["chat"])


@chat_router.get("/", response=GetChatRoomResponse)
def get_chat_room_list(request):
    #getItemメソッドの呼び出し(主キー検索)
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')
    table = dynamodb.Table('dev-UserChatRoomRelation')

    response = table.query(
        KeyConditionExpression=Key('user_id').eq('1'),
    )
    chat_room_list = []
    for item in response["Items"]:
        print(item)
        chat_room = ChatRoom(user_id=item['user_id'],
                             room_id=item['room_id'],
                             last_message=item['last_message'],
                             unchecked_count=item['unchecked_count'],
                             updated_at=item['updated_at'])
        chat_room_list.append(chat_room)

    chat_room_res = GetChatRoomResponse(room_list=chat_room_list)
    return chat_room_res

@chat_router.post("/")
def create_chat_room(request):
    current_time_int = int(time.time() * 1000)

    # DynamoDBクライアントの初期化
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')
    # chat_room_table = dynamodb.Table('dev-ChatRoom')
    user_chat_room_relation_table = dynamodb.Table('dev-UserChatRoomRelation')

    # chat_room_table.put_item(
    #     Item={
    #         'room_id': "1111",
    #         'last_message': None,
    #         'created_at': current_time_int,
    #         'updated_at': current_time_int,
    #     }
    # )

    user_chat_room_relation_table.put_item(
        Item={
            'user_id': "1",
            'updated_at': current_time_int,
            'room_id': "1",
            'created_at': current_time_int,
            'last_message': None,
            'unchecked_count': 0,
        }
    )
    user_chat_room_relation_table.put_item(
        Item={
            'user_id': "22",
            'updated_at': current_time_int,
            'room_id': "1",
            'created_at': current_time_int,
            'last_message': None,
            'unchecked_count': 0
        }
    )

    pass

@chat_router.get("/{room_id}")
def get_chat_room(request, room_id):
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')
    table = dynamodb.Table('dev-Chat')
    response = table.query(
        KeyConditionExpression=Key('room_id').eq(room_id),
        # ScanIndexForward=False
    )
    return response['Items']

@chat_router.post("/{room_id}")
def create_chat(request, room_id, createChatRequest: CreateChatRequest):
    current_time_int = int(time.time() * 1000)

    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')
    chat_table = dynamodb.Table('dev-Chat')
    message_dict = {
                'room_id': room_id,
                'created_at': current_time_int,
                'user_id': createChatRequest.user_id,
                'message': createChatRequest.message,
                'message_id': createChatRequest.message_id,
            }
    try:
        response = chat_table.put_item(
            Item=message_dict
        )
    except Exception as e:
        print(e)
        return 500

    chat_room_table = dynamodb.Table('dev-UserChatRoomRelation')
    response = chat_room_table.query(
        IndexName='RoomIndex',
        KeyConditionExpression=Key('room_id').eq(room_id),
    )

    print(response)
    user_id_list = []
    for item in response['Items']:
        user_id = item['user_id']
        updated_at = item['updated_at']
        if user_id != '11':
            user_id_list.append(item['user_id'])


    connection_id_list = []
    for user_id in user_id_list:
        connection_table = dynamodb.Table('dev-ConnectionsTable')
        response = connection_table.query(
            IndexName='UserIdIndex',
            KeyConditionExpression=Key('user_id').eq(user_id),
        )
        for item in response['Items']:
            connection_id_list.append(item['connection_id'])

    message_json = json.dumps(message_dict).encode('utf-8')
    for connection_id in connection_id_list:
        # API Gateway Management APIクライアントを作成
        client = boto3.client('apigatewaymanagementapi',
                              region_name='ap-northeast-1',
                              endpoint_url=WEBSOCKET_API)
        try:
            # メッセージを指定されたコネクションに送信
            response = client.post_to_connection(
                ConnectionId=connection_id,
                Data=message_json
            )
            print("Message sent successfully.")
        except client.exceptions.GoneException:
            print("Connection is no longer available.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")


    return
