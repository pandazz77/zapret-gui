from dataclasses import dataclass, asdict
import json
import os

FILENAME = "settings.json"
_settings_dir: str = None
_filepath: str = None

@dataclass
class Settings:
    preffered_bins_provider: str
    preffered_strategy_provider: str
    preffered_strategy: str = None

    @staticmethod
    def setup(dir:str):
        global _settings_dir, _filepath
        _settings_dir = dir
        _filepath = os.path.join(_settings_dir,FILENAME)

    def load(self):
        if not os.path.exists(_filepath):
            self.save()
            return
        
        with open(_filepath,"r") as f:
            data = json.load(f)

        instance_vars = vars(self)
        for key in instance_vars:
            if key in data:
                instance_vars[key] = data[key]

    def save(self):
        settings_dict = asdict(self)
        with open(_filepath, "w", encoding='utf-8') as f:
            json.dump(settings_dict, f, ensure_ascii=False, indent=4)