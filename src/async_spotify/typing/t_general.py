# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (album.py) is part of AsyncSpotify which is released under MIT.                       #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

from typing import List, Optional

from pydantic import BaseModel


class ExternalUrls(BaseModel):
    spotify: Optional[str]


class Artist(BaseModel):
    external_urls: Optional[ExternalUrls]
    href: Optional[str]
    id: Optional[str]
    name: Optional[str]
    type: Optional[str]
    uri: Optional[str]


class Copyright(BaseModel):
    text: Optional[str]
    type: Optional[str]


class ExternalIds(BaseModel):
    upc: Optional[str]


class Image(BaseModel):
    height: Optional[int]
    url: Optional[str]
    width: Optional[int]


class Item(BaseModel):
    artists: Optional[List[Artist]]
    available_markets: Optional[List[str]]
    disc_number: Optional[int]
    duration_ms: Optional[int]
    explicit: Optional[bool]
    external_urls: Optional[ExternalUrls]
    href: Optional[str]
    id: Optional[str]
    name: Optional[str]
    preview_url: Optional[str]
    track_number: Optional[int]
    type: Optional[str]
    uri: Optional[str]


class Followers(BaseModel):
    href: Optional[str]
    total: Optional[int]


