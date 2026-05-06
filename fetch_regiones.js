const http = require('https');
const fs = require('fs');

const url = 'https://raw.githubusercontent.com/juanbrujo/listado-comunas-y-regiones-de-chile/master/comunas-regiones.json'; // 404
const alternateUrl = 'https://gist.githubusercontent.com/juanbrujo/0fd2f4d12733aeeaeb67/raw';
// Let's just create a list of regions and comunas directly since we can't find a stable URL here, wait, let's try getting it from an API: https://apis.digital.gob.cl/dpa/regiones

process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";
async function getRegiones() {
  try {
    const resRegiones = await fetch('https://apis.digital.gob.cl/dpa/regiones');
    const regiones = await resRegiones.json();
    let dataMap = [];
    for (let r of regiones) {
      const resComunas = await fetch(`https://apis.digital.gob.cl/dpa/regiones/${r.codigo}/comunas`);
      const comunas = await resComunas.json();
      dataMap.push({
        nombre: r.nombre,
        comunas: comunas.map(c => c.nombre)
      });
    }
    fs.writeFileSync('vigildata-frontend/src/utils/regiones.js', 'export const regionesData = ' + JSON.stringify(dataMap, null, 2) + ';');
    console.log('Saved regiones.js');
  } catch (e) {
    console.error(e);
  }
}
getRegiones();
