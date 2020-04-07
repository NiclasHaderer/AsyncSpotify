"""
Main types
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (t_objects.py) is part of AsyncSpotify which is released under MIT.                   #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

from typing import Optional, List

from pydantic import BaseModel

from .t_general import Item, ExternalIds, Copyright, ExternalUrls, Image, Followers


class TTracks(BaseModel):
    href: Optional[str]
    items: Optional[List[Item]]
    limit: Optional[int]
    next: Optional[str]
    offset: Optional[int]
    previous: Optional[str]
    total: Optional[int]


########################################################################################################################

class TAritst(BaseModel):
    external_urls: Optional[ExternalUrls]
    followers: Optional[Followers]
    genres: Optional[List[str]]
    href: Optional[str]
    id: Optional[str]
    images: Optional[List[Image]]
    name: Optional[str]
    popularity: Optional[int]
    type: Optional[str]
    uri: Optional[str]


########################################################################################################################

class TAlbum(BaseModel):
    album_type: Optional[str]
    artists: Optional[List[TAritst]]
    available_markets: Optional[List[str]]
    copyrights: Optional[List[Copyright]]
    external_ids: Optional[ExternalIds]
    external_urls: Optional[ExternalUrls]
    genres: Optional[List]
    href: Optional[str]
    id: Optional[str]
    images: Optional[List[Image]]
    name: Optional[str]
    popularity: Optional[int]
    release_date: Optional[str]
    release_date_precision: Optional[str]
    tracks: Optional[TTracks]
    type: Optional[str]
    uri: Optional[str]


########################################################################################################################

class TAlbums(BaseModel):
    albums: Optional[List[TAlbum]]


########################################################################################################################

class TArtistAlbums(BaseModel):
    href: Optional[str]
    items: Optional[List[Item]]
    limit: Optional[int]
    next: Optional[str]
    offset: Optional[int]
    previous: Optional[str]
    total: Optional[int]


########################################################################################################################

class TTrack(BaseModel):
    album: Optional[TAlbum]
    artists: Optional[List[TAritst]]
    available_markets: Optional[List[str]]
    disc_number: Optional[int]
    duration_ms: Optional[int]
    explicit: Optional[bool]
    external_ids: Optional[ExternalIds]
    external_urls: Optional[ExternalUrls]
    href: Optional[str]
    id: Optional[str]
    name: Optional[str]
    popularity: Optional[int]
    preview_url: Optional[str]
    track_number: Optional[int]
    type: Optional[str]
    uri: Optional[str]


########################################################################################################################

class TTrackList(BaseModel):
    tracks: Optional[List[TTrack]]


class TArtistList(BaseModel):
    artists: Optional[List[TAritst]]
