"""Diagramas rehechos para la web, en inglés: gobierno, seguridad, plataforma y red.

Mismo estilo que los diagramas de draw.io del repo planning: zonas claras con
borde, íconos de Azure y líneas ortogonales con quiebres fijos.

    python3 diagrams/build.py        # escribe diagrams/out/*.drawio
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent / 'out'
AZ = 'img/lib/azure2/'
ICON = {
    'entra': AZ + 'identity/Azure_Active_Directory.svg',
    'pim': AZ + 'identity/Entra_Privileged_Identity_Management.svg',
    'mi': AZ + 'identity/Managed_Identities.svg',
    'users': AZ + 'identity/Users.svg',
    'mg': AZ + 'general/Management_Groups.svg',
    'sub': AZ + 'general/Subscriptions.svg',
    'tags': AZ + 'general/Tags.svg',
    'budget': AZ + 'general/Cost_Budgets.svg',
    'policy': AZ + 'management_governance/Policy.svg',
    'law': AZ + 'management_governance/Log_Analytics_Workspaces.svg',
    'defender': AZ + 'security/Security_Center.svg',
    'kv': AZ + 'security/Key_Vaults.svg',
    'firewall': AZ + 'networking/Firewalls.svg',
    'fwpolicy': AZ + 'networking/Azure_Firewall_Policy.svg',
    'appgw': AZ + 'networking/Application_Gateways.svg',
    'vpngw': AZ + 'networking/Virtual_Network_Gateways.svg',
    'bastion': AZ + 'networking/Bastions.svg',
    'dns': AZ + 'networking/DNS_Private_Resolver.svg',
    'pe': AZ + 'networking/Private_Endpoint.svg',
    'datagw': AZ + 'networking/On_Premises_Data_Gateways.svg',
    'aca': AZ + 'other/Container_App_Environments.svg',
    'mysql': AZ + 'databases/Azure_Database_MySQL_Server.svg',
    'redis': AZ + 'databases/Azure_Managed_Redis.svg',
    'storage': AZ + 'storage/Storage_Accounts.svg',
    'iothub': AZ + 'iot/IoT_Hub.svg',
    'dps': AZ + 'iot/Device_Provisioning_Services.svg',
    'func': AZ + 'iot/Function_Apps.svg',
    'sensor': AZ + 'other/Defender_Sensor.svg',
    'edge': AZ + 'iot/IoT_Edge.svg',
    'mobile': AZ + 'general/Mobile.svg',
    'browser': AZ + 'general/Browser.svg',
    'fabric': AZ + 'analytics/Power_BI_Embedded.svg',
}
NET = 'html=1;outlineConnect=0;fillColor=#CCCCCC;strokeColor=#6881B3;gradientColor=none;strokeWidth=2;shape=mxgraph.networks.'

INK = '#0A1F2E'
MUTE = '#52646F'
GREEN = '#2E7D32'
BLUE = '#1565C0'
ORANGE = '#EF6C00'
PURPLE = '#6A1B9A'
GRAY = '#78909C'
TEAL = '#0D7894'

Z_GRAY = ('#F7F9FA', '#B0BEC5')
Z_BLUE = ('#EEF6FC', '#64A6D9')
Z_TEAL = ('#ECF7FA', '#4FB3CC')
Z_PURPLE = ('#F6EEF9', '#A77BC4')
Z_GREEN = ('#EEF7EF', '#7CB883')
Z_AMBER = ('#FFF8EC', '#E0B162')
Z_WHITE = ('#FFFFFF', '#B0BEC5')


def lab(s):
    return escape(s, {'\n': '&lt;br&gt;', '"': '&quot;'})


class Diagram:
    def __init__(self):
        self.cells = []
        self.n = 0

    def _id(self, p):
        self.n += 1
        return f'{p}{self.n}'

    def _v(self, cid, value, style, x, y, w, h):
        self.cells.append(f'<mxCell id="{cid}" value="{lab(value)}" style="{style}" vertex="1" parent="1">'
                          f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        return cid

    def zone(self, x, y, w, h, label, colors=Z_GRAY, dashed=False, font=13):
        fill, stroke = colors
        st = (f'rounded=1;arcSize={max(1, int(1600 / max(w, h)))};whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};'
              f'verticalAlign=top;align=left;spacingLeft=12;spacingTop=6;fontSize={font};fontStyle=1;fontColor={INK};'
              f'{"dashed=1;" if dashed else ""}')
        return self._v(self._id('z'), label, st, x, y, w, h)

    def text(self, x, y, w, h, label, font=12, align='left', color=MUTE, bold=False, valign='middle'):
        st = (f'text;html=1;whiteSpace=wrap;align={align};verticalAlign={valign};fontSize={font};fontColor={color};'
              f'{"fontStyle=1;" if bold else ""}')
        return self._v(self._id('t'), label, st, x, y, w, h)

    def card(self, x, y, w, h, label, colors=Z_WHITE, font=12, bold_first=True):
        fill, stroke = colors
        lines = label.split('\n')
        value = (f'<b>{escape(lines[0])}</b>' if bold_first else escape(lines[0])) + ''.join(f'<br>{escape(l)}' for l in lines[1:])
        st = (f'rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};fontSize={font};'
              f'fontColor={INK};align=left;verticalAlign=middle;spacingLeft=12;spacingRight=8;')
        cid = self._id('c')
        self.cells.append(f'<mxCell id="{cid}" value="{escape(value, {chr(34): "&quot;"})}" style="{st}" vertex="1" parent="1">'
                          f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        return cid

    def icon(self, x, y, kind, label, size=48, font=11, side='bottom', lw=None):
        if kind in ICON:
            st = f'image;aspect=fixed;html=1;points=[];image={ICON[kind]};fontSize={font};fontColor={INK};labelBackgroundColor=none;'
        elif kind == 'cloud':
            st = f'ellipse;shape=cloud;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={GRAY};fontSize={font};fontColor={INK};'
        else:
            st = NET + kind + f';fontSize={font};fontColor={INK};'
        if kind != 'cloud':
            if side == 'bottom':
                st += 'verticalLabelPosition=bottom;verticalAlign=top;align=center;'
            elif side == 'right':
                st += 'labelPosition=right;verticalLabelPosition=middle;align=left;verticalAlign=middle;spacingLeft=6;'
            elif side == 'left':
                st += 'labelPosition=left;verticalLabelPosition=middle;align=right;verticalAlign=middle;spacingRight=6;'
            elif side == 'top':
                st += 'verticalLabelPosition=top;verticalAlign=bottom;align=center;'
        if lw:
            st += f'labelWidth={lw};whiteSpace=wrap;'
        h = size if kind != 'cloud' else int(size * 0.62)
        return self._v(self._id('i'), label, st, x, y, size, h)

    def edge(self, s, t, color=INK, label='', pts=(), exit=None, entry=None, dashed=False, arrow=True, width=1.5, font=10, both=False):
        cid = self._id('e')
        st = (f'edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor={color};strokeWidth={width};fontSize={font};'
              f'fontColor={color};labelBackgroundColor=#FFFFFF;jumpStyle=none;')
        st += 'endArrow=block;endFill=1;endSize=5;' if arrow else 'endArrow=none;'
        st += 'startArrow=block;startFill=1;startSize=5;' if both else ''
        if dashed:
            st += 'dashed=1;dashPattern=6 4;'
        if exit:
            st += f'exitX={exit[0]};exitY={exit[1]};exitDx=0;exitDy=0;'
        if entry:
            st += f'entryX={entry[0]};entryY={entry[1]};entryDx=0;entryDy=0;'
        p = ''.join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in pts)
        arr = '<Array as="points">' + p + '</Array>' if p else ''
        geo = '<mxGeometry relative="1" as="geometry">' + arr + '</mxGeometry>'
        self.cells.append(f'<mxCell id="{cid}" value="{lab(label)}" style="{st}" edge="1" parent="1" source="{s}" target="{t}">{geo}</mxCell>')
        return cid

    def save(self, name):
        OUT.mkdir(exist_ok=True)
        xml = ('<mxfile host="drawio"><diagram name="Page-1" id="p1"><mxGraphModel dx="1600" dy="900" grid="0" gridSize="10" '
               'guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="0" pageScale="1" math="0" shadow="0" '
               'background="#FFFFFF"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
               + ''.join(self.cells) + '</root></mxGraphModel></diagram></mxfile>')
        (OUT / f'{name}.drawio').write_text(xml)


# ---------------------------------------------------------------- gobierno
def governance():
    d = Diagram()
    d.zone(0, 0, 1240, 620, 'FríoAndes tenant · Microsoft Entra ID', Z_GRAY)
    d.icon(28, 44, 'entra', 'One corporate directory\nfor every environment', size=40, side='right', lw=200)

    root = d.icon(500, 60, 'mg', 'mg-frioandes\nroot management group', size=48, side='right', lw=170)
    d.icon(790, 76, 'policy', '', size=36)
    d.card(836, 46, 364, 98, 'Azure Policy at the root\nRequired tags on every resource (deny)\nAllowed regions: East US 2 and Central US (deny)\nVersioned initiatives, exceptions with expiry', Z_AMBER)

    d.zone(40, 180, 470, 300, 'Shared platform', Z_TEAL)
    d.zone(560, 180, 640, 300, 'Business workloads', Z_BLUE)
    plat = d.icon(200, 220, 'mg', 'mg-fa-platform', size=40, side='right', lw=120)
    work = d.icon(810, 220, 'mg', 'mg-fa-workloads', size=40, side='right', lw=120)
    d.edge(root, plat, MUTE, exit=(0.5, 1), entry=(0.5, 0), pts=[(524, 160), (220, 160)])
    d.edge(root, work, MUTE, exit=(0.5, 1), entry=(0.5, 0), pts=[(524, 160), (830, 160)])

    subs = [
        (100, 'sub-fa-security', 'Log Analytics, investigation,\naudit archive', plat, 220),
        (330, 'sub-fa-connectivity', 'Hub, Azure Firewall,\nVPN to Cali, hybrid DNS', plat, 220),
        (620, 'sub-fa-prod', 'Logistics, portal, data,\narchive and telemetry', work, 830),
        (830, 'sub-fa-test', 'Integration testing\nbefore production', work, 830),
        (1040, 'sub-fa-dev', 'Synthetic or\nanonymized data', work, 830),
    ]
    for x, name, what, parent, px in subs:
        s = d.icon(x + 40, 330, 'sub', '', size=40)
        d.text(x - 20, 374, 160, 60, f'<b style="color:{INK}">{name}</b><br>{what.replace(chr(10), "<br>")}', font=11, align='center')
        d.edge(parent, s, MUTE, exit=(0.5, 1), entry=(0.5, 0), pts=[(px, 300), (x + 60, 300)])
    d.text(560, 440, 640, 24, 'Production also denies public access to data services and requires HTTPS with TLS 1.2 on storage.', font=11, align='center')

    d.zone(40, 500, 1160, 100, 'Applied to every subscription', Z_WHITE)
    d.icon(64, 538, 'tags', '', size=36)
    d.text(110, 530, 340, 56, '<b style="color:#0A1F2E">Mandatory tags</b><br>environment, workload, cost line, criticality, owner', font=11)
    d.icon(470, 538, 'budget', '', size=36)
    d.text(516, 530, 300, 56, '<b style="color:#0A1F2E">Monthly budget</b><br>alerts at 80%, 100% and 120% of actual spend', font=11)
    d.icon(836, 538, 'law', '', size=36)
    d.text(882, 530, 300, 56, '<b style="color:#0A1F2E">Central diagnostics</b><br>platform logs sent to Log Analytics', font=11)
    d.save('gobierno')


# ---------------------------------------------------------------- seguridad
def security():
    d = Diagram()
    entra = d.icon(600, 6, 'entra', 'Microsoft Entra ID\nMFA and Conditional Access', size=52, side='right', lw=200)

    za = d.zone(0, 110, 420, 270, 'Internal operations', Z_TEAL)
    zb = d.zone(450, 110, 420, 270, 'Corporate customers', Z_BLUE)
    zc = d.zone(900, 110, 440, 270, 'Administration and control', Z_AMBER)
    for z, x in ((za, 210), (zb, 660), (zc, 1120)):
        d.edge(entra, z, MUTE, exit=(0.5, 1), entry=(0.5, 0), pts=[(626, 88), (x, 88)])

    u1 = d.icon(40, 156, 'users', 'Dispatch, quality and on-call\n450 internal users, MFA', size=44, side='right', lw=240)
    a1 = d.icon(40, 280, 'aca', 'Control tower console\nAPI checks role, action and waybill.\nPrivate entry through VPN and firewall.', size=44, side='right', lw=300)
    d.edge(u1, a1, TEAL, 'App roles', exit=(0.5, 1), entry=(0.5, 0))

    u2 = d.icon(490, 156, 'users', 'B2B guest accounts\neach one linked to a customer_id,\nno Azure role', size=44, side='right', lw=260)
    a2 = d.icon(490, 280, 'appgw', 'Tracking portal\nHTTPS through the WAF. Customers see\nonly their own waybills.', size=44, side='right', lw=300)
    d.edge(u2, a2, BLUE, 'Per customer', exit=(0.5, 1), entry=(0.5, 0))

    d.icon(930, 152, 'pim', 'Administrators\nassigned resources only, MFA and\njust-in-time elevation with PIM', size=40, side='right', lw=300)
    d.icon(930, 226, 'users', 'Developers and QA\ndevelopment and test only,\nsynthetic data', size=40, side='right', lw=300)
    d.icon(930, 300, 'law', 'Security and audit\nlogs and authorized evidence,\nfive years of access history', size=40, side='right', lw=300)

    data = d.zone(0, 420, 870, 180, 'Applications reach data with managed identities', Z_GREEN)
    d.edge(a1, data, TEAL, exit=(0.5, 1), entry=(0.071, 0))
    d.edge(a2, data, BLUE, exit=(0.5, 1), entry=(0.588, 0))
    xs = [40, 180, 320, 460, 600, 740]
    for x, (k, t) in zip(xs, [('mi', 'Managed\nidentity'), ('mysql', 'MySQL'), ('redis', 'Redis'), ('storage', 'Blob\nStorage'), ('iothub', 'IoT Hub'), ('kv', 'Key Vault')]):
        d.icon(x + 20, 462, k, t, size=44)
    d.text(24, 562, 820, 28, 'Least privilege per service. People never reach the database or the secrets directly.', font=11)

    d.zone(900, 420, 440, 180, 'Protection', Z_GRAY)
    d.icon(930, 460, 'defender', 'Defender for Cloud\nper subscription, paid plans\nin production', size=40, side='right', lw=280)
    d.icon(930, 530, 'kv', 'Encryption\nTLS 1.2+ in transit, at rest with\none Key Vault per environment', size=40, side='right', lw=280)
    d.save('seguridad')


# ---------------------------------------------------------------- plataforma
def platform():
    d = Diagram()
    r1, r2 = 96, 300
    d.zone(0, 0, 220, 540, 'People', Z_WHITE, dashed=True)
    users = d.icon(86, r1, 'users', '450 internal users\ndispatch, via Entra ID', size=48)
    cust = d.icon(86, r2, 'users', '~2,000 corporate\ncustomers, over\nthe internet', size=48)

    d.zone(250, 0, 190, 540, 'Entry', Z_WHITE, dashed=True)
    fw = d.icon(321, r1, 'firewall', 'Azure Firewall\ncorporate network only', size=48)
    agw = d.icon(321, r2, 'appgw', 'Application Gateway\nWAF v2, the only\npublic entry', size=48)

    d.zone(470, 0, 760, 540, 'Production · East US 2 · vnet-prod 10.101.0.0/21', Z_GRAY)
    d.zone(490, 40, 330, 360, 'Azure Container Apps', Z_PURPLE)
    tower = d.icon(631, r1, 'aca', 'Control tower console\nsnet-app-torre', size=48)
    portal = d.icon(631, r2, 'aca', 'Portal services\nsnet-app-portal', size=48)
    d.text(506, 190, 260, 74, '<b style="color:#0A1F2E">Business services</b><br>Waybills, inventory, dock and route assignment and corporate billing run in the same two environments.', font=11, align='center')

    d.zone(860, 40, 350, 360, 'Data · snet-data', Z_BLUE)
    mysql = d.icon(1011, r1, 'mysql', 'MySQL Flexible Server 8.4\nzone-redundant HA', size=48)
    redis = d.icon(1011, r2, 'redis', 'Azure Managed Redis\nprivate endpoint', size=48)

    d.zone(490, 420, 720, 100, 'Security', Z_GREEN)
    d.icon(530, 456, 'kv', 'Key Vault: secrets and certificates,\nread by the apps with managed identity', size=40, side='right', lw=270)
    d.icon(880, 456, 'entra', 'Microsoft Entra ID\nsign-in with MFA', size=40, side='right', lw=200)

    d.zone(1260, 0, 280, 540, 'Continuity · Central US', Z_GRAY)
    rep = d.icon(1376, r1, 'mysql', 'Geo-redundant replica\nRPO 15 min', size=48)
    d.icon(1376, r2, 'aca', 'Standby environments\nmanual failover, RTO 4 h', size=48)
    d.text(1276, 400, 250, 120, 'Failover is a runbook: it promotes the replica and starts the standby environments. The cache is not replicated and warms up with the first traffic.', font=11)

    d.edge(users, fw, GREEN, 'Corporate network')
    d.edge(fw, tower, GREEN, 'HTTPS 443')
    d.edge(cust, agw, BLUE, 'HTTPS')
    d.edge(agw, portal, BLUE, 'HTTPS')
    d.edge(tower, mysql, INK, 'TCP 3306', exit=(1, 0.3), entry=(0, 0.3))
    d.edge(portal, mysql, INK, 'TCP 3306', exit=(1, 0.3), entry=(0, 0.75), pts=[(840, r2 + 14), (840, r1 + 36)])
    d.edge(portal, redis, INK, 'TCP 10000', exit=(1, 0.7), entry=(0, 0.7))
    d.edge(mysql, rep, PURPLE, 'Geo-redundant replication', dashed=True, exit=(1, 0.5), entry=(0, 0.5))
    d.save('plataforma')


# ---------------------------------------------------------------- red
def network():
    d = Diagram()
    # internet y terceros
    d.zone(470, 0, 1060, 180, 'Internet and third parties', Z_WHITE)
    trucks = d.icon(510, 72, 'mobile', 'Trucks\n120, 180 at peak', size=44)
    carrier = d.icon(630, 63, 'cloud', 'Carrier\nnetwork', size=100)
    inet = d.icon(790, 26, 'cloud', 'Internet', size=240)
    cust = d.icon(1290, 72, 'browser', 'Portal customers\nabout 2,000', size=44)
    d.edge(trucks, carrier, ORANGE, '')
    d.edge(carrier, inet, ORANGE, 'Cellular')
    d.edge(cust, inet, BLUE, 'HTTPS')

    # on-premises
    d.zone(0, 210, 430, 680, 'On-premises', Z_GRAY)
    d.zone(16, 246, 398, 150, 'Cali headquarters · 10.20.0.0/16', Z_WHITE)
    cu = d.icon(50, 290, 'users', 'Users and tower\n10.20.0.0/24', size=44)
    cfw = d.icon(300, 290, 'firewall', 'Cali firewall', size=44)
    d.edge(cu, cfw, INK)

    cen = d.zone(16, 412, 398, 462, '8 regional centers · 10.31.0.0/16 to 10.38.0.0/16', Z_WHITE)
    names = ['Buenaventura', 'Bogotá', 'Medellín', 'Barranquilla', 'Bucaramanga', 'Pereira', 'Pasto', 'Neiva']
    for i, n in enumerate(names):
        x = 40 + (i % 4) * 92
        y = 450 + (i // 4) * 88
        d.icon(x + 16, y, 'router', f'{n}\n10.{31 + i}.0.0/16', size=34, font=9)
        d.cells[-1] = d.cells[-1].replace('fillColor=#CCCCCC', 'fillColor=#E8F4F7').replace('strokeColor=#6881B3', f'strokeColor={TEAL}')
    d.zone(30, 640, 370, 220, 'Typical center (same in all 8)', Z_TEAL)
    tu = d.icon(56, 680, 'users', 'Users\n10.3X.0.0/24', size=38)
    sen = d.icon(56, 780, 'sensor', 'Cold room\nsensors', size=38)
    col = d.icon(190, 780, 'edge', 'Local collector\nif needed', size=38)
    vpn = d.icon(330, 730, 'router', 'VPN device\nIKEv2, BGP', size=38, side='left', lw=90)
    d.edge(tu, vpn, INK, exit=(1, 0.5), entry=(0.5, 0), pts=[(349, 699)])
    d.edge(sen, col, BLUE, 'Every 30 s')
    d.edge(col, vpn, BLUE, exit=(1, 0.5), entry=(0.5, 1), pts=[(349, 799)])

    # proveedores
    isp1 = d.icon(450, 272, 'cloud', 'ISP 1 · 400 Mbps\n2 tunnels, BGP', size=130)
    isp2 = d.icon(450, 404, 'cloud', 'ISP 2, backup\n2 tunnels, BGP', size=130)
    d.edge(cfw, isp1, INK, exit=(1, 0.5), entry=(0, 0.5))
    d.edge(cfw, isp2, INK, exit=(1, 0.85), entry=(0, 0.5), pts=[(395, 327), (395, 444)])

    # azure east us 2
    az = d.zone(600, 210, 900, 680, 'Azure · East US 2 · 10.100.0.0/14', Z_BLUE)
    d.cells[-1] = d.cells[-1].replace('align=left;spacingLeft=12;', 'align=right;spacingRight=14;')
    hub = d.zone(620, 250, 290, 400, 'vnet-hub · 10.100.0.0/23', Z_WHITE, dashed=True)
    d.icon(660, 290, 'dns', 'DNS Resolver\ninbound', size=44)
    bas = d.icon(800, 290, 'bastion', 'Azure Bastion\nEntra ID and MFA', size=44)
    vgw = d.icon(660, 422, 'vpngw', 'VPN Gateway\nactive-active', size=44)
    afw = d.icon(800, 422, 'firewall', 'Azure Firewall\nStandard', size=44)
    d.icon(660, 550, 'dns', 'DNS Resolver\noutbound to Cali', size=44)
    d.icon(800, 550, 'fwpolicy', 'Firewall policy\nrules per zone', size=44)
    d.edge(vgw, afw, INK, 'UDR')

    d.edge(isp1, vgw, INK, '', exit=(1, 0.5), entry=(0, 0.2), pts=[(610, 312), (610, 431)])
    d.edge(isp2, vgw, INK, '', exit=(1, 0.5), entry=(0, 0.5))
    d.edge(cen, vgw, TEAL, 'IPsec, 2 tunnels per center', exit=(1, 0.17), entry=(0, 0.85), pts=[(645, 490), (645, 459)])

    d.zone(940, 250, 540, 400, 'vnet-prod · 10.101.0.0/21', Z_WHITE, dashed=True)
    c1, c2, c3 = 990, 1150, 1310
    agw = d.icon(c1, 290, 'appgw', 'App Gateway WAF\nsnet-ingress', size=44)
    portal = d.icon(c2, 290, 'aca', 'Portal apps\nsnet-app-portal', size=44, side='right', lw=105)
    d.icon(c3, 290, 'func', 'Notifier function\nsnet-telemetry-func', size=44)
    tower = d.icon(c1, 422, 'aca', 'Tower console\nsnet-app-torre', size=44)
    mysql = d.icon(c2, 422, 'mysql', 'MySQL Flexible HA\nsnet-data', size=44)
    fgw = d.icon(c3, 422, 'datagw', 'Fabric data gateway\nsnet-fabric-egress', size=44)
    arch = d.icon(c1, 550, 'pe', 'Private archive\nsnet-archive', size=44)
    blob = d.icon(c2, 550, 'storage', 'Blob archive\nprivate, immutable', size=44)
    ing = d.icon(c3, 550, 'pe', 'Private ingestion\nsnet-ingest', size=44, side='left', lw=110)

    d.edge(inet, bas, GRAY, 'Remote admins', exit=(0.135, 0.85), entry=(0.5, 0))
    d.edge(inet, agw, BLUE, 'HTTPS 443, only public entry', exit=(0.925, 0.85), entry=(0.5, 0))
    d.edge(agw, portal, BLUE, 'HTTPS')
    d.edge(afw, tower, GREEN)
    d.edge(tower, mysql, INK, '3306')
    d.edge(portal, mysql, INK, '', exit=(0.5, 1), entry=(0.5, 0))
    d.edge(fgw, mysql, PURPLE, 'Read 3306', exit=(0, 0.5), entry=(1, 0.5))
    d.edge(arch, blob, INK, 'Private Link')
    d.edge(afw, ing, BLUE, 'Path 1: sensors through VPN and firewall', exit=(1, 0.85), entry=(0.5, 1), pts=[(925, 459), (925, 630), (1332, 630)])

    # fabric, central us, futuro
    d.zone(1530, 380, 130, 120, 'Fabric (SaaS)', Z_PURPLE, font=12)
    fab = d.icon(1573, 422, 'fabric', 'Capacity', size=44)
    d.edge(fgw, fab, PURPLE, 'Outbound to Fabric')

    d.zone(1530, 520, 250, 210, 'Central US · 10.104.0.0/15', Z_BLUE, font=12)
    iot = d.icon(1716, 550, 'iothub', 'IoT Hub', size=44)
    d.icon(1716, 650, 'dps', 'DPS, device\nenrollment', size=44, side='left', lw=90)
    d.edge(ing, iot, BLUE, 'Private Link', exit=(1, 0.5), entry=(0, 0.5))
    d.edge(inet, iot, ORANGE, 'Path 2: trucks over TLS', exit=(1, 0.75), entry=(0.5, 0), pts=[(1160, 138), (1160, 196), (1738, 196)])

    t = d.zone(620, 690, 130, 70, 'vnet-test\n10.102.0.0/21', Z_WHITE, dashed=True, font=11)
    v = d.zone(780, 690, 130, 70, 'vnet-dev\n10.103.0.0/21', Z_WHITE, dashed=True, font=11)
    d.edge(hub, t, MUTE, '', arrow=False, exit=(0.224, 1), entry=(0.5, 0))
    d.edge(hub, v, MUTE, '', arrow=False, exit=(0.776, 1), entry=(0.5, 0))
    d.text(940, 676, 540, 30, 'Test and development use the same subnet module, peered with the hub.', font=11)
    d.text(940, 706, 540, 130, '<b style="color:#0A1F2E">Legend</b><br>Solid: current traffic · Dashed: future connection<br>Lines without arrows: peering with the hub<br>Blue: cold rooms and portal · Orange: trucks<br>Green: tower, 443 from the corporate network only · Purple: Fabric', font=11, valign='top')
    fut = d.icon(1560, 760, 'cloud', 'Second cloud\n10.110.0.0/15 reserved', size=200)
    d.edge(hub, fut, GRAY, 'Future: VPN or ExpressRoute', dashed=True, exit=(0.5, 1), entry=(0, 0.5), pts=[(765, 862)])
    d.save('red')


if __name__ == '__main__':
    governance()
    security()
    platform()
    network()
    print('ok 4 diagrams')
