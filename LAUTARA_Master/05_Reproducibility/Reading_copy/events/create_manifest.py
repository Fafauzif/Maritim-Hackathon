"""Build case chronology and calculate the police-coordinate discrepancy."""
import csv
import json
from math import asin, atan2, cos, degrees, radians, sin, sqrt
from pathlib import Path

base = Path(__file__).resolve().parent
sources = {
    "T_KKP": "https://kkp.go.id/djpsdkp/kkp-hentikan-aktivitas-pengerukan-pasir-di-perairan-jakarta65c30567edc3d/detail.html",
    "T_LPSPL": "https://kkp.go.id/storage/AkuntabilitasKinerja/1119/document-akuntabilitas-kinerja-667b778530efeLaporan%20Kinerja%20LPSPL%20SERANG%20Tahun%202023.pdf",
    "T_WALHI": "https://www.walhi.or.id/kapal-vox-maxima-kembali-beroperasi-di-perairan-pulau-tunda-dan-teluk-jakarta-koalisi-ngo-desak-penegakan-hukum-lingkungan",
    "T_BAPENDA_JAN": "https://www.bantenraya.com/daerah/11692765/ternyata-tidak-bayar-pajak-pemkab-serang-kecolongan-soal-penambangan-pasir-laut-2",
    "T_BAPENDA_MAR": "https://www.bantenraya.com/daerah/12277769/perusahaan-tambang-pasir-di-kabupaten-serang-cicil-pembayaran-pajak-rp45-miliar",
    "K_BOSKALIS": "https://boskalis.com/media/vvqpszsv/makassar-new-port.pdf",
    "K_WALHI": "https://www.greenpeace.org/static/planet4-indonesia-stateless/2021/03/17185db9-gp-spermonde-report-v8.pdf",
    "K_POLICE": "https://tribratanews.polri.go.id/article/polda-sulsel-amankan-12-orang-diduga-pelaku-pengrusakan-kapal-boskalis-int-15716",
    "K_WALHI_RETRO": "https://www.walhi.or.id/uploads/buku/Policy%20Paper%20-%20Jaring%20Nusa%20KTI%20%281%29.pdf",
    "K_LAW_REVIEW": "https://doi.org/10.30872/mulrev.v6i2.621",
    "K_DPR": "https://berkas.dpr.go.id/akd/dokumen/komisi4-Laporan-Kunjungan-Kerja-Komisi-IV-DPR-Reses-Masa-Persidangan-IV-Tahun-Sidang-2023-2024-ke-Provinsi-Sulawesi-Selatan-1721114899.pdf",
    "K_WALHI_PRICE": "https://walhisulsel.or.id/4037-pernyataan-pers-atas-dugaan-praktik-penyimpangan-penetapan-harga-jual-hasil-pertambangan-pasir-laut-tahun-2020-di-perairan-galesong-kabupaten-takalar/",
    "T_COAST_STUDY": "https://doi.org/10.2478/cjf-2023-0009",
    "T_TRANSECT": "https://doi.org/10.22373/kenanga.v5i2.8470",
}
fields = ("event_id","site","event_start_local","event_end_local","event_precision","timezone","public_evidence_date_or_period","release_precision","contemporary_operational_availability","event_type","evidence_type","confirmed_or_reported_fact","location_support","inferential_boundary","source_key")
rows = [
 ("T1","Tunda","2021-07","2021-12","month range","Asia/Jakarta","2023","year","No as a publication, prior field availability not documented","reef study window","peer-reviewed survey and model","Line-intercept reef survey and sediment-transport model near a historical mining area","Historical WIUP and reef stations, no event-linked track","Model outputs are scenarios and surveys do not establish 2023 causation","T_COAST_STUDY"),
 ("T2","Tunda","2021-11","2022-01","month range","Asia/Jakarta","2025","year","No as a publication, prior field availability not documented","reef study window","peer-reviewed site observations","Archived sampling reported mean live coral cover 16.92 percent across four purposive stations","Station-level sample, publication years after survey","No causal or island-wide estimate, no comparison across dates with standardized methods","T_TRANSECT"),
 ("T3","Tunda","2023-10-27","2023-10-27","local day","Asia/Jakarta","2023-10-29","local day","Patrol observed action on event day, public release two calendar dates later","patrol stop and inspection","official operational report","HIU 06 stopped and inspected VOX MAXIMA, reported approximately 24000 m3 of sand onboard, then secured ship/equipment/documents/cargo during inquiry","Tunda source and Tanjung Priok destination were the authority's reported hypotheses, no extraction coordinate or footprint","Contains evidence of cargo at inspection. No exact event hour, final outcome, confirmed extraction location or net environmental effect","T_KKP"),
 ("T4","Tunda","2023-10-27","2023-10-27","local day","Asia/Jakarta","2023 performance report","report year","Joint monitoring action day known, public availability of report at the time not shown","government monitoring and evidence gathering","official performance disclosure","Loka PSPL Serang DKI working unit and Pangkalan PSDKP Jakarta jointly monitored/researched Tunda sand allegations","Island waters as jurisdictional area","Do not treat this separate account of official action as a second independent dredging detection","T_LPSPL"),
 ("T5","Tunda","2023-11-18","2023-11-22","day range as reported","Asia/Jakarta","2023-11-23","publication day, statement dated November 22","Fishers report observations within interval, regulator intake timing unknown","reported vessel passage","community accounts in coalition release","Fishers reported a loaded vessel passing Pulau Pari. Coalition attributed activity to Tunda and Tanjung Priok","Reported observation location Pulau Pari, source assignment unverified","No location of extraction independently established; no basis for ecological or precise volume claims","T_WALHI"),
 ("T6","Tunda","2024-01-28","2024-01-28","date of quote","Asia/Jakarta","2024-01-28","local day","Statement made months after initial stop","district tax/permit account","local media quoting district revenue official","Official said tax receipts had not appeared and described information that HLS was exploring but awaiting renewal","Around Pulau Tunda, no verified permit geometry","A January statement about tax and permit status. Separate from KKP inquiry and later reported payments","T_BAPENDA_JAN"),
 ("T7","Tunda","2024-01","2024-02","tax period as reported","Asia/Jakarta","2024-03-26","local day","March reporting, no contemporaneous inspection implication","district tax/payment account","local media quoting district revenue official","District official reported roughly IDR 4.5 billion paid in early March by two firms for January–February extraction/sales period","Operations around Pulau Tunda as reported, two-firm total","Payment is not proof of clearance or VOX MAXIMA activity, environmental follow-up or final case disposition","T_BAPENDA_MAR"),
 ("K1","Kodingareng","2020-02","2020-10","month range","Asia/Makassar","undated contractor factsheet","unknown","Project scale later documented; operating log availability at event unverified","industrial deployment","contractor project factsheet","Phases 1B–1C Makassar New Port. Queen of the Netherlands deployed February–October 2020 and transported about 11 million m3 of marine sand","Regional borrow areas, not dated tracks or polygon","Cargo total is contractor-reported for those phases and cannot be allocated to a single ground or day","K_BOSKALIS"),
 ("K2","Kodingareng","2020-02-12","2020-02-12","local day as reported","Asia/Makassar","2021 advocacy report","year","Harbour undertaking reported as existing on day; original issue document not retrieved","harbour notice","retrospective coalition report citing harbourmaster","A February 12 harbourmaster notice described vessel presence and intended borrow/reclamation works","Bone Malonjo/Bone Ma'lonjo named in plans, no authoritative polygon recovered","Treat notice contents as reported, not independently authenticated","K_WALHI"),
 ("K3","Kodingareng","2020-02-13","2020-02-13","local day as reported","Asia/Makassar","2021 advocacy report","year","Operation reportedly started on this day, per retrospective publication","reported dredge onset","coalition field and tracking accounts","Coalition reported first extraction February 13 near the Spermonde grounds, citing investigation and vessel tracking","Copong Lompo, Copong Ca'di, Bonema'lonjo, Pungangrong are reported grounds","Date anchor, not vessel-by-hour log or proof all sites were active","K_WALHI"),
 ("K4","Kodingareng","2020-09-12T06:00:00+08:00","2020-09-12T07:00:00+08:00","times in police report, date numeric; weekday error in source","Asia/Makassar","2020-09-13T13:30:00","site display does not identify publication timezone","Police account describes contemporaneous movements, publication after them","named vessel movement and conflict","official police account","Reported departure Makassar New Port 06:00 and arrival at named Taka Copong quarry 07:00 local, followed by a police response to a confrontation","Published coordinates conflict with written offshore distance; excluded from scientific source geometry","Vessel presence and police confrontation reporting, not a verified borrow polygon or environmental determination","K_POLICE"),
 ("K5","Kodingareng","2020-10-26","2020-10-26","reported local day","Asia/Makassar","retrospective policy paper","year only/unverified posting day","Later report, exact timing not contemporaneously verified","reported last day","coalition policy paper","Later coalition places end of reported activity in October 2020, specifying October 26","Regional Spermonde/Galesong case","Contractor corroborates October month only. Keep October 26 as lower-confidence candidate end date, not proof of no operation afterward","K_WALHI_RETRO"),
 ("K6","Kodingareng","2020","2020","year of reported concerns","Asia/Makassar","2021-12-30","journal publication day","Later interviews/observational inquiry, raw catches/log timestamps not available","fishing-ground and rights evidence","peer-reviewed legal field study","Interviews and observations describe fishers' reports of reduced catch and livelihood concerns in the case","Named, used grounds described; site polygons not produced by the paper","No matched catch/effort counterfactual or calibrated measurement of environmental dose","K_LAW_REVIEW"),
 ("K7","Kodingareng","2020","2024-05-10","follow-up timeframe, exact examination dates absent","Asia/Makassar","2024 field visit report","year, visit dated May 6–10","Public disclosure years after primary work; cannot place each examination on decision day","regulatory follow-up","official parliamentary report relaying Satwas SDKP","SDKP examined three sand businesses and two reclamation businesses, heard fishers, and reported no violations in this follow-up. Conflict-reduction efforts were reported","Sangkarang and Galesong, no geospatial annex to reported follow-up","Closed statement about this regulatory follow-up only, no quantified ecological outcome or port-project-wide determination","K_DPR"),
 ("K8","Kodingareng","2023","2023","year of statement","Asia/Makassar","2023","year","Unrelated later inquiry cannot inform 2020 operations in real time","separate fiscal/legal issue","WALHI reporting about suspects in price determination case","Coalition mentions a case over alleged irregular pricing of sand against two companies","Galesong area, no environmental monitoring geography","Different allegation, separate forum and outcome not verified. Do not combine with SDKP follow-up or ecological exposure test","K_WALHI_PRICE"),
]
with (base/"event_register.csv").open("w",encoding="utf-8",newline="") as f:
    writer = csv.writer(f)
    writer.writerow((*fields,"source_url"))
    writer.writerows((*row,sources[row[-1]]) for row in rows)
tgt = (-5.14905,119.26473)
police = (-(5+9.470/60),119+14.789/60)
lat1,lon1 = map(radians,tgt)
lat2,lon2 = map(radians,police)
lat_diff,lon_diff = lat2-lat1,lon2-lon1
great_circle = 6371.0088*2*asin(sqrt(sin(lat_diff/2)**2+cos(lat1)*cos(lat2)*sin(lon_diff/2)**2))
bearing = (degrees(atan2(sin(lon_diff)*cos(lat2),cos(lat1)*sin(lat2)-sin(lat1)*cos(lat2)*cos(lon_diff)))+360)%360
(base/"coordinate_conflict.json").write_text(json.dumps({
    "island_anchor_lat_lon":tgt, "police_report_coordinate_lat_lon":police,
    "haversine_distance_km":great_circle, "nautical_miles_1852m":great_circle/1.852,
    "bearing_degrees":bearing, "narrative_distance_police_mil":11,
    "narrative_distance_walhi_mil":9, "include_as_source_geometry":False,
    "police_source":sources["K_POLICE"],"walhi_source":sources["K_WALHI"],
    "island_anchor_source":"https://mapcarta.com/16118912",
},indent=2)+"\n",encoding="utf-8")
