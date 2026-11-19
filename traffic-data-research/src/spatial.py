"""Spatial safeguards. This run does not compute metric buffers or crash risk."""
import re,unicodedata
def normalize_region(value):
    return re.sub(r'\s+',' ',unicodedata.normalize('NFC',value)).strip()
def chainage_metres(value):
    m=re.fullmatch(r'Km(\d+)\+(\d{1,3})',value.strip(),re.I)
    if not m: raise ValueError('Ambiguous chainage; requires manual validation')
    # Abbreviated +00 deliberately rejected: source may mean +000, not +0.
    if len(m[2])!=3: raise ValueError('Abbreviated metres not normalized automatically')
    return int(m[1])*1000+int(m[2])
def require_metric_crs(epsg):
    if epsg not in [32648,32649]: raise ValueError('Use locally suitable metric CRS EPSG:32648/32649; never EPSG:4326 for lengths')
    return epsg
def rate_per_100k(count,population):
    if count<0 or population<=0: raise ValueError('Invalid numerator/denominator')
    return count/population*100000
