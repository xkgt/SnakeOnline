from dataclasses import dataclass
from json import load, dump


@dataclass
class Config:
    fps: int = 60
    name: str = "Player"
    playsound: bool = True

    @classmethod
    def load(cls) -> "Config":
        obj = cls()
        try:
            with open("config.json", "r") as f:
                data = load(f)
                obj.__dict__.update(data)
        except Exception:
            ...
        return obj

    def save(self):
        with open("config.json", "w") as f:
            dump(self.__dict__, f, indent=4, ensure_ascii=False)
