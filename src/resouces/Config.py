from dataclasses import dataclass
from json import load, dump


@dataclass
class Config:
    fps: int = 60
    savepath: str = "config.json"
    name: str = "Player"
    playsound: bool = True

    @classmethod
    def load(cls, path) -> "Config":
        obj = cls()
        try:
            with open(path, "r") as f:
                data = load(f)
                obj.__dict__.update(data)
        except Exception:
            ...
        obj.savepath = path
        return obj

    def save(self):
        with open(self.savepath, "w") as f:
            dump(self.__dict__, f, indent=4, ensure_ascii=False)
