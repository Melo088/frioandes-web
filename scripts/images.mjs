// Pantallas del sistema de diseño en WebP. Los diagramas salen de diagrams/ en SVG.
import sharp from 'sharp';
const D='/home/melo/8thSem/auto/frioandes/planning/docs/';
const m={
'torre':'design/lamina/pantalla-torre-noche.png',
'portal':'design/lamina/pantalla-portal-escritorio.png'};
for (const [k,v] of Object.entries(m)){
 const i=await sharp(D+v).metadata();
 await sharp(D+v).resize({width:2200,withoutEnlargement:true}).webp({quality:82}).toFile(`/home/melo/projects/frioandes-web/public/img/${k}.webp`);
 console.log(k,i.width,i.height);
}
