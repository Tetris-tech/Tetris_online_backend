import random
import uuid

from factory import Factory, Faker, SubFactory
from factory.alchemy import SQLAlchemyModelFactory

from src.game_session.models import TetrisGameSession, TetrominoKindEnum, GameStatusEnum
from src.user.factories import UserFactory


class TetrisGameSessionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = TetrisGameSession

    id = uuid.uuid4()
    player_id = SubFactory(UserFactory)
    field_width = Faker("random_int", min=10, max=20)
    field_height = Faker("random_int", min=20, max=40)
    grid = Faker("json", data_type="list", elements=["boolean", "boolean"])
    colors = Faker("json", data_type="list", elements=["#FFFFFF", "#000000"])
    current_piece = Faker(
        "json",
        data_type="dict",
        elements={
            "tetromino": {
                "type": random.choice(list(TetrominoKindEnum)),
                "matrix": [[True, False], [False, True]],
                "color": "#FF0000",
            },
            "position": {"x": 0, "y": 0},
        },
    )
    next_pieces = [random.choice(list(TetrominoKindEnum)) for _ in range(3)]
    score = Faker("random_int", min=0, max=1000)
    level = Faker("random_int", min=1, max=10)
    lines_cleared = Faker("random_int", min=0, max=100)
    status = random.choice(list(GameStatusEnum))
    last_updated = Faker("date_time")