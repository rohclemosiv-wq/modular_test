# -*- coding: utf-8 -*-
"""
Service class for loading CSV and computing nearest provider coverage
"""

import csv
import os
import math
from utils import lambert93_to_gps


class CoverageService(object):
    """
    Class handling CSV loading and nearest coverage queries
    """

    def __init__(self, csv_path:str):
        """
        Initialize service with CSV file
        """
        self._sites = []
        if not os.path.isfile(csv_path):
            raise FileNotFoundError(f"Coverage CSV file not found: {csv_path}")
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                try:
                    provider = row["Operateur"]
                    x = float(row["x"])
                    y = float(row["y"])
        
                    def to_bool(v):
                        if isinstance(v, bool):
                            return v
                        v_str = str(v).strip().lower()
                        return v_str in ("true", "1", "yes")
        
                    coverage_2g = to_bool(row.get("2G", False))
                    coverage_3g = to_bool(row.get("3G", False))
                    coverage_4g = to_bool(row.get("4G", False))
        
                    lon, lat = lambert93_to_gps(x, y)
                    self._sites.append({
                        "provider": provider,
                        "lon": lon,
                        "lat": lat,
                        "coverage": {"2G": coverage_2g,
                                     "3G": coverage_3g,
                                     "4G": coverage_4g},
                    })
                except Exception as e:
                    print(e)
                #except (KeyError, ValueError):
                    #print(f"Error: {(str(KeyError), str(ValueError))}")
                    continue

    def _haversine(self, lon1:float, lat1:float, lon2:float, lat2:float):
        """
        Haversine distance in metres
        """
        R = 6371000  # Earth radius in metres
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        d_phi = math.radians(lat2 - lat1)
        d_lambda = math.radians(lon2 - lon1)
        a = (math.sin(d_phi / 2) ** 2 +
             math.cos(phi1) * math.cos(phi2) *
             math.sin(d_lambda / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def get_nearest_coverage(self, lon:float, lat:float):
        """
        Return nearest provider coverage for a GPS point
        """
        best_by_provider = {}
        for site in self._sites:
            distance = self._haversine(lon, lat, site["lon"], site["lat"])
            provider = site["provider"]
            print(f"{distance,provider}")
            
            if (provider not in best_by_provider) or (distance < best_by_provider[provider]["distance"]):
                best_by_provider[provider] = {"distance": distance,
                                              "coverage": site["coverage"]}
        # Strip distances and return only coverage dicts
        return {prov: info["coverage"] for prov, info in best_by_provider.items()}

