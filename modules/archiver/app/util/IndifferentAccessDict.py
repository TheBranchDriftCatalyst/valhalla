class IndifferentAccessDict(dict):
    def __getitem__(self, key):
        return super().__getitem__(str(key))