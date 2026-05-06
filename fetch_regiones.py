import urllib.request, json
url = 'https://raw.githubusercontent.com/juanbrujo/listado-comunas-y-regiones-de-chile/master/comunas-regiones.json'
req = urllib.request.Request(url)
res = urllib.request.urlopen(req)
data = json.loads(res.read())
out = 'export const regionesData = [\n'
for r in data['regiones']:
    comunas_str = json.dumps(r['comunas'], ensure_ascii=False)
    out += f"  {{ nombre: '{r['region']}', comunas: {comunas_str} }},\n"
out += '];\n'
with open('vigildata-frontend/src/utils/regiones.js', 'w', encoding='utf-8') as f:
    f.write(out)
