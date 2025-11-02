from pyray import init_audio_device, load_sound, play_sound, set_sound_volume, Sound, unload_sound


class SoundManager:
    sfx: dict[str, Sound]

    def initialize(self) -> None:
        init_audio_device()
        self.sfx = {}

    def unload(self) -> None:
        for _, sound in self.sfx.items():
            unload_sound(sound)
        self.sfx.clear()

    def load_sfx(self, sfx_name: str, path: str, volume: float = 1.0) -> None:
        if sfx_name in self.sfx:
            sound: Sound = self.sfx[sfx_name]
            unload_sound(sound)
        self.sfx[sfx_name] = load_sound(path)
        set_sound_volume(self.sfx[sfx_name], volume)

    def play_sfx(self, sfx_name: str) -> None:
        if sfx_name not in self.sfx:
            return
        sound = self.sfx[sfx_name]
        play_sound(sound)
