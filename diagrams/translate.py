"""Copia en inglés de los diagramas que ya están bien dibujados.

Lee los .drawio de diagrams/src, reemplaza cada etiqueta por su traducción y
escribe el resultado en diagrams/out. Falla si queda un texto sin traducir.

    python3 diagrams/translate.py
"""
import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

EN = {
    # firewall-9-p2-puntos-de-control
    'Cali': 'Cali',
    'Ocho centros': 'Eight regional centers',
    'Hub · vnet-hub 10.100.0.0/23': 'Hub · vnet-hub 10.100.0.0/23',
    'Producción · vnet-prod 10.101.0.0/21': 'Production · vnet-prod 10.101.0.0/21',
    'Usuarios<br>10.20.0.0/24': 'Users<br>10.20.0.0/24',
    'Servidores: aplicación,<br>base y archivo<br>10.20.1 a 10.20.3': 'Servers: application,<br>database and archive<br>10.20.1 to 10.20.3',
    'Firewall<br>de Cali': 'Cali<br>firewall',
    'Usuarios<br>10.3X.0.0/24': 'Users<br>10.3X.0.0/24',
    'Sensores de cuartos<br>fríos 10.3X.1.0/24': 'Cold room sensors<br>10.3X.1.0/24',
    'Equipo VPN<br>del centro': 'Center<br>VPN device',
    'Camiones<br>(red móvil del operador)': 'Trucks<br>(carrier mobile network)',
    'Internet': 'Internet',
    'VPN Gateway': 'VPN Gateway',
    'Azure Firewall Standard': 'Azure Firewall Standard',
    'Política': 'Policy',
    'Grupos 200 y 300: estables.<br>Grupos 400 y 500: temporales de la convivencia.<br>Sin regla: se rechaza y se registra.': 'Groups 200 and 300: permanent.<br>Groups 400 and 500: temporary, during coexistence.<br>No matching rule: denied and logged.',
    'Bastion': 'Bastion',
    'DNS Private<br>Resolver': 'DNS Private<br>Resolver',
    'Torre · snet-app-torre': 'Control tower · snet-app-torre',
    'FW-201: 443 desde la red corporativa': 'FW-201: 443 from the corporate network',
    'Ingesta · snet-ingest': 'Ingestion · snet-ingest',
    'FW-204: 8883, 5671 y 443': 'FW-204: 8883, 5671 and 443',
    'Integración con Cali': 'Integration with Cali',
    'FW-501 a 505 (temporales)': 'FW-501 to 505 (temporary)',
    'Archivo · snet-archive': 'Archive · snet-archive',
    'Copia desde Cali fuera del firewall.<br>NSG temporal: solo 10.20.3.0/24': 'Copy from Cali outside the firewall.<br>Temporary NSG: only 10.20.3.0/24',
    'Datos · snet-data y snet-data-pe': 'Data · snet-data and snet-data-pe',
    'NSG: solo aplicaciones y Fabric': 'NSG: applications and Fabric only',
    'Analítica · snet-fabric-egress': 'Analytics · snet-fabric-egress',
    'Lee solo la base, sin internet': 'Reads only the database, no internet',
    'Portal · snet-ingress': 'Portal · snet-ingress',
    'WAF v2': 'WAF v2',
    'Portal · snet-app-portal': 'Portal · snet-app-portal',
    'NSG: solo desde snet-ingress': 'NSG: only from snet-ingress',
    'Administración · snet-admin': 'Administration · snet-admin',
    'NSG: 22 y 3389 desde Bastion': 'NSG: 22 and 3389 from Bastion',
    'IoT Hub y DPS, endpoints públicos<br>(Central US)': 'IoT Hub and DPS, public endpoints<br>(Central US)',
    'Telemetría · snet-telemetry-func': 'Telemetry · snet-telemetry-func',
    'Función notificadora': 'Notifier function',
    'NSG de la torre: 443 desde esta subred, solo para entregar alertas.<br>Salida por el firewall: FW-319 a 321 (Teams, correo y SMS).': 'Tower NSG: 443 from this subnet, only to deliver alerts.<br>Outbound through the firewall: FW-319 to 321 (Teams, email and SMS).',
    '4 túneles,<br>2 proveedores': '4 tunnels,<br>2 providers',
    '2 túneles<br>por centro': '2 tunnels<br>per center',
    'Todo lo que entra<br>por la VPN': 'Everything arriving<br>through the VPN',
    'FW-301 a 330: salida a internet': 'FW-301 to 330: outbound to internet',
    'WAF: 443': 'WAF: 443',
    '443': '443',
    'Bastion: NSG, 22 y 3389': 'Bastion: NSG, 22 and 3389',
    'TLS y credencial por camión': 'TLS and one credential per truck',
    'Verde: pasa por el Azure Firewall o por el WAF. Azul punteado: temporal de la migración. Rojo: controlado por NSG o por IoT Hub, sin pasar por el firewall. El DNS entre Cali y el resolver del hub también se controla con NSG (UDP y TCP 53). El tránsito entre centros y Cali durante la convivencia (FW-401 y FW-402) pasa por el firewall.':
        'Green: goes through Azure Firewall or the WAF. Dotted blue: temporary, during the migration. Red: controlled by an NSG or by IoT Hub, without the firewall. DNS between Cali and the hub resolver is also controlled by NSG (UDP and TCP 53). Traffic between the centers and Cali during coexistence (FW-401 and FW-402) goes through the firewall.',

    # telemetria-13-p1-ingesta-y-alerta
    'Telemetría: los dos caminos de ingesta y el camino de la alerta': 'Telemetry: the two ingestion paths and the alert path',
    'Ocho centros · camino 1': 'Eight centers · path 1',
    'Camiones · camino 2': 'Trucks · path 2',
    'Hub · East US 2': 'Hub · East US 2',
    'vnet-prod<br>snet-ingest': 'vnet-prod<br>snet-ingest',
    'Central US': 'Central US',
    'Producción East US 2 · vnet-prod': 'Production East US 2 · vnet-prod',
    'Canales por internet<br>(salida por el Azure Firewall)': 'Internet channels<br>(outbound through Azure Firewall)',
    'Sensores de cuartos fríos<br>32 (4 por centro)<br>una lectura cada 30 s': 'Cold room sensors<br>32 (4 per center)<br>one reading every 30 s',
    'Recolector opcional por centro con IoT Edge, si los sensores no hablan MQTT o AMQP con TLS': 'Optional IoT Edge collector per center, if the sensors cannot speak MQTT or AMQP over TLS',
    '120 camiones (180 en campaña)<br>temperatura cada 60 s<br>posición cada 30 s<br>guardan 18 h sin señal': '120 trucks (180 at peak)<br>temperature every 60 s<br>position every 30 s<br>store 18 h without signal',
    'Azure Firewall<br>FW-204': 'Azure Firewall<br>FW-204',
    'Endpoints privados<br>de IoT Hub y DPS': 'IoT Hub and DPS<br>private endpoints',
    'DPS: alta automática<br>con certificados X.509': 'DPS: automatic enrollment<br>with X.509 certificates',
    'IoT Hub S1 × 2 unidades<br>800.000 mensajes al día<br>redundante entre zonas': 'IoT Hub S1 × 2 units<br>800,000 messages a day<br>zone-redundant',
    'Si cae la región, IoT Hub se conmuta a mano a East US 2. Los dispositivos guardan sus lecturas hasta confirmar que llegaron.': 'If the region fails, IoT Hub is failed over manually to East US 2. Devices keep their readings until delivery is confirmed.',
    'Rangos por cuarto frío<br>y por tipo de carga<br>(los mantiene calidad)': 'Ranges per cold room<br>and cargo type<br>(maintained by quality)',
    'Stream Analytics<br>reglas de alerta<br>1/3 SU V2 esperado': 'Stream Analytics<br>alert rules<br>1/3 SU V2 expected',
    'Función notificadora<br>Flex Consumption<br>snet-telemetry-func': 'Notifier function<br>Flex Consumption<br>snet-telemetry-func',
    'Event hub de estado<br>en vivo para el mapa': 'Live status<br>event hub for the map',
    'Event hub<br>de alertas': 'Alerts<br>event hub',
    'API y consola de la torre<br>snet-app-torre': 'Control tower API and console<br>snet-app-torre',
    'Teams (Workflows)<br>computador y teléfono': 'Teams (Workflows)<br>desktop and phone',
    'Correo: Azure<br>Communication Services': 'Email: Azure<br>Communication Services',
    'SMS: proveedor con<br>cobertura en Colombia': 'SMS: provider with<br>coverage in Colombia',
    'IPsec': 'IPsec',
    'Privado, entre regiones': 'Private, across regions',
    'Red móvil del operador': 'Carrier mobile network',
    'Endpoint de eventos': 'Events endpoint',
    'Mapa en vivo': 'Live map',
    'Alerta': 'Alert',
    'Volumen declarado (mensajes de 1 KB)<br>Normal: 7,2 mensajes por segundo, unos 486.000 al día<br>Campaña con 180 camiones: 10,2 por segundo, unos 682.000 al día': 'Declared volume (1 KB messages)<br>Normal: 7.2 messages per second, about 486,000 a day<br>Peak season with 180 trucks: 10.2 per second, about 682,000 a day',
    'Presupuesto de la alerta: hasta 40 s desde la hora de la lectura del sensor<br>hasta que se ve en pantalla (5 + 10 + 10 + 5 + 10 s), con 20 s de margen dentro del minuto': 'Alert budget: up to 40 s from the sensor reading time<br>until it is on screen (5 + 10 + 10 + 5 + 10 s), with 20 s of margin within the minute',
    'Destinatario según la hora de Colombia<br>04:00 a 22:00: torre de control (consola y Teams), copia a calidad<br>22:00 a 04:00: guardia de calidad (Teams, correo y SMS). Escala a los 5 y a los 15 minutos': 'Recipient by Colombian time<br>04:00 to 22:00: control tower (console and Teams), copy to quality<br>22:00 to 04:00: quality on-call (Teams, email and SMS). Escalates at 5 and 15 minutes',
    'Azul: camino 1, cuartos fríos por la VPN y el Azure Firewall. Naranja: camino 2, camiones por internet. Verde: lecturas hacia el procesamiento y el mapa. Rojo: alertas. Gris punteado: configuración. Stream Analytics también escribe el historial (ver el diagrama del historial).':
        'Blue: path 1, cold rooms through the VPN and Azure Firewall. Orange: path 2, trucks over the internet. Green: readings to processing and the map. Red: alerts. Dotted gray: configuration. Stream Analytics also writes the history.',

    # observabilidad-16-p1-recoleccion-y-alertas
    'Observabilidad: las cuatro áreas, dónde se recolecta y adónde llegan las alertas y los tableros': 'Observability: the four areas, where data is collected and where alerts and dashboards go',
    '1. Salud de la plataforma': '1. Platform health',
    '2. Enlaces hacia Cali y los centros': '2. Links to Cali and the centers',
    '3. Seguridad': '3. Security',
    '4. Despacho, rastreo e ingesta': '4. Dispatch, tracking and ingestion',
    'Container Apps<br>torre y portal': 'Container Apps<br>tower and portal',
    'MySQL y réplica<br>de Central US': 'MySQL and<br>Central US replica',
    'Managed Redis': 'Managed Redis',
    'Key Vault': 'Key Vault',
    'Archivo, historial<br>y función': 'Archive, history<br>and function',
    'Máquinas de<br>operación': 'Operations<br>machines',
    'Cali: 4 túneles,<br>2 proveedores': 'Cali: 4 tunnels,<br>2 providers',
    '8 centros:<br>2 túneles cada uno': '8 centers:<br>2 tunnels each',
    'VPN Gateway<br>BGP por túnel': 'VPN Gateway<br>BGP per tunnel',
    'Azure Firewall': 'Azure Firewall',
    'Defender for Cloud<br>5 suscripciones': 'Defender for Cloud<br>5 subscriptions',
    'WAF del portal': 'Portal WAF',
    'DDoS IP<br>Protection': 'DDoS IP<br>Protection',
    'Inteligencia de<br>amenazas': 'Threat<br>intelligence',
    'Cambios en<br>reglas y permisos': 'Rule and<br>permission changes',
    'Despacho<br>(torre)': 'Dispatch<br>(tower)',
    'Rastreo<br>(portal)': 'Tracking<br>(portal)',
    'Application<br>Gateway': 'Application<br>Gateway',
    'IoT Hub': 'IoT Hub',
    'Stream<br>Analytics': 'Stream<br>Analytics',
    'Función<br>notificadora': 'Notifier<br>function',
    'Azure Monitor · espacio central de Log Analytics en la suscripción de seguridad': 'Azure Monitor · central Log Analytics workspace in the security subscription',
    'Métricas de plataforma<br>cada minuto, 93 días, sin costo': 'Platform metrics<br>every minute, 93 days, no cost',
    'Log Analytics<br>registros, alertas de Defender y<br>registro de cada alerta': 'Log Analytics<br>logs, Defender alerts and<br>a record of every alert',
    'Application Insights<br>uno por ambiente': 'Application Insights<br>one per environment',
    'Se guarda en el espacio': 'Stored in the workspace',
    'Métricas y registros<br>de recurso (P-04)': 'Resource metrics<br>and logs',
    'BGP y ancho de banda por túnel,<br>Resource Health': 'BGP and bandwidth per tunnel,<br>Resource Health',
    'Exportación continua de Defender,<br>registros del WAF y del firewall': 'Continuous Defender export,<br>WAF and firewall logs',
    'OpenTelemetry (10 %), registro de<br>cada alerta, prueba de disponibilidad': 'OpenTelemetry (10%), record of<br>every alert, availability test',
    'Alertas, guardia y tableros': 'Alerts, on-call and dashboards',
    'Reglas de alerta<br>métricas, búsquedas,<br>Resource Health': 'Alert rules<br>metrics, queries,<br>Resource Health',
    'Sev0 crítica, Sev1 alta,<br>Sev2 aviso': 'Sev0 critical, Sev1 high,<br>Sev2 warning',
    'Reglas de procesamiento<br>mantenimientos, pruebas<br>y desarrollo': 'Processing rules<br>maintenance, test<br>and development',
    'Grupos de acción<br>guardia, operación, aviso,<br>seguridad, respaldo de calidad': 'Action groups<br>on-call, operations, notice,<br>security, quality backup',
    'Logic App<br>Teams (Workflows) y SMS<br>del proveedor': 'Logic App<br>Teams (Workflows) and<br>provider SMS',
    'Push de la app de Azure y correo salen<br>directo del grupo de acción': 'Azure app push and email go<br>straight from the action group',
    'Destinatarios': 'Recipients',
    'Guardia de plataforma<br>24 horas': 'Platform on-call<br>24 hours',
    'Operación': 'Operations',
    'Calidad o torre, si falla<br>el camino de la alerta': 'Quality or tower, if the<br>alert path fails',
    'Responsable<br>de seguridad': 'Security<br>owner',
    'Tablero de operación<br>(Workbooks): objetivos,<br>enlaces, datos, telemetría,<br>seguridad, migración': 'Operations dashboard<br>(Workbooks): objectives,<br>links, data, telemetry,<br>security, migration',
    'Consultas': 'Queries',
    'Vistas de Cost<br>Management por línea:<br>operación, telemetría,<br>pruebas, compartido;<br>Fabric aparte': 'Cost Management<br>views per line:<br>operations, telemetry,<br>testing, shared;<br>Fabric separately',
    'Objetivos de servicio: portal de rastreo, 99,9 % de minutos buenos en 28 días; alerta de temperatura, 99 % visible en 60 segundos o menos desde la lectura del sensor. Las métricas no se muestrean. Las vistas de costo leen directamente la facturación de Azure.':
        'Service objectives: tracking portal, 99.9% good minutes over 28 days; temperature alert, 99% visible within 60 seconds of the sensor reading. Metrics are not sampled. Cost views read Azure billing directly.',

    # fabric-18-p1-acceso-y-usos
    'Fabric: quién ve qué y cómo llegan los tres usos a la torre, a calidad y al cliente': 'Fabric: who sees what, and how the three use cases reach the tower, quality and the customer',
    'Azure · East US 2': 'Azure · East US 2',
    'Fabric · fcfaprod': 'Fabric · fcfaprod',
    'ws-fa-datos-prod': 'ws-fa-datos-prod',
    'Quién lo usa': 'Who uses it',
    'Event Hub del estado en vivo<br>con umbrales de aviso': 'Live status Event Hub<br>with warning thresholds',
    'Tabla de análisis<br>(atajo)': 'Analysis table<br>(shortcut)',
    'Libro operativo<br>(vistas del esquema fabric)': 'Operational database<br>(fabric schema views)',
    'Fotos y comprobantes<br>(atajo)': 'Photos and receipts<br>(shortcut)',
    'Eventstream<br>(endpoint privado)': 'Eventstream<br>(private endpoint)',
    'Activator: cerca del límite,<br>puerta abierta, sensor intermitente': 'Activator: near the limit,<br>door open, intermittent sensor',
    'Lakehouse<br><br>Operación (copia)<br>Telemetría (atajo)<br>eta_viaje<br>cliente_guias<br>Resultados de evidencias<br>Files: fotos (atajo)<br><br>Roles de OneLake:<br>torre_lectura<br>calidad_lectura<br>cliente_vista':
        'Lakehouse<br><br>Operations (copy)<br>Telemetry (shortcut)<br>eta_viaje<br>cliente_guias<br>Evidence results<br>Files: photos (shortcut)<br><br>OneLake roles:<br>torre_lectura<br>calidad_lectura<br>cliente_vista',
    'Atajo': 'Shortcut',
    'Gateway y Copy Job<br>04:00 a 22:00 cada 15 min': 'Gateway and Copy Job<br>04:00 to 22:00 every 15 min',
    'Cuaderno de Python<br>hora estimada, cada 5 min': 'Python notebook<br>arrival estimate, every 5 min',
    'Cuaderno nocturno: calidad<br>de imagen y funciones de IA': 'Nightly notebook: image<br>quality and AI functions',
    'Endpoint SQL: eta_viaje<br>(rol torre_lectura)': 'SQL endpoint: eta_viaje<br>(torre_lectura role)',
    'ws-fa-calidad-prod': 'ws-fa-calidad-prod',
    'Tableros con Direct Lake<br>(rol calidad_lectura)': 'Direct Lake dashboards<br>(calidad_lectura role)',
    'ws-fa-cliente-prod': 'ws-fa-cliente-prod',
    'Modelo sobre cliente_guias con<br>seguridad por filas (cliente_vista)': 'Model over cliente_guias with<br>row-level security (cliente_vista)',
    'Teams: Avisos de cadena de frío.<br>Torre de día, guardia de calidad de noche': 'Teams: cold chain notices.<br>Tower by day, quality on-call by night',
    'Aviso, sin SMS ni escalamiento': 'Notice, no SMS or escalation',
    'Consola de la torre: hora estimada<br>como sugerencia; decide el despachador': 'Tower console: arrival estimate<br>as a suggestion; the dispatcher decides',
    'TDS 1433': 'TDS 1433',
    'Aplicación de evidencias: calidad ve la<br>imagen y confirma o descarta la marca': 'Evidence app: quality sees the<br>image and confirms or dismisses the flag',
    'Enlace': 'Link',
    'Portal: token de inserción con el<br>cliente_id; el cliente ve solo sus guías': 'Portal: embed token with the<br>customer_id; customers see only their waybills',
    'Morado: lo que ocurre en Fabric y sale de Fabric. Azul: copia del libro operativo. Ningún elemento de Fabric escribe en el libro operativo ni en la API de despacho; la confirmación de calidad vuelve por la base (revision_evidencias) y Copy Job. Los despachadores y los clientes no necesitan licencia de Power BI.':
        'Purple: what happens in Fabric and leaves Fabric. Blue: copy of the operational database. Nothing in Fabric writes to the operational database or the dispatch API; the quality confirmation returns through the database (revision_evidencias) and Copy Job. Dispatchers and customers need no Power BI license.',

    # carga-c-14-p1-de-cali-a-azure
    'De Cali a Azure: decisión, destino y momento de cada pieza': 'From Cali to Azure: decision, destination and timing for each piece',
    'Pieza en Cali': 'Piece in Cali',
    'Decisión': 'Decision',
    'Destino en Azure': 'Destination in Azure',
    'Cuándo': 'When',
    'despacho, inventario,<br>facturación corporativa': 'dispatch, inventory,<br>corporate billing',
    'Se mueve tal cual': 'Rehost',
    'Entorno de la torre (Container Apps)': 'Tower environment (Container Apps)',
    'Cambian juntos en el corte': 'Switch together at cutover',
    'rastreo': 'tracking',
    'Entorno del portal, detrás del<br>Application Gateway con WAF': 'Portal environment, behind<br>Application Gateway with WAF',
    'En el corte': 'At cutover',
    'evidencias': 'evidence',
    'Se rehace': 'Refactor',
    'Entorno de la torre; lee y escribe en<br>Blob Storage, sin NFS': 'Tower environment; reads and writes<br>Blob Storage, no NFS',
    'Ajuste probado antes del día 0;<br>cambia en el corte': 'Change tested before day 0;<br>switches at cutover',
    'Front (2 máquinas)': 'Front end (2 machines)',
    'Un contenedor de front por entorno': 'One front-end container per environment',
    'Nginx (2 máquinas)': 'Nginx (2 machines)',
    'Se reemplaza': 'Replace',
    'Application Gateway v2 con WAF': 'Application Gateway v2 with WAF',
    'En el corte; Nginx se apaga<br>al cerrar el plazo': 'At cutover; Nginx is switched off<br>when rollback closes',
    'MySQL 5.7 de producción': 'Production MySQL 5.7',
    'MySQL Flexible Server 8.4,<br>migrado en línea con DMS': 'MySQL Flexible Server 8.4,<br>migrated online with DMS',
    'Replicación desde el día 5;<br>cambia en el corte': 'Replication from day 5;<br>switches at cutover',
    'MySQL 5.7 de desarrollo y pruebas': 'Development and test MySQL 5.7',
    'Bases nuevas vacías,<br>con datos inventados': 'New empty databases<br>with synthetic data',
    'Antes del día 0': 'Before day 0',
    'Redis 5': 'Redis 5',
    'Azure Managed Redis': 'Azure Managed Redis',
    'En el corte; arranca vacía': 'At cutover; starts empty',
    'FTP y NFS con 1,2 PB': 'FTP and NFS with 1.2 PB',
    'Se retira': 'Retire',
    'Cuentas de archivo y evidencias<br>(siembra y copia continua, #15)': 'Archive and evidence accounts<br>(seeding and continuous copy)',
    'Siembra conciliada antes del ensayo;<br>copia continua del día 0 al 35': 'Seeding reconciled before the rehearsal;<br>continuous copy from day 0 to 35',
    'Carga de temperatura por lote': 'Batch temperature load',
    'IoT Hub (#13)': 'IoT Hub',
    'Centro por centro,<br>días 8 a 19': 'Center by center,<br>days 8 to 19',
    'Zabbix': 'Zabbix',
    'Azure Monitor (#16)': 'Azure Monitor',
    'Día 61': 'Day 61',
    'VMware (3 clústeres)': 'VMware (3 clusters)',
    '—': 'n/a',
    'Día 62: Cali apagada': 'Day 62: Cali switched off',
    'Se mueve tal cual (misma imagen, otra configuración)': 'Rehost (same image, different configuration)',
    'Se rehace en su forma final': 'Refactor into its final form',
    'Se reemplaza por un servicio administrado': 'Replace with a managed service',
}

NAMES = {
    'firewall-9-p2-puntos-de-control': 'firewall',
    'telemetria-13-p1-ingesta-y-alerta': 'telemetria',
    'observabilidad-16-p1-recoleccion-y-alertas': 'observabilidad',
    'fabric-18-p1-acceso-y-usos': 'fabric',
    'carga-c-14-p1-de-cali-a-azure': 'migracion',
}


def main():
    out = HERE / 'out'
    out.mkdir(exist_ok=True)
    missing = []
    for src, name in NAMES.items():
        text = (HERE / 'src' / f'{src}.drawio').read_text()

        def swap(m):
            raw = html.unescape(m.group(1))
            if not raw.strip():
                return m.group(0)
            if raw not in EN:
                missing.append((src, raw))
                return m.group(0)
            return 'value="' + html.escape(EN[raw], quote=True) + '"'

        text = re.sub(r'value="([^"]*)"', swap, text)
        (out / f'{name}.drawio').write_text(text)
    if missing:
        for src, raw in missing:
            print(f'{src}: {raw!r}', file=sys.stderr)
        sys.exit(1)
    print('ok', len(NAMES), 'diagrams')


if __name__ == '__main__':
    main()
