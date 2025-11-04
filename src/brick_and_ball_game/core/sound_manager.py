from pyray import (
    init_audio_device,
    is_music_stream_playing,
    load_sound,
    load_music_stream,
    Music,
    play_music_stream,
    play_sound,
    set_music_volume,
    set_sound_volume,
    Sound,
    stop_music_stream,
    unload_music_stream,
    unload_sound,
    update_music_stream,
)


class SoundManager:
    current_bgm: str | None
    bgm: dict[str, Music]
    sfx: dict[str, Sound]

    def initialize(self) -> None:
        init_audio_device()
        self.sfx = {}
        self.current_bgm = None
        self.bgm = {}

    def unload(self) -> None:
        for _, sound in self.sfx.items():
            unload_sound(sound)
        self.sfx.clear()

        for _, bgm in self.bgm.items():
            unload_music_stream(bgm)
        self.bgm.clear()

    def load_sfx(self, sfx_name: str, path: str, volume: float = 1.0) -> None:
        if sfx_name in self.sfx:
            return
        self.sfx[sfx_name] = load_sound(path)
        set_sound_volume(self.sfx[sfx_name], volume)

    def play_sfx(self, sfx_name: str) -> None:
        if sfx_name not in self.sfx:
            return
        sound = self.sfx[sfx_name]
        play_sound(sound)

    def load_bgm(self, bgm_name: str, path: str, volume: float = 1.0) -> None:
        if bgm_name in self.bgm:
            return
        self.bgm[bgm_name] = load_music_stream(path)
        set_music_volume(self.bgm[bgm_name], volume)

    def play_bgm(self, bgm_name: str) -> None:
        # song not loaded yet
        if bgm_name not in self.bgm:
            return

        # song is currently playing
        if self.current_bgm == bgm_name and is_music_stream_playing(self.bgm[self.current_bgm]):
            return
        
        # stop current song
        if self.current_bgm is not None:
            stop_music_stream(self.bgm[self.current_bgm])
    
        # play song
        self.current_bgm = bgm_name
        play_music_stream(self.bgm[bgm_name])

    def update(self) -> None:
        if self.current_bgm is not None:
            update_music_stream(self.bgm[self.current_bgm])
