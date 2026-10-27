# County selection: first Northern Illinois market

Checked: 2026-10-27

## Decision

**Lake County is the first county adapter target.**

This is a product/engineering decision, not a claim that Lake County has the best investment returns in Illinois. The selection is based on the combination of local operating relevance, documented public data availability, and a clean path to a reusable statewide adapter architecture.

## Evidence

| Factor | Lake | DuPage | Kane | McHenry | Will |
|---|---|---|---|---|---|
| 2025 population | 719,339 | 934,298 | 525,757 | 317,751 | 712,253 |
| Public parcel source verified | Yes | Yes | Yes | Yes | Yes |
| Public ArcGIS/service path verified | Yes | Yes | Yes | Yes | Yes |
| First implementation fit | **Strong** | Strong | Strong | Strong | Strong |

Population figures are July 1, 2025 estimates from the cited county comparison source. Parcel-service availability is based on county/public GIS documentation and the live service metadata reviewed during research.

### Why Lake wins for the first implementation

1. **Local operating fit.** The initial operator is in Lake County, so the first production workflow can be validated in the market where the system will actually be used.
2. **Current parcel dataset.** Data.gov lists LakeCountyParcels as public, with a weekly update frequency and downloadable CSV, XLSX, GeoJSON, KML, Shapefile, GeoPackage, SQLite geodatabase, and ArcGIS GeoService resources. The catalog record was updated October 11, 2026.
3. **Public parcel service exposes acquisition-relevant fields.** Lake County's Tax Parcel Information service exposes PIN, situs address, taxpayer name and mailing address components, assessed values, municipality, parcel area, and other fields. The service supports JSON/GeoJSON/PBF queries and pagination.
4. **Expansion path.** The adapter is being built against a generic ArcGIS source interface rather than embedding Lake County assumptions into the rest of the application. That lets the same ingestion contract support other Illinois counties.
5. **Regional comparability.** CMAP maintains county and municipal data across the seven-county northeastern Illinois region: Cook, DuPage, Kane, Kendall, Lake, McHenry, and Will. This provides a consistent future enrichment layer across the initial expansion region.

## Important limitations

- This research does **not** establish which county has the highest distressed-property yield, investor competition, foreclosure volume, assignment volume, or expected return. Those require additional datasets and analysis.
- DuPage, Kane, McHenry, and Will all have credible public parcel/GIS infrastructure, so Lake is not selected because the alternatives lack data.
- Lake County's public GIS documentation includes ordinary parcel/GIS disclaimers; parcel geometry is not a substitute for an on-site survey.
- Terms, access policies, and data vintages must be rechecked before production automation.

## Sources

- Lake County GIS: https://www.lakecountyil.gov/636/GISMaps
- Lake County parcel dataset catalog: https://catalog.data.gov/dataset/lakecountyparcels
- Lake County parcel service metadata: https://maps.lakecountyil.gov/arcgis/rest/services/GISMapping/WABParcels/MapServer
- Kane County GIS FAQ/open-data documentation: https://www.kanecountyil.gov/Pages/gis-faq.aspx
- McHenry County GIS: https://www.mchenrycountyil.gov/departments/geographic-information-system-gis
- Will County GIS data: https://willcounty.gov/County-Offices/Administration/GIS-Division/Data/Vector
- CMAP northeastern Illinois community data: https://cmap.illinois.gov/data/community-data-snapshots/
- 2025 county population comparison used for relative scale: https://uspopulationdata.com/states/illinois/counties/

## Next county sequence

After Lake's ingestion and entity-resolution path are stable, evaluate **Kane, McHenry, Will, DuPage, Cook, and Kendall** using the same documented-source scorecard. Do not hard-code that order as an investment ranking.
