from __future__ import annotations

from homescraper.ingest.arcgis import ArcGISFeatureLayerAdapter, ArcGISQueryConfig
from homescraper.sources import SourceRecord

LAKE_COUNTY_PARCELS = SourceRecord(
    source_name="Lake County Illinois GIS - Tax Parcel Information",
    jurisdiction="Lake County, Illinois",
    url="https://maps.lakecountyil.gov/arcgis/rest/services/GISMapping/WABParcels/MapServer/12",
    access_method="public ArcGIS REST query endpoint",
    update_frequency="weekly for the LakeCountyParcels published dataset; live service should be re-verified before production use",
    terms_url="https://catalog.data.gov/dataset/lakecountyparcels",
    robots_policy=None,
    api_available=True,
    cost="public; no paid credential required for the documented endpoint",
    reliability=None,
    legal_confidence=None,
)

LAKE_COUNTY_QUERY = ArcGISQueryConfig(
    layer_url=LAKE_COUNTY_PARCELS.url,
    out_fields=(
        "PIN",
        "situs_addr_line_1",
        "situs_addr_line_2",
        "situs_addr_line_3",
        "situs_addr_city",
        "situs_addr_zip_legdat",
        "taxpayer_name",
        "taxpayer_addr_line_1",
        "taxpayer_addr_line_2",
        "taxpayer_addr_line_3",
        "assess_total_assyr",
        "MUNI_NAME",
    ),
)


def lake_county_adapter() -> ArcGISFeatureLayerAdapter:
    return ArcGISFeatureLayerAdapter(LAKE_COUNTY_PARCELS, LAKE_COUNTY_QUERY)
