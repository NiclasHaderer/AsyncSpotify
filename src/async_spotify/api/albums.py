from typing import List


class Albums:

    async def get_album(self, id: str, market: str = None):
        pass

    async def get_album_tracks(self, id: str, limit: int = None, offset: int = None, market: str = None):
        pass

    async def get_multiple_albums(self, id_list: List[str], market: str = None):
        pass
