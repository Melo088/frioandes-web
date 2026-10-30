export const metrics = [
  { n: 120, l: 'refrigerated trucks', s: '180 during peak season' },
  { n: 32, l: 'cold rooms', s: 'across 8 regional centers' },
  { n: 486, u: 'k', l: 'sensor readings a day', s: '682k during peak season' },
  { n: 1.2, dec: 1, u: ' PB', l: 'archive moved to Azure', s: 'growing 12 TB a month' },
  { n: 60, pre: '< ', u: ' s', l: 'to see an excursion', s: 'day or night' }
];

export const compare = [
  ['Development, test and production share one cluster', 'Three environments built from the same Terraform modules'],
  ['A single firewall in Cali holds every policy', 'Azure Firewall and a WAF, driven by a verified 100-rule policy table'],
  ['Temperature arrives in hourly batches', 'Excursion alerts visible in under 60 seconds'],
  ['1.2 PB of evidence sits on FTP and NFS', 'Seeded on 71 disks and read by Fabric without a second copy'],
  ['Zabbix watches the servers', 'Two service objectives measured over 28 days'],
  ['No brand guide', 'One design system for the control tower and the customer portal']
];

export const layers = [
  {
    name: 'Governance',
    title: 'One tenant, five subscriptions',
    text: 'Policies, tags and budgets are applied once from a single management group, and every dollar is assigned to the area that spends it.',
    facts: [['5', 'subscriptions'], ['5 yrs', 'access audit'], ['4', 'cost centers']],
    img: 'gobierno', cap: 'Governance hierarchy'
  },
  {
    name: 'Security',
    title: 'Least privilege, end to end',
    text: 'MFA and just-in-time access for administrators and dispatch, a Key Vault per environment, and personal data with a defined owner, retention period and location under Colombian law.',
    facts: [['MFA', 'and PIM'], ['1', 'Key Vault per env'], ['Defender', 'per subscription']],
    img: 'seguridad', cap: 'Identity, roles and encryption'
  },
  {
    name: 'Network',
    title: 'A hub that outlives the datacenter',
    text: 'Hub and spoke in East US 2. Every regional center connects straight to Azure through its own VPN, so the network keeps working the day Cali is switched off.',
    facts: [['11', 'subnets per env'], ['8', 'centers on VPN'], ['0', 'overlaps with Cali']],
    img: 'red', cap: 'Steady-state network'
  },
  {
    name: 'Perimeter',
    title: 'One checkpoint for everything',
    text: 'All traffic except the public portal crosses Azure Firewall. The portal is the only service facing the internet, always behind an Application Gateway WAF with DDoS protection.',
    facts: [['100', 'firewall rules'], ['1', 'public service'], ['Script', 'verified']],
    img: 'firewall', cap: 'Control points'
  },
  {
    name: 'Applications',
    title: 'Tower and portal on containers',
    text: 'Container Apps run the control tower and the customer portal on MySQL Flexible Server 8.4 with zone redundancy and a replica in Central US. Kubernetes stays documented as a variant.',
    facts: [['2,000', 'requests / min at peak'], ['15 min', 'RPO'], ['4 h', 'RTO']],
    img: 'plataforma', cap: 'Application platform'
  },
  {
    name: 'Telemetry',
    title: 'From sensor to screen in a minute',
    text: 'Cold rooms report through VPN and private endpoints, trucks through the carrier network. IoT Hub and Stream Analytics detect the problem and a function pages the tower by day or quality on-call by night.',
    facts: [['486k', 'readings a day'], ['< 60 s', 'to alert'], ['5 yrs', 'immutable history']],
    img: 'telemetria', cap: 'Ingestion and alerting'
  },
  {
    name: 'Observability',
    title: 'Two numbers that matter',
    text: 'Application Insights with OpenTelemetry and Log Analytics protect two service objectives: the portal and the temperature alert. Teams and SMS paging run through a Logic App.',
    facts: [['99.9%', 'portal good minutes'], ['99%', 'alerts within 60 s'], ['28 d', 'window']],
    img: 'observabilidad', cap: 'Collection and alerts'
  },
  {
    name: 'Data and AI',
    title: 'Fabric without copying the archive',
    text: 'Fabric reads the database with an incremental copy and reaches the archive through shortcuts. The tower gets early excursion warnings, arrival estimates and damaged photo detection.',
    facts: [['3', 'AI use cases'], ['0 TB', 'duplicated'], ['$4,788', 'saved a month']],
    img: 'fabric', cap: 'Access and AI use cases'
  }
];

export const timeline = [
  { d: 0, t: 'Coexistence starts', p: 'Cali and Azure run side by side.' },
  { d: 18, t: 'Archive reconciled', p: 'The seeded 1.2 PB is complete in Azure.' },
  { d: 20, t: 'Cutover rehearsal', p: 'Two hours at night to prove every criterion.' },
  { d: 34, t: 'Cutover', p: 'Azure becomes the primary platform.', key: true },
  { d: 56, t: 'Rollback closes', p: 'No more return to Cali after this day.' },
  { d: 61, t: 'Zabbix retired', p: 'Azure Monitor watches everything.' },
  { d: 62, t: 'Cali switched off', p: 'The datacenter stops operating.', key: true },
  { d: 90, t: 'Coexistence limit', p: 'The plan closes well before it.' }
];

export const costs = [
  { cls: 'wide', l: 'Total cost of ownership over five years', n: 2625095, note: 'Project, cloud and Fabric together.', bars: [[864360, '1 year'], [1748584, '3 years'], [2625095, '5 years']] },
  { l: 'One-time project cost', n: 419355, note: 'Team, training, migration and 15% contingency.' },
  { l: 'Steady cloud month', n: 17240, note: 'Including the archive.' },
  { l: 'Fabric per month', n: 2892, note: 'F16 capacity, list prices.' },
  { l: 'Avoided over five years', n: 1850000, approx: true, note: '25 design decisions that cost less than the obvious option.' }
];

export const pipeline = [
  { t: 'Pull request', p: 'Format, validate, tfsec, TFLint and Checkov' },
  { t: 'Plan', p: 'Automatic plan per environment' },
  { t: 'Dev', p: 'Applied on merge' },
  { t: 'Test', p: 'Promoted with approval' },
  { t: 'Prod', p: 'Approval and change window, 22:00 to 04:00' }
];

export const palette = [
  ['Deep navy', '#0A1F2E', '#fff'],
  ['Panel navy', '#10304A', '#fff'],
  ['Andean teal', '#0D7894', '#fff'],
  ['Glacier cyan', '#1FB5D6', '#0A1F2E'],
  ['Ice', '#DDF3F8', '#0A1F2E'],
  ['Mist', '#F2F6F8', '#0A1F2E']
];

export const states = [
  { k: 'normal', name: 'Normal', p: 'Within range', ink: '#17794A', soft: '#E3F5EC' },
  { k: 'advertencia', name: 'Warning', p: 'Close to the limit', ink: '#8A5300', soft: '#FFF1D6' },
  { k: 'excursion', name: 'Excursion', p: 'Out of range', ink: '#B3261E', soft: '#FDE6E3' },
  { k: 'sinsenal', name: 'No signal', p: 'Sensor not reporting', ink: '#5B3FC4', soft: '#EEE9FC' }
];
