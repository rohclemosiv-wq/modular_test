# -*- coding: utf-8 -*-
"""
Utility functions and async geocoding
"""

import httpx
from pyproj import Transformer

async def get_address_coordinates(address:str):
    """
    Async geocoding using httpx
    """
    url = "https://api-adresse.data.gouv.fr/search/"
    params = {"q": address, "limit": 1}
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    if not data["features"]:
        raise ValueError(f"No result for address: {address}")
    lon, lat = data["features"][0]["geometry"]["coordinates"]
    return lon, lat


def lambert93_to_gps(x:float, y:float):
    """
    Convert Lambert‑93 coordinates to GPS using global transformer
    """
    lon, lat = _transformer.transform(x, y)
    return lon, lat

_transformer = Transformer.from_crs("epsg:2154", "epsg:4326", always_xy=True)
