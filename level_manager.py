class LevelManager:

    def __init__(self):
        self.rooms = {}
        self.current_room = None

    def load_room(self, room_name):
        self.current_room = self.rooms[room_name]

    def update(self, player):
        door = self.current_room.get_door_at(player.rect)

        if door:
            self.load_room(door["target"])