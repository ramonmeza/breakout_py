from pyray import (
    load_texture,
    Texture,
    unload_texture,
)


class TextureManager:
    textures: dict[str, Texture]

    def initialize(self) -> None:
        self.textures = {}

    def unload(self) -> None:
        for _, texture in self.textures.items():
            unload_texture(texture)
        self.textures.clear()

    def load_texture(self, texture_name: str, path: str) -> None:
        if texture_name in self.textures:
            texture: Texture = self.textures[texture_name]
            unload_texture(texture)
        self.textures[texture_name] = load_texture(path)

    def get_texture(self, texture_name: str) -> Texture:
        return self.textures[texture_name]
