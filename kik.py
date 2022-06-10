

from distutils.log import error
from paho.mqtt import client as mqtt_client
from enum import Enum

class STATUS(Enum):
    WAITINGFORPLAYERS = 1
    GAME = 2

broker = '192.168.1.104'
port = 1883
client_id = f'RPi_python_Client'

class Board:
    def __init__(self):
        self.board =    [-1, -1, -1, 
                        -1, -1, -1,
                        -1, -1, -1]

    def putMarker(self, pos, player):
        if not (player == 1 or player == 2):
            return "Wrong player identificator"
        if self.board[pos] == -1:
            self.board[pos] = player
            return "move recorded"
        else: 
            return "position taken"
    
    def checkIfGameFinished(self):
        #row
        for i in range(3):
            if self.board[i*3] != -1 and self.board[i*3] == self.board[i*3+1] == self.board[i*3+2]:
                return self.board[i*3]
        #col
        for i in range(3):
            if self.board[i] != -1 and self.board[i] == self.board[i*3+3] == self.board[i*3+6]:
                return self.board[i]
        #diagonals
        if self.board[0] != -1 and ((self.board[0] == self.board[4] == self.board[8]) or (self.board[2] == self.board[4] == self.board[6])):
            return self.board[4]
        return False
    
    def clearBoard(self):
        self.board =    [-1, -1, -1, 
                        -1, -1, -1,
                        -1, -1, -1]

class Game:
    def __init__(self, board):
        self.board = Board()
        self.turn = 1
        self.playersCount = 1

    def putMarker(self, pos, playerId):
        if self.turn != playerId:
            return 'Not your turn'
        if playerId < 1 and playerId > 2:
            return 'Wrong player Id'
        retVal = self.board.putMarker(pos, playerId)
        winner = self.board.checkIfGameFinished()
        if winner:
            self.board.clearBoard()
            return 'Player' + str(winner) + ' won!'
        else:
            self.turn = self.turn%2+1
            return retVal

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
#    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

game = Game()


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        msgString = msg.payload.decode()
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        
        if msgString is 'subscribed':
            if game.playersCount < 2:
                game.playersCount = 2
                client.publish("gameserver", game.playersCount)
            else:
                client.publish("gameserver", "player" + str(game.turn))


    client.subscribe('gameclients')
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.publish("gameserver", game.playersCount)
    client.loop_forever()


if __name__ == '__main__':
    run()

    
