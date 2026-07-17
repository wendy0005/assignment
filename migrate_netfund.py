#!/usr/bin/env python3
"""Migrate Security+ networking fundamentals (data-flow / attack-surface focus)."""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "progress.db"
COURSE_ID = "netfund"

GLOSSARY = {
    "DHCP": "Dynamic Host Configuration Protocol — automatically assigns IP address, subnet mask, default gateway, and DNS server to a device joining a network.",
    "ARP": "Address Resolution Protocol — maps a known IP address to a MAC address on the local network. Has no authentication, enabling spoofing attacks.",
    "ICMP": "Internet Control Message Protocol — used for network diagnostics (ping, traceroute) and error reporting. Attackers use it for host discovery and tunneling.",
    "NAT": "Network Address Translation — translates private internal IPs to a public IP so many devices can share one Internet connection.",
    "DNS": "Domain Name System — converts human-readable names (google.com) into IP addresses. Critical for almost all Internet use.",
    "MAC Address": "Media Access Control address — a Layer 2 hardware identifier burned into a network interface. Format like 00:1A:2B:3C:4D:5E.",
    "IP Address": "Internet Protocol address — a Layer 3 logical address assigned by DHCP or statically. Example: 192.168.1.100.",
    "Default Gateway": "The router IP on your local network that forwards traffic destined for other networks (usually the Internet). Example: 192.168.1.1.",
    "Subnet Mask": "Defines which part of an IP address is the network and which is the host. Used with the IP to decide if traffic stays local or goes to the gateway.",
    "Rogue DHCP": "An unauthorized DHCP server on the network that hands out attacker-controlled settings (gateway/DNS) to enable MITM.",
    "DHCP Starvation": "An attack that exhausts the DHCP pool by requesting many leases, forcing clients to fail or fall back to a rogue server.",
    "ARP Spoofing": "Also called ARP poisoning — attacker sends fake ARP replies so traffic meant for another host is sent to the attacker (MITM).",
    "DNS Poisoning": "Corrupting DNS responses or cache so clients resolve legitimate names to attacker-controlled IPs.",
    "DNS Tunneling": "Hiding data or C2 traffic inside DNS queries/responses to bypass firewalls that allow DNS.",
    "MITM": "Man-in-the-Middle — attacker sits between two parties and can read, modify, or inject traffic.",
    "OSPF": "Open Shortest Path First — a dynamic routing protocol used inside networks to automatically learn and update routes.",
    "RIP": "Routing Information Protocol — an older distance-vector dynamic routing protocol. Rare on modern enterprise networks.",
    "EIGRP": "Enhanced Interior Gateway Routing Protocol — Cisco dynamic routing protocol. Security+ may test it as a dynamic routing example.",
    "Static Routing": "Routes configured manually by an admin. Predictable but does not adapt automatically to topology changes.",
    "Dynamic Routing": "Routers exchange route information automatically using protocols like OSPF, RIP, or EIGRP.",
    "Private IP": "Non-routable addresses (e.g. 10.x, 172.16–31.x, 192.168.x) used inside LANs. Require NAT to reach the public Internet.",
    "Public IP": "Globally routable address assigned by an ISP. Visible on the Internet side of NAT.",
    "TTL": "Time To Live — hop count that decreases at each router. When it hits zero, the packet is dropped and ICMP TTL Exceeded is sent (basis of traceroute).",
    "Layer 2": "Data Link layer — frames, MAC addresses, switches, ARP. Local segment only.",
    "Layer 3": "Network layer — packets, IP addresses, routers, routing. Moves traffic between networks.",
    "On-path Attack": "Security+ term for MITM — attacker intercepts communication path between victim systems.",
}


def step(title, body, diagram=None):
    return {"title": title, "body": body, "diagram": diagram}


def lesson(number, title, intro, steps, recap):
    return {
        "number": number,
        "title": title,
        "intro": intro,
        "steps": steps,
        "recap": recap,
    }


TUTORIALS = [
    {
        "id": "nf-core",
        "title": "Core Protocols — DHCP, ARP, ICMP, DNS",
        "short": "Core Protocols",
        "lessons": [
            lesson(
                1,
                "DHCP — Getting on the Network",
                "You do not need every networking detail for Security+ or pentesting. You need to know how data flows and where attackers abuse the process. {{DHCP}} is where that journey starts: a laptop joins Wi-Fi and must get an identity before anything else works.",
                [
                    step(
                        "What DHCP provides",
                        """
<div class="highlight-box">
<strong>{{DHCP}}</strong> automatically gives a device its network settings so users do not configure IPs by hand.
</div>
<p>A successful lease typically includes:</p>
<ul>
  <li><strong>{{IP Address}}</strong> — who you are on the network</li>
  <li><strong>{{Subnet Mask}}</strong> — which addresses are local vs remote</li>
  <li><strong>{{Default Gateway}}</strong> — where to send non-local traffic</li>
  <li><strong>{{DNS}}</strong> server — how names become IPs</li>
</ul>
<p>Without these four pieces, the device is mostly offline even if the radio link is up.</p>
""",
                    ),
                    step(
                        "DORA handshake",
                        """
<p>Remember the four-step exchange as <strong>DORA</strong>:</p>
<ol>
  <li><strong>Discover</strong> — client broadcasts: "Is there a DHCP server?"</li>
  <li><strong>Offer</strong> — server proposes an IP and options</li>
  <li><strong>Request</strong> — client asks for that offer</li>
  <li><strong>Acknowledgement</strong> — server confirms the lease</li>
</ol>
<div class="example-box">
Laptop joins Wi-Fi → Discover → Offer → Request → Acknowledgement. Only then does the laptop have a usable configuration.
</div>
""",
                        diagram="""flowchart TB
  A[Laptop joins Wi-Fi] --> B[DHCP Discover]
  B --> C[DHCP Offer]
  C --> D[DHCP Request]
  D --> E[DHCP Acknowledgement]
  E --> F[IP + Mask + Gateway + DNS]
  style A fill:#dbeafe,stroke:#3b82f6
  style F fill:#f0fdf4,stroke:#059669
  style B fill:#fef3c7,stroke:#f59e0b
  style C fill:#fef3c7,stroke:#f59e0b
  style D fill:#fef3c7,stroke:#f59e0b
  style E fill:#fef3c7,stroke:#f59e0b
""",
                    ),
                    step(
                        "Why attackers care",
                        """
<p>{{DHCP}} is trusted by default on many LANs. That trust is the attack surface.</p>
<table>
  <tr><th>Attack</th><th>What happens</th><th>Why it matters</th></tr>
  <tr><td><strong>{{Rogue DHCP}}</strong></td><td>Attacker server hands out fake gateway/DNS</td><td>Enables {{MITM}} and traffic redirection</td></tr>
  <tr><td><strong>{{DHCP Starvation}}</strong></td><td>Exhausts legitimate lease pool</td><td>Forces clients toward rogue offers</td></tr>
  <tr><td><strong>MITM setup</strong></td><td>Malicious gateway or DNS in the lease</td><td>Attacker becomes path for client traffic</td></tr>
</table>
<div class="highlight-box">
<strong>Exam / lab mindset:</strong> DHCP is not just "auto IP." It is the first chance to control a victim's path to the Internet.
</div>
""",
                    ),
                ],
                [
                    "DHCP assigns IP, subnet mask, default gateway, and DNS (DORA).",
                    "Rogue DHCP and DHCP starvation create MITM opportunities.",
                    "For Security+, link DHCP abuse to on-path attacks.",
                ],
            ),
            lesson(
                2,
                "ARP — IP to MAC Mapping",
                "{{ARP}} answers one question every local packet needs answered: <em>I know the IP — what is the MAC address?</em> That simple map is unauthenticated, which is why {{ARP Spoofing}} shows up constantly in pentesting and Security+.",
                [
                    step(
                        "The ARP question",
                        """
<div class="highlight-box">
<strong>{{ARP}}</strong> maps a known {{IP Address}} to a {{MAC Address}} on the local segment ({{Layer 2}}).
</div>
<p>Example request:</p>
<pre>Who has 192.168.1.5?
Tell 192.168.1.100</pre>
<p>Example response:</p>
<pre>192.168.1.5 is at AA:BB:CC:DD:EE:FF</pre>
<p>Switches forward frames using MAC addresses. Without ARP, your host cannot deliver a packet to the next hop on the LAN — even if it already knows the IP.</p>
""",
                    ),
                    step(
                        "No authentication",
                        """
<p>ARP has <strong>no authentication</strong>. Hosts typically trust the last reply they hear and cache it in the ARP table.</p>
<div class="example-box">
If an attacker replies "192.168.1.1 is at MY-MAC," victims may send gateway traffic to the attacker instead of the real router.
</div>
<p>That is the core of {{ARP Spoofing}} / ARP poisoning and a classic path to {{MITM}} (on-path) attacks.</p>
""",
                        diagram="""flowchart LR
  V[Victim 192.168.1.100] -->|Who has 192.168.1.1?| LAN[Local LAN]
  A[Attacker] -->|Fake reply: 192.168.1.1 is MY-MAC| V
  V -->|Frames for gateway| A
  A -->|Forward or inspect| G[Real Gateway]
  style V fill:#dbeafe,stroke:#3b82f6
  style A fill:#fecaca,stroke:#ef4444
  style G fill:#f0fdf4,stroke:#059669
""",
                    ),
                    step(
                        "Security importance",
                        """
<p>You will see ARP abuse repeatedly in labs and exams:</p>
<ul>
  <li><strong>ARP spoofing / poisoning</strong> — fake IP→MAC bindings</li>
  <li><strong>Man-in-the-middle / on-path</strong> — read or modify traffic</li>
  <li><strong>Session hijacking setup</strong> — steal cookies or credentials after redirect</li>
</ul>
<table>
  <tr><th>Defense idea</th><th>How it helps</th></tr>
  <tr><td>Dynamic ARP Inspection (DAI)</td><td>Validates ARP against DHCP snooping bindings</td></tr>
  <tr><td>Static ARP entries (rare)</td><td>Hardens critical hosts; not scalable</td></tr>
  <tr><td>Port security / NAC</td><td>Limits who can inject frames</td></tr>
</table>
""",
                    ),
                ],
                [
                    "ARP maps IP → MAC on the local network.",
                    "No authentication means spoofing/poisoning is possible.",
                    "ARP abuse is a common MITM / on-path technique.",
                ],
            ),
            lesson(
                3,
                "ICMP — Diagnostics and Discovery",
                "{{ICMP}} is the network's diagnostic language. Defenders use it for troubleshooting; attackers use it for reconnaissance and covert channels. Know the common messages and tools, not every ICMP type number.",
                [
                    step(
                        "What ICMP is for",
                        """
<div class="highlight-box">
<strong>{{ICMP}}</strong> carries error and diagnostic messages. It is not used to carry normal application data like HTTP, but tools build on it heavily.
</div>
<p>Commands you already use:</p>
<ul>
  <li><code>ping</code> — is the host reachable?</li>
  <li><code>traceroute</code> / <code>tracert</code> — which path do packets take?</li>
</ul>
<p>Important message types for exams and labs:</p>
<ul>
  <li><strong>Echo Request / Echo Reply</strong> — ping</li>
  <li><strong>Destination Unreachable</strong> — host/port/network cannot be reached</li>
  <li><strong>TTL Exceeded</strong> — hop limit expired (how traceroute works)</li>
</ul>
""",
                    ),
                    step(
                        "How traceroute works",
                        """
<p>{{TTL}} starts high and drops by 1 at each router. When TTL hits zero, the router drops the packet and often returns <strong>ICMP Time Exceeded</strong>.</p>
<div class="example-box">
Traceroute sends probes with TTL=1, then 2, then 3… Each hop reveals itself when it reports TTL Exceeded.
</div>
""",
                        diagram="""flowchart TB
  L[Laptop TTL probes] --> R1[Router 1]
  R1 -->|TTL Exceeded| L
  L --> R2[Router 2]
  R2 -->|TTL Exceeded| L
  L --> T[Target]
  T -->|Echo Reply or final hop| L
  style L fill:#dbeafe,stroke:#3b82f6
  style T fill:#f0fdf4,stroke:#059669
  style R1 fill:#fef3c7,stroke:#f59e0b
  style R2 fill:#fef3c7,stroke:#f59e0b
""",
                    ),
                    step(
                        "Attacker and defender use",
                        """
<table>
  <tr><th>Role</th><th>Uses ICMP to…</th></tr>
  <tr><td><strong>Attacker</strong></td><td>Discover live hosts, map topology, sometimes tunnel C2 (ICMP tunneling)</td></tr>
  <tr><td><strong>Defender</strong></td><td>Troubleshoot outages; may rate-limit or block ICMP at the edge; detect abnormal ICMP volume</td></tr>
</table>
<div class="highlight-box">
<strong>Pentesting takeaway:</strong> If ICMP is allowed, host discovery is easier. If blocked, switch techniques — absence of ping replies does not mean the host is down.
</div>
""",
                    ),
                ],
                [
                    "ICMP powers ping and traceroute diagnostics.",
                    "Key messages: Echo, Destination Unreachable, TTL Exceeded.",
                    "Attackers use ICMP for discovery and sometimes tunneling.",
                ],
            ),
            lesson(
                4,
                "DNS — Names to Addresses",
                "Humans type names; networks route IPs. {{DNS}} bridges that gap. Without it, the Internet would mostly require raw addresses — and attackers know that controlling resolution means controlling where users go.",
                [
                    step(
                        "What DNS does",
                        """
<div class="highlight-box">
<strong>{{DNS}}</strong> converts a name like <code>google.com</code> into an {{IP Address}} such as <code>142.250.x.x</code>.
</div>
<p>Typical flow when you open a site:</p>
<ol>
  <li>Browser needs an IP for the hostname</li>
  <li>OS checks cache / configured DNS server (often from {{DHCP}})</li>
  <li>Recursive resolver queries authoritative servers as needed</li>
  <li>Client connects to the returned IP</li>
</ol>
<p>If DNS fails or lies, the rest of the stack still works — but it talks to the wrong place.</p>
""",
                    ),
                    step(
                        "How attackers abuse DNS",
                        """
<table>
  <tr><th>Attack</th><th>Idea</th></tr>
  <tr><td><strong>{{DNS Poisoning}}</strong> / spoofing</td><td>Fake answers redirect victims to attacker IPs</td></tr>
  <tr><td><strong>Fake DNS servers</strong></td><td>Rogue DHCP sets attacker DNS so every lookup is controlled</td></tr>
  <tr><td><strong>{{DNS Tunneling}}</strong></td><td>Hide data or C2 inside DNS queries/responses</td></tr>
</table>
<div class="example-box">
If an attacker owns DNS, they can send <code>bank.example</code> to a phishing server while the URL bar still looks plausible to a rushed user.
</div>
""",
                        diagram="""flowchart LR
  U[User types bank.example] --> D[DNS lookup]
  D -->|Legitimate| R[Real bank IP]
  D -->|Poisoned / fake DNS| A[Attacker IP]
  A --> P[Phishing site]
  style U fill:#dbeafe,stroke:#3b82f6
  style R fill:#f0fdf4,stroke:#059669
  style A fill:#fecaca,stroke:#ef4444
  style P fill:#fecaca,stroke:#ef4444
""",
                    ),
                    step(
                        "Defenses you will hear on Security+",
                        """
<ul>
  <li><strong>DNSSEC</strong> — digitally signs DNS data so responses can be validated</li>
  <li><strong>DNS filtering / reputation</strong> — block known-bad domains</li>
  <li><strong>DoH/DoT awareness</strong> — encrypted DNS changes visibility for monitoring</li>
  <li><strong>Protect resolver config</strong> — stop rogue DHCP from pointing clients at attacker DNS</li>
</ul>
<div class="highlight-box">
<strong>Memorize the chain:</strong> control DHCP → control DNS → control destinations. That is why these protocols are taught together for cybersecurity.
</div>
""",
                    ),
                ],
                [
                    "DNS resolves names to IP addresses.",
                    "Poisoning, fake DNS, and tunneling are high-value abuse paths.",
                    "DNSSEC and reputation filtering are common exam defenses.",
                ],
            ),
        ],
    },
    {
        "id": "nf-path",
        "title": "Path to the Internet — Gateway, Routing, NAT",
        "short": "Path & NAT",
        "lessons": [
            lesson(
                1,
                "Default Gateway — Exit from Your LAN",
                "If there is one networking idea that unlocks everything else, it is the {{Default Gateway}}. When traffic is not for your own network, it goes to the gateway — usually your router.",
                [
                    step(
                        "What the gateway is",
                        """
<div class="highlight-box">
The <strong>{{Default Gateway}}</strong> is the local IP of the router that forwards traffic destined for other networks.
</div>
<div class="example-box">
Laptop: <code>192.168.1.20</code><br>
Gateway: <code>192.168.1.1</code><br>
Anything not in the local subnet is sent to <code>192.168.1.1</code>.
</div>
<p>Your host uses the {{Subnet Mask}} to decide: local delivery (via {{ARP}}) vs send-to-gateway.</p>
""",
                    ),
                    step(
                        "Mental model",
                        """
<pre>Everything not local
        ↓
   Default Gateway
        ↓
     Internet path</pre>
<p>If the gateway is wrong — because of misconfiguration or a {{Rogue DHCP}} lease — your traffic still leaves the host, but it may go to an attacker first.</p>
""",
                        diagram="""flowchart TB
  L[Laptop 192.168.1.20] -->|Local traffic| LAN[Other LAN hosts]
  L -->|Non-local traffic| G[Gateway 192.168.1.1]
  G --> I[Internet]
  style L fill:#dbeafe,stroke:#3b82f6
  style G fill:#fef3c7,stroke:#f59e0b
  style I fill:#f0fdf4,stroke:#059669
""",
                    ),
                    step(
                        "Why cybersecurity cares",
                        """
<ul>
  <li>Gateway is a natural <strong>chokepoint</strong> for firewalls, IDS/IPS, and logging</li>
  <li>Attackers want to <strong>become</strong> the gateway (ARP spoof, rogue DHCP)</li>
  <li>Knowing the gateway is step one when mapping a network in a lab</li>
</ul>
<div class="highlight-box">
<strong>Lab habit:</strong> On a new box, identify your IP, mask, gateway, and DNS before you scan or exploit anything.
</div>
""",
                    ),
                ],
                [
                    "Default gateway is the local router for non-local traffic.",
                    "Subnet mask decides local vs gateway delivery.",
                    "Attackers try to impersonate the gateway for MITM.",
                ],
            ),
            lesson(
                2,
                "Routing — Choosing the Path",
                "Routers decide: <em>Which path should this packet take?</em> Think GPS for packets. Security+ likes the difference between static and dynamic routing more than deep protocol math.",
                [
                    step(
                        "What routing does",
                        """
<div class="highlight-box">
<strong>Routing</strong> is {{Layer 3}} path selection between networks using {{IP Address}} destinations.
</div>
<pre>Laptop → Router → ISP → Google</pre>
<p>Each hop looks at the destination IP and consults a routing table. If no better match exists, traffic follows a default route (often toward the Internet).</p>
""",
                        diagram="""flowchart LR
  L[Laptop] --> R1[Home/Office Router]
  R1 --> ISP[ISP]
  ISP --> G[Google]
  style L fill:#dbeafe,stroke:#3b82f6
  style R1 fill:#fef3c7,stroke:#f59e0b
  style ISP fill:#fef3c7,stroke:#f59e0b
  style G fill:#f0fdf4,stroke:#059669
""",
                    ),
                    step(
                        "Static vs dynamic",
                        """
<table>
  <tr><th>Type</th><th>How routes are learned</th><th>Notes</th></tr>
  <tr><td><strong>{{Static Routing}}</strong></td><td>Admin configures manually</td><td>Simple, predictable; does not auto-adapt</td></tr>
  <tr><td><strong>{{Dynamic Routing}}</strong></td><td>Protocols exchange routes</td><td>Examples: {{OSPF}}, {{RIP}}, {{EIGRP}}</td></tr>
</table>
<div class="example-box">
Security+ loves: static = manual; dynamic = OSPF / RIP / EIGRP style automatic updates.
</div>
""",
                    ),
                    step(
                        "Security angle",
                        """
<ul>
  <li><strong>Route hijacking / manipulation</strong> — attacker injects false routes so traffic takes a malicious path</li>
  <li><strong>Trust in routing protocols</strong> — unauthenticated routing updates are dangerous</li>
  <li><strong>Defense</strong> — authentication for routing protocols, filtering, monitoring unexpected path changes</li>
</ul>
<div class="highlight-box">
You do not need to configure OSPF for the exam. You need to know it is dynamic routing and that routing control equals traffic control.
</div>
""",
                    ),
                ],
                [
                    "Routers forward packets based on destination IP.",
                    "Static = manual; dynamic = OSPF/RIP/EIGRP-style learning.",
                    "Route manipulation redirects traffic like a GPS spoof.",
                ],
            ),
            lesson(
                3,
                "NAT — Private to Public Translation",
                "{{Private IP}} addresses cannot reach the Internet directly. {{NAT}} on the router translates them so an entire home or office can share one {{Public IP}}.",
                [
                    step(
                        "Why NAT exists",
                        """
<div class="highlight-box">
<strong>{{NAT}}</strong> translates private internal addresses to a public address (and usually tracks ports so replies return correctly).
</div>
<pre>192.168.1.10  →  Router/NAT  →  203.10.25.100</pre>
<p>This is why every device at home often appears as one public IP on the Internet.</p>
""",
                        diagram="""flowchart LR
  subgraph Private[Private LAN]
    A[192.168.1.10]
    B[192.168.1.20]
  end
  R[Router NAT]
  P[Public 203.10.25.100]
  I[Internet]
  A --> R
  B --> R
  R --> P --> I
  style A fill:#dbeafe,stroke:#3b82f6
  style B fill:#dbeafe,stroke:#3b82f6
  style R fill:#fef3c7,stroke:#f59e0b
  style P fill:#f0fdf4,stroke:#059669
""",
                    ),
                    step(
                        "What to remember",
                        """
<ul>
  <li><strong>Private → Public</strong> on the way out; reverse mapping on the way back</li>
  <li>NAT is common on consumer and edge routers</li>
  <li>It is <strong>not primarily a security control</strong>, even though it hides internal IPs</li>
</ul>
<div class="example-box">
Security note: NAT reduces direct inbound reachability by accident of design, but real protection still needs firewalls, patching, and least privilege.
</div>
""",
                    ),
                    step(
                        "Attack surface note",
                        """
<table>
  <tr><th>Topic</th><th>Reality</th></tr>
  <tr><td>Direct attack on NAT?</td><td>Less common than abusing hosts/services behind it</td></tr>
  <tr><td>Exposure effect</td><td>Port forwards / UPnP can intentionally expose internal services</td></tr>
  <tr><td>Pentest relevance</td><td>External scan sees public IP; internal hosts may only be reachable after foothold</td></tr>
</table>
<div class="highlight-box">
For your priority list: understand translation and shared public IP — not deep NAT table math.
</div>
""",
                    ),
                ],
                [
                    "NAT maps private IPs to a public IP for Internet access.",
                    "Home networks share one public IP via the router.",
                    "NAT hides internals but is not a complete security control.",
                ],
            ),
            lesson(
                4,
                "MAC vs IP — Never Confuse Them",
                "Security+ asks this constantly. {{MAC Address}} is Layer 2 hardware identity. {{IP Address}} is Layer 3 logical identity. Mixing them up breaks your mental model of ARP, switching, and routing.",
                [
                    step(
                        "Side-by-side",
                        """
<table>
  <tr><th></th><th>MAC</th><th>IP</th></tr>
  <tr><td><strong>Layer</strong></td><td>{{Layer 2}}</td><td>{{Layer 3}}</td></tr>
  <tr><td><strong>Nature</strong></td><td>Hardware / interface ID</td><td>Logical address</td></tr>
  <tr><td><strong>Stability</strong></td><td>Changes rarely (can be spoofed)</td><td>Often assigned by {{DHCP}}</td></tr>
  <tr><td><strong>Example</strong></td><td><code>00:1A:2B:3C:4D:5E</code></td><td><code>192.168.1.100</code></td></tr>
  <tr><td><strong>Scope</strong></td><td>Local segment / frames</td><td>Across networks / packets</td></tr>
</table>
""",
                    ),
                    step(
                        "How they work together",
                        """
<p>End-to-end communication uses <strong>IP</strong> for the destination host. Each local hop still needs a <strong>MAC</strong> for the next device on that wire/Wi-Fi segment.</p>
<div class="example-box">
To reach Google: keep Google's IP in the packet headers, but ARP for your gateway's MAC so the frame can leave your laptop.
</div>
""",
                        diagram="""flowchart TB
  P[Packet destination: Google IP] --> Q{Is Google on my LAN?}
  Q -->|No| ARP[ARP for gateway MAC]
  ARP --> F[Frame to gateway MAC]
  F --> R[Router strips/rebuilds frames]
  R --> N[Next hop toward Internet]
  style P fill:#dbeafe,stroke:#3b82f6
  style ARP fill:#fef3c7,stroke:#f59e0b
  style F fill:#fef3c7,stroke:#f59e0b
  style N fill:#f0fdf4,stroke:#059669
""",
                    ),
                    step(
                        "Exam traps",
                        """
<ul>
  <li>Switches care about <strong>MACs</strong>; routers care about <strong>IPs</strong></li>
  <li>{{ARP}} is the bridge: IP question → MAC answer</li>
  <li>MAC spoofing ≠ changing your IP; ARP spoofing abuses the mapping between them</li>
</ul>
<div class="highlight-box">
If you can explain MAC vs IP in one sentence each, half of network Security+ wording becomes easier.
</div>
""",
                    ),
                ],
                [
                    "MAC = Layer 2 hardware; IP = Layer 3 logical.",
                    "ARP connects IP knowledge to MAC delivery.",
                    "Switches use MAC; routers use IP.",
                ],
            ),
        ],
    },
    {
        "id": "nf-flow",
        "title": "Packet Journey & Attack Map",
        "short": "Journey & Attacks",
        "lessons": [
            lesson(
                1,
                "What Happens When You Visit google.com",
                "This is the biggest idea in the room. Every protocol you prioritized fits into one sequence. If you can narrate typing <code>google.com</code> into a browser, you understand the core networking model for Security+ and pentesting.",
                [
                    step(
                        "The full sequence",
                        """
<div class="highlight-box">
Memorize this order for exams and labs:
</div>
<ol>
  <li><strong>{{DHCP}}</strong> — need network settings?</li>
  <li><strong>{{DNS}}</strong> — need IP for the name?</li>
  <li><strong>{{ARP}}</strong> — need MAC for next hop?</li>
  <li><strong>{{Default Gateway}}</strong> — need Internet exit?</li>
  <li><strong>Router / routing</strong> — which path?</li>
  <li><strong>{{NAT}}</strong> — private to public translation?</li>
  <li><strong>Destination</strong> — Google (or attacker if poisoned)</li>
</ol>
<p>Not every step runs every time (caches help), but this is the logical dependency chain.</p>
""",
                        diagram="""flowchart TB
  A[Type google.com] --> B[DHCP if no config]
  B --> C[DNS name to IP]
  C --> D[ARP IP to MAC for gateway]
  D --> E[Send to Default Gateway]
  E --> F[Routers choose path]
  F --> G[NAT at edge]
  G --> H[Google]
  style A fill:#002b5e,color:#fff
  style B fill:#dbeafe,stroke:#3b82f6
  style C fill:#dbeafe,stroke:#3b82f6
  style D fill:#dbeafe,stroke:#3b82f6
  style E fill:#fef3c7,stroke:#f59e0b
  style F fill:#fef3c7,stroke:#f59e0b
  style G fill:#fef3c7,stroke:#f59e0b
  style H fill:#f0fdf4,stroke:#059669
""",
                    ),
                    step(
                        "Priority memory order",
                        """
<p>For Security+ and TryHackMe-style networking rooms, prioritize understanding in this order:</p>
<pre>1. DHCP
2. DNS
3. ARP
4. Gateway
5. Router
6. NAT
7. Internet</pre>
<div class="example-box">
You do not need every RFC detail. You need the flow and the abuse points.
</div>
""",
                    ),
                    step(
                        "Caches change timing, not the model",
                        """
<ul>
  <li>Already have a lease? DHCP may be skipped until renewal</li>
  <li>DNS cached? No new query until TTL expires</li>
  <li>ARP cached? No new who-has until entry ages out</li>
</ul>
<div class="highlight-box">
Attacks often target <strong>trust at each step</strong>, not your ability to recite port numbers.
</div>
""",
                    ),
                ],
                [
                    "Browser visit = DHCP → DNS → ARP → gateway → routing → NAT → destination.",
                    "Memorize the dependency order, not every protocol field.",
                    "Caches skip steps temporarily; the model stays the same.",
                ],
            ),
            lesson(
                2,
                "Where Attacks Happen",
                "Connect each protocol to a security risk. This table is the exam-friendly version of the packet journey: normal purpose on the left, common abuse on the right.",
                [
                    step(
                        "Protocol → attack map",
                        """
<table>
  <tr><th>Protocol</th><th>Normal purpose</th><th>Common attack</th></tr>
  <tr><td><strong>{{DHCP}}</strong></td><td>Assign IP configuration</td><td>{{Rogue DHCP}}, {{DHCP Starvation}}</td></tr>
  <tr><td><strong>{{ARP}}</strong></td><td>Map IP → MAC</td><td>{{ARP Spoofing}} / poisoning</td></tr>
  <tr><td><strong>{{ICMP}}</strong></td><td>Diagnostics</td><td>Host discovery, ICMP tunneling</td></tr>
  <tr><td><strong>{{DNS}}</strong></td><td>Resolve names</td><td>Spoofing, cache poisoning, tunneling</td></tr>
  <tr><td><strong>{{NAT}}</strong></td><td>Private/public translation</td><td>Not usually attacked directly; affects exposure</td></tr>
  <tr><td><strong>Routing</strong></td><td>Forward packets</td><td>Route hijacking / manipulation</td></tr>
</table>
""",
                    ),
                    step(
                        "Why the same flow helps offense and defense",
                        """
<p>If you can explain the google.com journey, you can also explain:</p>
<ul>
  <li>Why {{ARP Spoofing}} enables {{MITM}}</li>
  <li>Why {{DNS Poisoning}} redirects users without malware on the host</li>
  <li>Why a rogue gateway/DNS setting is devastating</li>
  <li>Where to place monitoring (gateway, DNS logs, DHCP bindings)</li>
</ul>
""",
                        diagram="""flowchart LR
  subgraph Trust[Trusted steps]
    DHCP[DHCP]
    DNS[DNS]
    ARP[ARP]
  end
  subgraph Abuse[Abuse points]
    R[Rogue DHCP]
    P[DNS poison]
    S[ARP spoof]
  end
  DHCP -.-> R
  DNS -.-> P
  ARP -.-> S
  R --> M[MITM / wrong path]
  P --> M
  S --> M
  style DHCP fill:#dbeafe,stroke:#3b82f6
  style DNS fill:#dbeafe,stroke:#3b82f6
  style ARP fill:#dbeafe,stroke:#3b82f6
  style R fill:#fecaca,stroke:#ef4444
  style P fill:#fecaca,stroke:#ef4444
  style S fill:#fecaca,stroke:#ef4444
  style M fill:#fecaca,stroke:#ef4444
""",
                    ),
                    step(
                        "Study goal for Security+ / THM / API hacking prep",
                        """
<div class="highlight-box">
Goal: explain <strong>what happens when you type google.com</strong> and point to <strong>where trust can be abused</strong>.
</div>
<p>That single story covers the highest-value networking concepts for:</p>
<ul>
  <li>CompTIA Security+ network fundamentals questions</li>
  <li>TryHackMe networking rooms</li>
  <li>Later pentest topics (on-path attacks, recon, pivoting context)</li>
</ul>
<p>You do not need to memorize every networking detail — prioritize data flow and attacker opportunities.</p>
""",
                    ),
                ],
                [
                    "Map each protocol to at least one attack.",
                    "DHCP/DNS/ARP trust failures often enable MITM.",
                    "Master the google.com flow and attack points for Security+.",
                ],
            ),
        ],
    },
]


def clear_course(c):
    c.execute(
        """
        DELETE FROM lesson_recaps WHERE lesson_id IN (
          SELECT l.id FROM lessons l
          JOIN tutorials t ON l.tutorial_id = t.id
          WHERE t.course_id = ?
        )
        """,
        (COURSE_ID,),
    )
    c.execute(
        """
        DELETE FROM lesson_steps WHERE lesson_id IN (
          SELECT l.id FROM lessons l
          JOIN tutorials t ON l.tutorial_id = t.id
          WHERE t.course_id = ?
        )
        """,
        (COURSE_ID,),
    )
    c.execute(
        """
        DELETE FROM lessons WHERE tutorial_id IN (
          SELECT id FROM tutorials WHERE course_id = ?
        )
        """,
        (COURSE_ID,),
    )
    c.execute("DELETE FROM tutorials WHERE course_id = ?", (COURSE_ID,))
    c.execute("DELETE FROM glossary WHERE course_id = ?", (COURSE_ID,))
    c.execute("DELETE FROM courses WHERE id = ?", (COURSE_ID,))


def migrate(conn):
    c = conn.cursor()
    clear_course(c)

    c.execute(
        "INSERT OR REPLACE INTO courses (id, code, name, description, icon, course_type) VALUES (?,?,?,?,?,?)",
        (
            COURSE_ID,
            "NET-SEC",
            "Networking for Security+",
            "DHCP, ARP, ICMP, DNS, gateway, routing, and NAT — data flow and attack surfaces for Security+, TryHackMe, and pentesting",
            "🛰️",
            "lesson",
        ),
    )

    for term, definition in GLOSSARY.items():
        c.execute(
            "INSERT OR REPLACE INTO glossary (course_id, term, definition) VALUES (?,?,?)",
            (COURSE_ID, term, definition),
        )

    for ti, tut in enumerate(TUTORIALS):
        c.execute(
            "INSERT OR REPLACE INTO tutorials (id, course_id, title, short_title, sort_order) VALUES (?,?,?,?,?)",
            (tut["id"], COURSE_ID, tut["title"], tut["short"], ti),
        )
        for li, les in enumerate(tut["lessons"]):
            c.execute(
                "INSERT INTO lessons (tutorial_id, number, title, intro, sort_order) VALUES (?,?,?,?,?)",
                (tut["id"], les["number"], les["title"], les["intro"], li),
            )
            lesson_id = c.lastrowid
            for si, st in enumerate(les["steps"]):
                c.execute(
                    "INSERT INTO lesson_steps (lesson_id, title, body_html, diagram_mermaid, sort_order) VALUES (?,?,?,?,?)",
                    (lesson_id, st["title"], st["body"].strip(), st.get("diagram"), si),
                )
            for ri, text in enumerate(les["recap"]):
                c.execute(
                    "INSERT INTO lesson_recaps (lesson_id, text, sort_order) VALUES (?,?,?)",
                    (lesson_id, text, ri),
                )

    conn.commit()

    counts = {
        "tutorials": c.execute(
            "SELECT COUNT(*) FROM tutorials WHERE course_id=?", (COURSE_ID,)
        ).fetchone()[0],
        "lessons": c.execute(
            """
            SELECT COUNT(*) FROM lessons l
            JOIN tutorials t ON l.tutorial_id=t.id
            WHERE t.course_id=?
            """,
            (COURSE_ID,),
        ).fetchone()[0],
        "steps": c.execute(
            """
            SELECT COUNT(*) FROM lesson_steps ls
            JOIN lessons l ON ls.lesson_id=l.id
            JOIN tutorials t ON l.tutorial_id=t.id
            WHERE t.course_id=?
            """,
            (COURSE_ID,),
        ).fetchone()[0],
        "glossary": c.execute(
            "SELECT COUNT(*) FROM glossary WHERE course_id=?", (COURSE_ID,)
        ).fetchone()[0],
    }
    print(f"Migrated {COURSE_ID}: {counts}")
    return counts


if __name__ == "__main__":
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    migrate(conn)
    conn.close()
    print("Migration complete")
