#!/usr/bin/env python3
"""Migrate ISO/OSI Model & Layer Attacks — study + quiz course."""

import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "progress.db"
COURSE_ID = "osi-attacks"

GLOSSARY = {
    "Evil Maid Attack": "An attack where someone with physical access inserts malicious hardware (USB Rubber Ducky, PoisonTap, hardware keylogger) into a target device to compromise it.",
    "Network Tapping": "Inserting a physical device onto a network cable to intercept and inspect traffic. Tools like the Throwing Star LAN Tap enable passive or active interception.",
    "Rogue Access Point": "An unauthorized Wi-Fi access point deployed to trick users into connecting, enabling traffic interception and credential harvesting.",
    "Deauthentication Attack": "Sending forged deauth frames to disconnect Wi-Fi clients, often used to force reconnection to a Rogue Access Point or cause denial of service.",
    "MAC Address": "Media Access Control address — a Layer 2 hardware identifier burned into a network interface, formatted like 00:1A:2B:3C:4D:5E.",
    "ARP": "Address Resolution Protocol — maps an IP address to a MAC address on the local network. Has no authentication, enabling spoofing attacks.",
    "ARP Spoofing": "Also called ARP poisoning — attacker sends forged ARP replies so traffic meant for another host is sent to the attacker (MITM).",
    "MAC Flooding": "Bombarding a switch with fake MAC addresses to exhaust its CAM table, forcing it into hub mode where it broadcasts all traffic to all ports.",
    "VLAN Hopping": "An attack that sends packets with double 802.1Q tags to bypass switch isolation and jump between different VLANs.",
    "IP Address": "Internet Protocol address — a Layer 3 logical address assigned by DHCP or statically, used to identify hosts across networks.",
    "IP Spoofing": "Altering packet headers to falsify the source IP address, making traffic appear to originate from a trusted or different source.",
    "ICMP": "Internet Control Message Protocol — carries diagnostic and error messages (ping, traceroute). Attackers abuse it for discovery, DoS, and covert channels.",
    "Smurf Attack": "A DDoS attack that sends ICMP Echo Requests to a broadcast address with a spoofed victim source IP, amplifying traffic against the victim.",
    "BGP Route Hijacking": "Maliciously announcing control over IP prefixes in BGP to reroute internet traffic through attacker-controlled routers.",
    "Ping Flood": "A DoS attack that overwhelms a target with ICMP Echo Request packets, consuming bandwidth and processing resources.",
    "TCP": "Transmission Control Protocol — connection-oriented Layer 4 protocol with reliable delivery via the three-way handshake.",
    "UDP": "User Datagram Protocol — connectionless Layer 4 protocol with no handshake, used when speed matters more than reliability.",
    "Three-Way Handshake": "The process TCP uses to establish a connection: SYN, SYN-ACK, ACK. Each step is visible in packet captures.",
    "SYN Flood": "A DoS attack that sends many TCP SYN packets without completing the handshake, exhausting the target's connection pool.",
    "Port Scanning": "Probing a target host for open ports and running services using tools like Nmap, often the first step in reconnaissance.",
    "Nmap": "Network Mapper — the standard tool for port scanning, service detection, and network discovery in penetration testing.",
    "UDP Amplification": "Spoofing a victim's IP when querying open UDP services (NTP, DNS) so large responses flood the victim, causing bandwidth saturation.",
    "NetBIOS": "Network Basic Input/Output System — a Session layer protocol for naming and communication services on Windows networks.",
    "RPC": "Remote Procedure Call — allows a program to execute code on a remote system. Vulnerable implementations enable remote code execution.",
    "Session Hijacking": "Intercepting or guessing session tokens to impersonate a legitimate user without authentication credentials.",
    "EternalBlue": "A notorious exploit (MS17-010) targeting SMB/NetBIOS session setup to achieve remote code execution on unpatched Windows systems.",
    "SSL/TLS": "Secure Sockets Layer / Transport Layer Security — cryptographic protocols that encrypt data between client and server at the Presentation layer.",
    "SSL Stripping": "An attack that downgrades an HTTPS connection to HTTP by intercepting the secure handshake, often using tools like sslstrip.",
    "POODLE": "Padding Oracle On Downgraded Legacy Encryption — an attack exploiting SSL 3.0's block cipher padding to decrypt encrypted data.",
    "Certificate Spoofing": "Presenting a fake or self-signed TLS certificate during a Man-in-the-Middle attack to intercept encrypted sessions.",
    "Serialization Exploit": "Crafting malicious payloads in serialized data formats (JSON, XML, YAML) to trigger remote code execution during parsing.",
    "SQL Injection": "Injecting malicious SQL queries through user input fields to manipulate, read, or destroy database contents.",
    "XSS": "Cross-Site Scripting — injecting malicious scripts into web pages viewed by other users to steal data or hijack sessions.",
    "CSRF": "Cross-Site Request Forgery — tricking an authenticated user into submitting unwanted actions on a web application they are logged into.",
    "Credential Stuffing": "Automating login attempts using credentials leaked from one service to gain access to another where users reused passwords.",
    "Hydra": "A popular password brute-forcing tool that supports many network protocols including HTTP, SSH, FTP, and SMTP.",
    "DNS Spoofing": "Also called DNS poisoning — corrupting a DNS resolver's cache with forged records to redirect domain lookups to attacker-controlled IPs.",
    "CAM Table": "Content Addressable Memory — the switch memory that maps MAC addresses to physical ports. MAC flooding attacks exhaust this table.",
    "802.1Q": "The IEEE standard for VLAN tagging — inserting a tag into Ethernet frames to identify which VLAN the traffic belongs to.",
    "OSI Model": "Open Systems Interconnection Reference Model — a 7-layer conceptual framework (Physical → Application) that standardizes how network communication functions. Each layer handles a specific aspect of data transmission.",
    "Encapsulation": "The process of wrapping data with protocol headers as it travels down the OSI stack (Layer 7 → Layer 1). Each layer adds its own header, like nesting envelopes inside each other.",
    "Decapsulation": "The reverse process of stripping protocol headers as data travels up the OSI stack (Layer 1 → Layer 7) on the receiving end.",
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
        "id": "osi-intro",
        "title": "The OSI Model in Action — Your Data's Journey",
        "short": "Intro — OSI Story",
        "c_idx": 0,
        "lessons": [
            lesson(
                1,
                "Your Data's Journey Through 7 Layers",
                "Imagine this: you type google.com into your browser and press Enter. In the next second, your data will be encrypted, chopped into segments, wrapped in envelopes, addressed like a package, converted to radio waves, and shot through the air at the speed of light. That's the {{OSI Model}} in action — and at every single layer, an attacker could be waiting. Let's follow the journey together.",
                [
                    step(
                        "Scene 7: Application Layer — The Request Is Born",
                        """
<div class="highlight-box">
<strong>📍 We start at the top — Layer 7, the Application layer.</strong> This is where your data is <em>born</em>.
</div>

<p>You type <code>https://www.google.com</code> into the address bar and press Enter. Your browser doesn't know anything about IP addresses or routing — it just knows it needs a web page. It creates a clean, simple {{HTTP}} request:</p>

<pre>GET / HTTP/1.1
Host: www.google.com
Accept: text/html</pre>

<p>This is your data in its purest form — a simple request written in plain text. But the browser can't send this across the internet yet. It needs to pass the request <em>down</em> through the layers, each one wrapping the message in its own specialized packaging.</p>

<div class="example-box">
<strong>Think of it like mailing a letter.</strong> Right now you've only written the words on the paper — you haven't sealed it in an envelope, addressed it, or dropped it in a mailbox. The Application layer is where the message is written. The layers below will handle the rest.
</div>
""",
                        diagram="""flowchart TB
  subgraph OSI["<b>Your Data's Journey — Starting at the Top</b>"]
    direction TB
    L7["7. Application 💻<br/>HTTP Request written"]
    L6["6. Presentation"]
    L5["5. Session"]
    L4["4. Transport"]
    L3["3. Network"]
    L2["2. Data Link"]
    L1["1. Physical"]
  end
  style L7 fill:#f0fdf4,stroke:#059669,color:#064e3b,stroke-width:3px
  style L6 fill:#e2e8f0,stroke:#94a3b8
  style L5 fill:#e2e8f0,stroke:#94a3b8
  style L4 fill:#e2e8f0,stroke:#94a3b8
  style L3 fill:#e2e8f0,stroke:#94a3b8
  style L2 fill:#e2e8f0,stroke:#94a3b8
  style L1 fill:#e2e8f0,stroke:#94a3b8
""",
                    ),
                    step(
                        "Scene 6: Presentation Layer — Wrapping in Encryption",
                        """
<div class="highlight-box">
<strong>📍 Moving down to Layer 6 — the Presentation layer.</strong> Your data gets its first layer of protection.
</div>

<p>Because you typed <code>https://</code>, not <code>http://</code>, your browser triggers {{SSL/TLS}} encryption. Your computer and Google's server perform a cryptographic handshake, agreeing on secret keys that only they know. The HTTP request gets wrapped:</p>

<pre>[🔒 TLS Encrypted ] | HTTP GET /</pre>

<p>Now, even if someone intercepts the data mid-journey, all they'll see is unreadable gibberish. The Presentation layer is your secret language — only you and Google have the decoder ring.</p>

<div class="highlight-box">
<strong>Attack preview:</strong> Attackers use {{SSL Stripping}} to <em>remove</em> this encryption layer, tricking your browser into sending everything in plain text. The {{POODLE}} attack forces the connection to use broken encryption that can be cracked.
</div>
""",
                        diagram="""flowchart TB
  subgraph OSI["<b>Your Data's Journey — Encrypting the Message</b>"]
    direction TB
    L7["7. Application 💻<br/>HTTP Request"]
    L6["6. Presentation 🔒<br/>TLS Encryption applied"]
    L5["5. Session"]
    L4["4. Transport"]
    L3["3. Network"]
    L2["2. Data Link"]
    L1["1. Physical"]
  end
  style L7 fill:#dbeafe,stroke:#3b82f6
  style L6 fill:#f0fdf4,stroke:#059669,color:#064e3b,stroke-width:3px
  style L5 fill:#e2e8f0,stroke:#94a3b8
  style L4 fill:#e2e8f0,stroke:#94a3b8
  style L3 fill:#e2e8f0,stroke:#94a3b8
  style L2 fill:#e2e8f0,stroke:#94a3b8
  style L1 fill:#e2e8f0,stroke:#94a3b8
""",
                    ),
                    step(
                        "Scene 5: Session Layer — Starting a Conversation",
                        """
<div class="highlight-box">
<strong>📍 Down to Layer 5 — the Session layer.</strong> Before data can flow, you and Google need to establish a conversation.
</div>

<p>The Session layer manages the dialog between your browser and Google's server — it handles saying <em>hello</em> (session establishment), keeping track of who's talking (session management), and saying <em>goodbye</em> when done (session termination).</p>

<div class="example-box">
<strong>Think of walkie-talkies.</strong> "Over" starts a transmission, "Roger" acknowledges, "Out" ends it. The Session layer is the protocol for that whole conversation — who speaks when, and for how long.
</div>

<p>For your web request, the TLS session established in Layer 6 also manages session state — remembering which encrypted conversation belongs to your connection versus someone else's.</p>

<div class="highlight-box">
<strong>Attack preview:</strong> {{Session Hijacking}} lets an attacker grab your walkie-talkie mid-conversation. {{EternalBlue}} exploited a flaw in Windows' session management ({{NetBIOS}}/{{RPC}}) to achieve remote code execution.
</div>
""",
                        diagram="""flowchart TB
  subgraph OSI["<b>Your Data's Journey — Establishing the Dialog</b>"]
    direction TB
    L7["7. Application 💻<br/>HTTP Request"]
    L6["6. Presentation 🔒<br/>Encrypted"]
    L5["5. Session 🔗<br/>Conversation established"]
    L4["4. Transport"]
    L3["3. Network"]
    L2["2. Data Link"]
    L1["1. Physical"]
  end
  style L7 fill:#dbeafe,stroke:#3b82f6
  style L6 fill:#dbeafe,stroke:#3b82f6
  style L5 fill:#f0fdf4,stroke:#059669,color:#064e3b,stroke-width:3px
  style L4 fill:#e2e8f0,stroke:#94a3b8
  style L3 fill:#e2e8f0,stroke:#94a3b8
  style L2 fill:#e2e8f0,stroke:#94a3b8
  style L1 fill:#e2e8f0,stroke:#94a3b8
""",
                    ),
                    step(
                        "Scene 4: Transport Layer — Cutting and Addressing",
                        """
<div class="highlight-box">
<strong>📍 Down to Layer 4 — the Transport layer.</strong> Your encrypted message is too big to send all at once. Time to chop it up.
</div>

<p>{{TCP}} at Layer 4 takes the encrypted data, slices it into smaller segments, numbers each one, and adds <strong>port addresses</strong>:</p>

<pre>Segment 1: [TCP src:49502 → dst:443 | Seq#1 | 🔒 data ]
Segment 2: [TCP src:49502 → dst:443 | Seq#2 | 🔒 data ]
Segment 3: [TCP src:49502 → dst:443 | Seq#3 | 🔒 data ]</pre>

<p>Your browser picks a random source port (e.g., 49502). Google listens on port 443 (HTTPS). Before sending data, TCP performs the {{Three-Way Handshake}}:</p>

<pre>You  →  Google:  SYN
You  ←  Google:  SYN-ACK
You  →  Google:  ACK
✅ Connection established!</pre>

<p>If the data gets lost, TCP retransmits. If it arrives out of order, TCP reorders it. {{UDP}} skips all this — it just fires packets and hopes for the best, making it faster but less reliable.</p>

<div class="highlight-box">
<strong>Attack preview:</strong> A {{SYN Flood}} fills Google's connection queue with fake hellos — real users can't connect. {{Port Scanning}} with {{Nmap}} probes every port on your computer like checking every door to see which ones are unlocked. {{UDP Amplification}} turns tiny queries into devastating floods.
</div>
""",
                        diagram="""flowchart TB
  subgraph OSI["<b>Your Data's Journey — Chopping & Addressing</b>"]
    direction TB
    L7["7. Application 💻<br/>HTTP Request"]
    L6["6. Presentation 🔒<br/>Encrypted"]
    L5["5. Session 🔗<br/>Session active"]
    L4["4. Transport 📦<br/>TCP Segments + Ports"]
    L3["3. Network"]
    L2["2. Data Link"]
    L1["1. Physical"]
  end
  style L7 fill:#dbeafe,stroke:#3b82f6
  style L6 fill:#dbeafe,stroke:#3b82f6
  style L5 fill:#dbeafe,stroke:#3b82f6
  style L4 fill:#f0fdf4,stroke:#059669,color:#064e3b,stroke-width:3px
  style L3 fill:#e2e8f0,stroke:#94a3b8
  style L2 fill:#e2e8f0,stroke:#94a3b8
  style L1 fill:#e2e8f0,stroke:#94a3b8
""",
                    ),
                    step(
                        "Scene 3: Network Layer — Finding Google",
                        """
<div class="highlight-box">
<strong>📍 Down to Layer 3 — the Network layer.</strong> Every package needs an address. This is where your data gets one.
</div>

<p>Each TCP segment is wrapped in an IP packet, and the Network layer adds the most important thing: <strong>where this needs to go</strong>.</p>

<pre>From: 192.168.1.50 (your laptop)
  To: 142.250.80.46 (Google's server)</pre>

<p>{{IP Address}}es are like street addresses for the internet. Routers along the path look at the destination IP and forward the packet hop by hop — through your home router, your ISP, across the ocean in submarine cables, and finally to Google's data center.</p>

<div class="example-box">
<strong>Like a package with a shipping label.</strong> Each sorting facility (router) reads the destination and sends it closer. Your package might pass through 10-15 routers before arriving.
</div>

<p>Other protocols at this layer: {{ICMP}} (ping, diagnostics) and routing protocols like BGP that build the internet's GPS.</p>

<div class="highlight-box">
<strong>Attack preview:</strong> {{IP Spoofing}} forges the return address to hide the attacker's identity. A {{Smurf Attack}} amplifies {{ICMP}} traffic to crush a victim. {{BGP Route Hijacking}} is like rerouting all mail for a zip code through a criminal warehouse.
</div>
""",
                        diagram="""flowchart TB
  subgraph OSI["<b>Your Data's Journey — Addressing the Package</b>"]
    direction TB
    L7["7. Application 💻<br/>HTTP Request"]
    L6["6. Presentation 🔒<br/>Encrypted"]
    L5["5. Session 🔗<br/>Session active"]
    L4["4. Transport 📦<br/>TCP Segments"]
    L3["3. Network 🌐<br/>IP Packets + Routing"]
    L2["2. Data Link"]
    L1["1. Physical"]
  end
  style L7 fill:#dbeafe,stroke:#3b82f6
  style L6 fill:#dbeafe,stroke:#3b82f6
  style L5 fill:#dbeafe,stroke:#3b82f6
  style L4 fill:#dbeafe,stroke:#3b82f6
  style L3 fill:#f0fdf4,stroke:#059669,color:#064e3b,stroke-width:3px
  style L2 fill:#e2e8f0,stroke:#94a3b8
  style L1 fill:#e2e8f0,stroke:#94a3b8
""",
                    ),
                    step(
                        "Scene 2: Data Link Layer — Your Next-Door Neighbor",
                        """
<div class="highlight-box">
<strong>📍 Down to Layer 2 — the Data Link layer.</strong> Before your data can cross the internet, it first needs to reach your router — just one hop away on your local network.
</div>

<p>The Data Link layer wraps the IP packet in an <strong>Ethernet frame</strong> with source and destination {{MAC Address}}es — hardware IDs burned into every network interface:</p>

<pre>From MAC: AA:BB:CC:11:22:33 (your laptop)
  To MAC: DD:EE:FF:44:55:66 (your router)</pre>

<p>Your computer uses {{ARP}} to find the router's MAC: <em>"Who has 192.168.1.1? Tell 192.168.1.50."</em> The router replies with its MAC, and now the frame can be built and sent.</p>

<div class="example-box">
<strong>Think of this as handing a letter to your next-door neighbor.</strong> You know their house (MAC), not the entire street address of the final destination — that's for the Network layer. Layer 2 only cares about the <em>next hop</em> on the local wire.
</div>

<div class="highlight-box">
<strong>Attack preview:</strong> {{ARP Spoofing}} lets attackers answer "I'm the gateway!" with a lie — suddenly all your traffic flows through them. {{MAC Flooding}} overwhelms switches until they broadcast your data to everyone. {{VLAN Hopping}} jumps between isolated networks as if walls didn't exist.
</div>
""",
                        diagram="""flowchart TB
  subgraph OSI["<b>Your Data's Journey — Local Delivery</b>"]
    direction TB
    L7["7. Application 💻<br/>HTTP Request"]
    L6["6. Presentation 🔒<br/>Encrypted"]
    L5["5. Session 🔗<br/>Session active"]
    L4["4. Transport 📦<br/>TCP Segments"]
    L3["3. Network 🌐<br/>IP Packets"]
    L2["2. Data Link 🔗<br/>Ethernet Frames + MAC"]
    L1["1. Physical"]
  end
  style L7 fill:#dbeafe,stroke:#3b82f6
  style L6 fill:#dbeafe,stroke:#3b82f6
  style L5 fill:#dbeafe,stroke:#3b82f6
  style L4 fill:#dbeafe,stroke:#3b82f6
  style L3 fill:#dbeafe,stroke:#3b82f6
  style L2 fill:#f0fdf4,stroke:#059669,color:#064e3b,stroke-width:3px
  style L1 fill:#e2e8f0,stroke:#94a3b8
""",
                    ),
                    step(
                        "Scene 1: Physical Layer — Into the Wild",
                        """
<div class="highlight-box">
<strong>📍 Finally — Layer 1, the Physical layer.</strong> All the packaging above was just preparation. Now your data leaves the computer.
</div>

<p>Your Wi-Fi card modulates the Ethernet frame into radio waves at 2.4 GHz. The bits fly through the air at the speed of light:</p>

<pre style="font-size:18px; letter-spacing:2px;">10110010 01101001 01110100 01110011...</pre>

<p>Into the router, down the Ethernet cable as electrical voltages, through a fiber optic line as pulses of light to your ISP, under the ocean in submarine cables, and back up — arriving at Google's data center.</p>

<div class="example-box">
<strong>The miracle:</strong> Your data is now pure energy. It has been encrypted, chopped, addressed, framed, and finally converted to physical signals — all in under a second.
</div>

<div class="highlight-box">
<strong>Attack preview:</strong> At Layer 1, attackers don't need to break encryption or guess passwords — they just tap the wire. A {{Network Tapping}} device called the Throwing Star LAN Tap clips onto Ethernet cables to copy every passing bit. An {{Evil Maid Attack}} plugs malicious USB hardware directly into your computer. A {{Rogue Access Point}} catches Wi-Fi signals out of thin air.
</div>
""",
                        diagram="""flowchart TB
  subgraph OSI["<b>Your Data's Journey — Onto the Wire!</b>"]
    direction TB
    L7["7. Application 💻<br/>HTTP Request"]
    L6["6. Presentation 🔒<br/>Encrypted"]
    L5["5. Session 🔗<br/>Session active"]
    L4["4. Transport 📦<br/>TCP Segments"]
    L3["3. Network 🌐<br/>IP Packets"]
    L2["2. Data Link 🔗<br/>Ethernet Frames"]
    L1["1. Physical ⚡<br/>Radio Waves / Voltage"]
  end
  style L7 fill:#dbeafe,stroke:#3b82f6
  style L6 fill:#dbeafe,stroke:#3b82f6
  style L5 fill:#dbeafe,stroke:#3b82f6
  style L4 fill:#dbeafe,stroke:#3b82f6
  style L3 fill:#dbeafe,stroke:#3b82f6
  style L2 fill:#dbeafe,stroke:#3b82f6
  style L1 fill:#f0fdf4,stroke:#059669,color:#064e3b,stroke-width:3px
""",
                    ),
                    step(
                        "Arrival — Decapsulation on the Other Side",
                        """
<div class="highlight-box">
<strong>📍 The bits arrive at Google's server. Now the journey reverses.</strong>
</div>

<p>Google's server receives the raw bits and processes them in reverse — each layer strips the envelope that your computer added on the way out:</p>

<table>
  <tr><th>Layer</th><th>What the server does</th></tr>
  <tr><td><strong>1. Physical</strong></td><td>Receives radio waves / light pulses → converts to bits</td></tr>
  <tr><td><strong>2. Data Link</strong></td><td>Strips the Ethernet frame — destination MAC matches? Yes → pass up</td></tr>
  <tr><td><strong>3. Network</strong></td><td>Strips the IP header — destination IP matches? Yes → pass up</td></tr>
  <tr><td><strong>4. Transport</strong></td><td>Strips the TCP header — reassembles segments in correct order</td></tr>
  <tr><td><strong>5. Session</strong></td><td>Confirms the session is still valid and active</td></tr>
  <tr><td><strong>6. Presentation</strong></td><td>Decrypts the TLS layer — revealing the original HTTP request</td></tr>
  <tr><td><strong>7. Application</strong></td><td>Web server reads: <code>GET / HTTP/1.1</code> — and sends the Google homepage</td></tr>
</table>

<div class="highlight-box">
<strong>This is the beauty of the {{OSI Model}}:</strong> Each layer only needs to understand its own job. A router doesn't care about your HTTPS session. A switch doesn't care about your IP address. They all just handle their layer and pass the rest up or down.
</div>
""",
                        diagram="""flowchart LR
  subgraph Send[<b>Sender — Encapsulation</b>]
    S7["7. App"] --> S6["6. Pres"]
    S6 --> S5["5. Sess"]
    S5 --> S4["4. Trans"]
    S4 --> S3["3. Net"]
    S3 --> S2["2. D-Link"]
    S2 --> S1["1. Phys ⚡"]
  end
  W["━━━━━━━━━━━━━━━"]
  subgraph Recv[<b>Receiver — Decapsulation</b>]
    R1["1. Phys ⚡"] --> R2["2. D-Link"]
    R2 --> R3["3. Net"]
    R3 --> R4["4. Trans"]
    R4 --> R5["5. Sess"]
    R5 --> R6["6. Pres"]
    R6 --> R7["7. App ✅"]
  end
  S1 --> W --> R1
  style W fill:#f8fafc,stroke:#64748b,stroke-width:2px
""",
                    ),
                    step(
                        "Attack Map — Where Things Can Go Wrong",
                        """
<p>Now that you've seen how data travels through all 7 layers, you can see exactly where attackers strike. <strong>Every layer has a weakness.</strong></p>

<table>
  <tr><th>Layer</th><th>Attack</th><th>The Weakness</th></tr>
  <tr><td><strong>7 Application</strong></td><td>{{SQL Injection}}, {{XSS}}, {{CSRF}}, {{Credential Stuffing}}</td><td>Application code trusts user input without validation</td></tr>
  <tr><td><strong>6 Presentation</strong></td><td>{{SSL Stripping}}, {{POODLE}}, {{Certificate Spoofing}}</td><td>Encryption can be downgraded or bypassed with forged certs</td></tr>
  <tr><td><strong>5 Session</strong></td><td>{{Session Hijacking}}, {{EternalBlue}}</td><td>Weak session tokens leave doors open; unpatched RPC services are exploitable</td></tr>
  <tr><td><strong>4 Transport</strong></td><td>{{SYN Flood}}, {{Port Scanning}}, {{UDP Amplification}}</td><td>Connection state can be exhausted; open ports invite probing</td></tr>
  <tr><td><strong>3 Network</strong></td><td>{{IP Spoofing}}, {{Smurf Attack}}, {{BGP Route Hijacking}}</td><td>No authentication in IP headers; routing trust is blind</td></tr>
  <tr><td><strong>2 Data Link</strong></td><td>{{ARP Spoofing}}, {{MAC Flooding}}, {{VLAN Hopping}}</td><td>ARP has no authentication; switches can be forced to broadcast</td></tr>
  <tr><td><strong>1 Physical</strong></td><td>{{Evil Maid Attack}}, {{Network Tapping}}, {{Rogue Access Point}}</td><td>Physical access bypasses every software defense</td></tr>
</table>

<div class="highlight-box">
<strong>Let's go deeper.</strong> Each of the 7 tutorials in this course dives into one layer's attacks in detail. You'll learn the exact tools and techniques — from hardware keyloggers at Layer 1 to SQL injection at Layer 7.
</div>
""",
                        diagram="""flowchart LR
  C["💻 Your Browser"] -->|"Data flows down (L7→L1)"| W["🔌 Internet"]
  W -->|"Then back up (L1→L7)"| S["☁️ Google Server"]
  A["👤 Attacker"] -.->|"Can strike at ANY layer"| W
  A -.->|"ARP Spoofing • SYN Flood<br/>Session Hijack • SSL Strip<br/>SQL Injection • and more"| C
  style A fill:#fecaca,stroke:#ef4444,stroke-width:2px
  style C fill:#dbeafe,stroke:#3b82f6
  style S fill:#f0fdf4,stroke:#059669
""",
                    ),
                ],
                [
                    "Your data starts at Layer 7 (Application) and gets wrapped in headers at each layer as it travels down to Layer 1 (Physical) — this is Encapsulation.",
                    "On the receiving end, the process reverses from Layer 1 up to Layer 7, stripping headers — this is Decapsulation.",
                    "Every OSI layer has unique attack surfaces: from physical tapping at L1 to SQL injection at L7. Each of the 7 detailed tutorials covers one layer's attacks.",
                ],
            ),
        ],
    },
    {
        "id": "osi-l1",
        "title": "Layer 1 — Physical Layer",
        "short": "Layer 1 — Physical",
        "c_idx": 1,
        "lessons": [
            lesson(
                1,
                "Physical Tampering, Tapping & Rogue APs",
                "The Physical layer is where raw bits travel over wire, radio, or light. Attackers who access the physical medium bypass all software-layer security controls — firewalls, encryption, and authentication are irrelevant if the hardware itself is compromised.",
                [
                    step(
                        "Protocols & Hardware at Layer 1",
                        """
<div class="highlight-box">
Layer 1 defines the <strong>physical medium</strong> and how raw bits are transmitted — voltage levels, radio frequencies, cable types, and connector shapes.
</div>
<p>Common technologies:</p>
<ul>
  <li><strong>Ethernet cables</strong> (Cat5e, Cat6) — twisted-pair copper wire</li>
  <li><strong>Fiber optics</strong> — light pulses through glass strands</li>
  <li><strong>Wi-Fi radio frequencies</strong> — 2.4 GHz and 5 GHz bands</li>
  <li><strong>Hubs</strong> — dumb repeaters that broadcast every signal to all ports</li>
</ul>
<div class="example-box">
Key idea: if you control the wire or the airwaves, you control the data — regardless of what the upper layers try to enforce.
</div>
""",
                    ),
                    step(
                        "Physical Tampering & Evil Maid Attacks",
                        """
<p>An <strong>{{Evil Maid Attack}}</strong> occurs when an attacker gains brief physical access to a device and installs malicious hardware or software.</p>
<table>
  <tr><th>Tool</th><th>What it does</th></tr>
  <tr><td><strong>USB Rubber Ducky</strong></td><td>Appears as a keyboard; injects keystrokes at high speed to install backdoors or exfiltrate data</td></tr>
  <tr><td><strong>PoisonTap</strong></td><td>Plugged into a USB port, it hijacks network traffic by posing as a network interface with priority routes</td></tr>
  <tr><td><strong>Hardware Keylogger</strong></td><td>Inline device between keyboard and computer that logs every keystroke</td></tr>
</table>
<div class="highlight-box">
<strong>Defense:</strong> Full-disk encryption, locked BIOS/UEFI, tamper-evident seals, and strict physical access controls.
</div>
""",
                        diagram="""flowchart TB
  A[Attacker gains physical access] --> B[Plug in malicious USB]
  B --> C{Type of device?}
  C --> D[Rubber Ducky - keystroke injection]
  C --> E[PoisonTap - network hijack]
  C --> F[Keylogger - capture keystrokes]
  D --> G[Backdoor installed]
  E --> G
  F --> H[Credentials stolen]
  style A fill:#fecaca,stroke:#ef4444
  style G fill:#fecaca,stroke:#ef4444
  style H fill:#fecaca,stroke:#ef4444
""",
                    ),
                    step(
                        "Network Tapping & Rogue Access Points",
                        """
<p><strong>{{Network Tapping}}</strong> physically intercepts cable traffic:</p>
<ul>
  <li><strong>Throwing Star LAN Tap</strong> — a passive tap inserted inline with an Ethernet cable; all traffic passes through it and is copied to a monitor port</li>
  <li><strong>Splitter taps</strong> — optical splitters on fiber lines</li>
</ul>
<p><strong>{{Rogue Access Point}}</strong> attacks deploy unauthorized Wi-Fi hotspots:</p>
<ul>
  <li>Attacker sets up an open Wi-Fi AP with a legitimate-sounding SSID</li>
  <li>{{Deauthentication Attack}} disconnects legitimate clients to force them onto the rogue AP</li>
  <li>Once connected, attacker intercepts all unencrypted traffic and can perform {{MITM}}</li>
</ul>
""",
                        diagram="""flowchart LR
  subgraph Normal[Normal Operation]
    C[Client] --> AP[Legitimate AP]
  end
  subgraph Attack[Attack Scenario]
    A[Rogue AP] --> C2[Victim connects]
    D[Deauth frames] -.->|Disconnect| C2
    C2 --> A
    A --> Att[Attacker captures traffic]
  end
  style A fill:#fecaca,stroke:#ef4444
  style Att fill:#fecaca,stroke:#ef4444
  style D fill:#fecaca,stroke:#ef4444
""",
                    ),
                ],
                [
                    "Layer 1 attacks require physical proximity or access to the medium.",
                    "Evil Maid attacks, network taps, and rogue APs bypass all software defenses.",
                    "Defenses include encryption, physical access controls, and tamper monitoring.",
                ],
            ),
        ],
    },
    {
        "id": "osi-l2",
        "title": "Layer 2 — Data Link Layer",
        "short": "Layer 2 — Data Link",
        "c_idx": 2,
        "lessons": [
            lesson(
                1,
                "ARP Spoofing, MAC Flooding & VLAN Hopping",
                "Layer 2 handles local communication within a broadcast domain using {{MAC Address}}es. Switches, ARP, and VLANs all operate here — and all share a fundamental weakness: trust without authentication.",
                [
                    step(
                        "Protocols & Hardware at Layer 2",
                        """
<div class="highlight-box">
Layer 2 frames data for transmission on the physical medium, using <strong>MAC addresses</strong> to identify devices on the same network segment.
</div>
<p>Key technologies:</p>
<ul>
  <li><strong>Ethernet frames</strong> — source/destination MAC, EtherType, payload, FCS</li>
  <li><strong>{{ARP}}</strong> — maps IP addresses to MAC addresses (no authentication)</li>
  <li><strong>Switches</strong> — forward frames based on MAC address tables ({{CAM Table}})</li>
  <li><strong>VLANs</strong> — logically segment a switch into isolated broadcast domains using {{802.1Q}} tagging</li>
  <li><strong>Wi-Fi (802.11)</strong> — wireless frames with MAC addressing</li>
</ul>
""",
                    ),
                    step(
                        "ARP Spoofing / Poisoning",
                        """
<p><strong>{{ARP Spoofing}}</strong> (ARP poisoning) is the most common Layer 2 attack in pentesting labs.</p>
<div class="highlight-box">
The attacker sends forged ARP replies, associating their MAC address with the IP of a legitimate host — typically the default gateway.
</div>
<ol>
  <li>Attacker sends fake ARP: "192.168.1.1 is at AA:BB:CC:DD:EE:FF"</li>
  <li>Victim updates ARP cache with the attacker's MAC for the gateway IP</li>
  <li>All victim traffic to the Internet goes through the attacker instead of the real router</li>
  <li>Attacker inspects, modifies, or forwards the traffic ({{MITM}})</li>
</ol>
<p>Tools: <code>arpspoof</code>, <code>Bettercap</code>, <code>Ettercap</code></p>
""",
                        diagram="""flowchart LR
  V[Victim] -->|Traffic for gateway| A[Attacker MAC]
  A -->|Forwards or inspects| R[Real Gateway]
  A -.->|Forged ARP: gateway = MY-MAC| V
  style V fill:#dbeafe,stroke:#3b82f6
  style A fill:#fecaca,stroke:#ef4444
  style R fill:#f0fdf4,stroke:#059669
""",
                    ),
                    step(
                        "MAC Flooding",
                        """
<p><strong>{{MAC Flooding}}</strong> targets the switch's forwarding logic.</p>
<ul>
  <li>A switch's {{CAM Table}} has limited capacity (e.g., 8,000 entries)</li>
  <li>Attacker floods the switch with frames containing many fake source MAC addresses</li>
  <li>When the CAM table fills, the switch enters a <strong>fail-open</strong> state</li>
  <li>In fail-open mode, the switch behaves like a <strong>hub</strong> — broadcasting all frames to all ports</li>
  <li>The attacker can now sniff traffic meant for any host on the switch</li>
</ul>
<div class="highlight-box">
<strong>Defense:</strong> Port security limits the number of MAC addresses per port. Dynamic ARP Inspection (DAI) validates ARP packets.
</div>
""",
                    ),
                    step(
                        "VLAN Hopping",
                        """
<p><strong>{{VLAN Hopping}}</strong> exploits {{802.1Q}} trunking to bypass VLAN isolation.</p>
<p>Two main techniques:</p>
<ol>
  <li><strong>Switch Spoofing</strong> — attacker's device impersonates a switch and negotiates trunking, gaining access to all VLANs</li>
  <li><strong>Double Tagging</strong> — attacker sends a frame with two 802.1Q tags; the first switch strips the outer tag (native VLAN), forwarding the inner tag to a different VLAN</li>
</ol>
<div class="highlight-box">
<strong>Impact:</strong> An attacker on VLAN 10 can reach hosts on VLAN 20 that should be completely isolated.
</div>
""",
                    ),
                ],
                [
                    "ARP Spoofing poisons the IP-to-MAC mapping for MITM positioning.",
                    "MAC Flooding exhausts switch CAM tables, forcing hub-mode broadcast.",
                    "VLAN Hopping bypasses VLAN isolation using trunking or double tagging.",
                ],
            ),
        ],
    },
    {
        "id": "osi-l3",
        "title": "Layer 3 — Network Layer",
        "short": "Layer 3 — Network",
        "c_idx": 3,
        "lessons": [
            lesson(
                1,
                "IP Spoofing, ICMP Attacks & BGP Hijacking",
                "Layer 3 routes packets across networks using logical {{IP Address}}es. Routing protocols and IP header fields rely on trust — attackers exploit that trust to redirect, forge, or amplify traffic at internet scale.",
                [
                    step(
                        "Protocols at Layer 3",
                        """
<div class="highlight-box">
Layer 3 provides logical addressing and path selection so packets can travel between different networks.
</div>
<p>Key protocols:</p>
<ul>
  <li><strong>IPv4 / IPv6</strong> — packet headers with source/destination IP addresses</li>
  <li><strong>{{ICMP}}</strong> — diagnostics (ping), error reporting (Destination Unreachable, TTL Exceeded)</li>
  <li><strong>IPsec</strong> — security extensions for IP (encryption + authentication)</li>
  <li><strong>BGP</strong> — Border Gateway Protocol, the routing protocol of the Internet</li>
  <li><strong>OSPF</strong> — Open Shortest Path First, a dynamic routing protocol for internal networks</li>
</ul>
""",
                    ),
                    step(
                        "IP Spoofing & ICMP Attacks",
                        """
<p><strong>{{IP Spoofing}}</strong> alters the source IP in packet headers to disguise the sender's identity.</p>
<ul>
  <li>Bypasses IP-based access controls</li>
  <li>Enables amplification attacks (source appears to be the victim)</li>
  <li>Complicates forensic attribution</li>
</ul>
<p><strong>{{ICMP}} abuse:</strong></p>
<table>
  <tr><th>Attack</th><th>Mechanism</th></tr>
  <tr><td><strong>{{Ping Flood}}</strong></td><td>Massive volume of ICMP Echo Requests to consume bandwidth and CPU</td></tr>
  <tr><td><strong>{{Smurf Attack}}</strong></td><td>ICMP Echo Request to broadcast address with spoofed victim source; all hosts reply to victim</td></tr>
</table>
<div class="highlight-box">
<strong>Defense:</strong> Ingress/egress filtering (BCP 38) blocks packets with non-routable or unexpected source IPs at network boundaries.
</div>
""",
                        diagram="""flowchart TB
  A[Attacker] -->|Spoofed ICMP Echo Request src=VICTIM| B[Network Broadcast]
  B --> C[Host 1 replies to victim]
  B --> D[Host 2 replies to victim]
  B --> E[Host 3 replies to victim]
  C --> F[Victim overwhelmed]
  D --> F
  E --> F
  style A fill:#fecaca,stroke:#ef4444
  style F fill:#fecaca,stroke:#ef4444
""",
                    ),
                    step(
                        "BGP Route Hijacking",
                        """
<p><strong>{{BGP Route Hijacking}}</strong> exploits trust between autonomous systems on the Internet.</p>
<div class="highlight-box">
An attacker-controlled AS announces IP prefixes it does not legitimately own, causing upstream routers to update their routing tables toward the attacker.
</div>
<ol>
  <li>Attacker configures a BGP router to announce a victim's IP prefix (e.g., a bank's IP range)</li>
  <li>Upstream ISPs accept the more specific or equal route</li>
  <li>Traffic destined for the victim's network is rerouted through attacker infrastructure</li>
  <li>Attacker can inspect, modify, or drop traffic before forwarding it</li>
</ol>
<p>Notable example: 2018 BGP hijack of Amazon's DNS — attackers redirected traffic to a phishing site for cryptocurrency wallets.</p>
""",
                        diagram="""flowchart LR
  U[User] -->|Routes to bank| I1[ISP Router]
  I1 -->|Legitimate path| B[Bank AS]
  I1 -->|Hijacked route| A[Attacker AS]
  A --> B
  style A fill:#fecaca,stroke:#ef4444
  style B fill:#f0fdf4,stroke:#059669
""",
                    ),
                ],
                [
                    "IP Spoofing forges source addresses to bypass access controls and enable amplification.",
                    "ICMP abuse includes Ping Floods and Smurf Attacks for denial of service.",
                    "BGP Route Hijacking reroutes Internet traffic through attacker-controlled networks.",
                ],
            ),
        ],
    },
    {
        "id": "osi-l4",
        "title": "Layer 4 — Transport Layer",
        "short": "Layer 4 — Transport",
        "c_idx": 4,
        "lessons": [
            lesson(
                1,
                "SYN Flood, Port Scanning & UDP Amplification",
                "Layer 4 manages host-to-host communication sessions. {{TCP}} provides reliable, connection-oriented delivery via the {{Three-Way Handshake}}; {{UDP}} is connectionless and faster. Both have distinct attack surfaces.",
                [
                    step(
                        "Protocols at Layer 4",
                        """
<div class="highlight-box">
Layer 4 segments and reassembles data for transport between applications on different hosts.
</div>
<p>Key protocols:</p>
<ul>
  <li><strong>{{TCP}}</strong> — connection-oriented, reliable, sequenced delivery</li>
  <li><strong>{{UDP}}</strong> — connectionless, best-effort delivery, low overhead</li>
</ul>
<p>The {{Three-Way Handshake}}:</p>
<pre>Client → Server: SYN
Server → Client: SYN-ACK
Client → Server: ACK</pre>
<p>This handshake creates state on both ends — state that attacks can exhaust or manipulate.</p>
""",
                        diagram="""flowchart LR
  C[Client] -->|SYN| S[Server]
  S -->|SYN-ACK| C
  C -->|ACK| S
  S -->|Connection established| C
  style C fill:#dbeafe,stroke:#3b82f6
  style S fill:#f0fdf4,stroke:#059669
""",
                    ),
                    step(
                        "SYN Flood (TCP DoS)",
                        """
<p><strong>{{SYN Flood}}</strong> is a classic denial-of-service attack against TCP's stateful handshake.</p>
<div class="highlight-box">
The attacker sends a high volume of SYN packets with spoofed source IPs — and never sends the final ACK to complete the handshake.
</div>
<ol>
  <li>Server receives SYN, allocates memory for a half-open connection, replies with SYN-ACK</li>
  <li>Attacker never sends the ACK (or spoofs a non-existent source IP)</li>
  <li>The half-open connection sits in the backlog queue until a timeout</li>
  <li>Backlog fills up — legitimate clients cannot connect</li>
</ol>
<p><strong>Defenses:</strong> SYN cookies, increased backlog, rate limiting, and firewalls that proxy TCP handshakes.</p>
""",
                        diagram="""flowchart LR
  A[Attacker] -->|SYN x 1000| S[Target Server]
  A -->|SYN x 1000| S
  A -->|SYN x 1000| S
  S -->|SYN-ACK for each| A
  L[Legitimate Client] -->|SYN| S
  S -->|Backlog full - REJECTED| L
  style A fill:#fecaca,stroke:#ef4444
  style S fill:#fecaca,stroke:#ef4444
  style L fill:#dbeafe,stroke:#3b82f6
""",
                    ),
                    step(
                        "Port Scanning with Nmap",
                        """
<p><strong>{{Port Scanning}}</strong> is typically the first step in network recon. {{Nmap}} is the industry standard.</p>
<table>
  <tr><th>Scan type</th><th>Packet sent</th><th>Response meaning</th></tr>
  <tr><td><strong>SYN scan</strong> (-sS)</td><td>SYN only</td><td>SYN-ACK = open; RST = closed</td></tr>
  <tr><td><strong>TCP Connect</strong> (-sT)</td><td>Full handshake</td><td>Completed = open</td></tr>
  <tr><td><strong>FIN scan</strong> (-sF)</td><td>FIN packet</td><td>No response = open (RFC non-compliant hosts)</td></tr>
  <tr><td><strong>UDP scan</strong> (-sU)</td><td>UDP datagram</td><td>ICMP Unreachable = closed; no response = open/filtered</td></tr>
</table>
<div class="highlight-box">
<strong>Pentesting tip:</strong> SYN scan (-sS) is the default. It is fast and does not complete the TCP handshake, which means it often avoids application-level logging.
</div>
""",
                    ),
                    step(
                        "UDP Amplification",
                        """
<p><strong>{{UDP Amplification}}</strong> exploits the connectionless nature of {{UDP}} for massive DDoS attacks.</p>
<div class="highlight-box">
A small query (e.g., 64 bytes) to an open UDP service can generate a response 50-100x larger. The attacker spoofs the victim's IP as the query source.
</div>
<ol>
  <li>Attacker sends many small DNS/NTP queries with spoofed source IP = victim</li>
  <li>Servers send large responses to the victim's IP</li>
  <li>Victim's bandwidth is saturated with unwanted traffic</li>
</ol>
<p><strong>Amplification factors:</strong> DNS ~50x, NTP ~550x, Memcached ~50,000x</p>
<p><strong>Defenses:</strong> Disable open recursion on DNS/NTP servers, rate-limit responses, filter spoofed traffic at edge.</p>
""",
                    ),
                ],
                [
                    "SYN Flood exhausts TCP connection pools with half-open handshakes.",
                    "Port scanning (Nmap) identifies open services for targeted attacks.",
                    "UDP Amplification uses spoofed queries to generate massive DDoS traffic.",
                ],
            ),
        ],
    },
    {
        "id": "osi-l5",
        "title": "Layer 5 — Session Layer",
        "short": "Layer 5 — Session",
        "c_idx": 5,
        "lessons": [
            lesson(
                1,
                "Session Hijacking & RPC Exploitation",
                "Layer 5 establishes, manages, and terminates dialogs between applications. If an attacker can hijack a session or exploit session setup, they can impersonate a user without ever knowing their password.",
                [
                    step(
                        "Protocols at Layer 5",
                        """
<div class="highlight-box">
The Session layer controls the dialog between two communicating hosts — when to start, stop, pause, and resume conversations.
</div>
<p>Key protocols:</p>
<ul>
  <li><strong>{{NetBIOS}}</strong> — provides naming, session, and datagram services on Windows networks</li>
  <li><strong>{{RPC}}</strong> — enables a program to execute code on a remote system</li>
  <li><strong>PPTP</strong> — Point-to-Point Tunneling Protocol for VPN connections</li>
  <li><strong>SOCKS</strong> — a proxy protocol that relays traffic at the session level</li>
</ul>
""",
                    ),
                    step(
                        "Session Hijacking",
                        """
<p><strong>{{Session Hijacking}}</strong> (also called cookie hijacking or sidejacking) allows an attacker to take over an authenticated user session.</p>
<table>
  <tr><th>Method</th><th>How it works</th></tr>
  <tr><td><strong>Session token theft</strong></td><td>Intercepting cookies or tokens via packet sniffing (especially over unencrypted HTTP)</td></tr>
  <tr><td><strong>Session prediction</strong></td><td>Analyzing weak token generation algorithms to guess the next valid session ID</td></tr>
  <tr><td><strong>Session fixation</strong></td><td>Forcing a victim to use a session ID known to the attacker (e.g., via URL parameter)</td></tr>
</table>
<div class="highlight-box">
<strong>Defense:</strong> Use HTTPS-only cookies with Secure + HttpOnly flags, regenerate session IDs after login, implement short session timeouts.
</div>
""",
                        diagram="""flowchart LR
  V[Victim] -->|Login with session cookie| S[Web Server]
  A[Attacker] -->|Intercepts cookie / guesses session ID| S
  A -->|Impersonates victim| S
  S -->|Serves victim's data to attacker| A
  style V fill:#dbeafe,stroke:#3b82f6
  style A fill:#fecaca,stroke:#ef4444
  style S fill:#fef3c7,stroke:#f59e0b
""",
                    ),
                    step(
                        "RPC Exploitation",
                        """
<p><strong>{{RPC}}</strong> vulnerabilities have been at the center of some of the most damaging cyberattacks in history.</p>
<div class="highlight-box">
<strong>{{EternalBlue}}</strong> (MS17-010) exploited a flaw in Windows SMB/NetBIOS session setup — a Layer 5 RPC mechanism — to achieve Remote Code Execution.
</div>
<p>How EternalBlue works at the session layer:</p>
<ol>
  <li>Attacker sends a specially crafted SMB packet to the target's NetBIOS session service</li>
  <li>The malformed RPC call triggers a buffer overflow in the kernel</li>
  <li>Attacker gains SYSTEM-level code execution</li>
  <li>Used by WannaCry and NotPetya to spread across networks</li>
</ol>
<p><strong>Defense:</strong> Patch promptly, disable unnecessary RPC services, segment networks, block SMB (port 445) at the edge.</p>
""",
                    ),
                ],
                [
                    "Session Hijacking steals or predicts tokens to impersonate authenticated users.",
                    "RPC exploits (like EternalBlue) target session setup mechanisms for code execution.",
                    "Session layer defenses include secure cookies, token regeneration, and patching RPC services.",
                ],
            ),
        ],
    },
    {
        "id": "osi-l6",
        "title": "Layer 6 — Presentation Layer",
        "short": "Layer 6 — Presentation",
        "c_idx": 6,
        "lessons": [
            lesson(
                1,
                "SSL/TLS Downgrade, Certificate Spoofing & Serialization Exploits",
                "Layer 6 translates, encrypts, and compresses data between the application and network layers. Attacks here target the <em>trust</em> in encryption and data format handling.",
                [
                    step(
                        "Protocols & Formats at Layer 6",
                        """
<div class="highlight-box">
The Presentation layer ensures data from the application layer is in a format the network can transmit — and vice versa. This includes encryption, encoding, and compression.
</div>
<p>Key technologies:</p>
<ul>
  <li><strong>{{SSL/TLS}}</strong> — encrypts data between client and server (though TLS sits between L5 and L6 in practice, it is most commonly associated with Presentation-layer functions)</li>
  <li><strong>MIME</strong> — encoding for email attachments</li>
  <li><strong>ASCII / UTF-8</strong> — character encoding</li>
  <li><strong>JPEG, PNG, GIF</strong> — image compression formats</li>
  <li><strong>JSON, XML, YAML</strong> — structured data serialization formats</li>
</ul>
""",
                    ),
                    step(
                        "SSL/TLS Downgrade Attacks",
                        """
<p><strong>{{SSL Stripping}}</strong> and protocol downgrade attacks force a secure connection to use a weaker or disabled encryption standard.</p>
<table>
  <tr><th>Attack</th><th>Mechanism</th></tr>
  <tr><td><strong>sslstrip</strong></td><td>Intercepts HTTPS links and rewrites them to HTTP; the attacker communicates with the server over HTTPS while the victim uses plain HTTP</td></tr>
  <tr><td><strong>{{POODLE}}</strong></td><td>Forces the connection to fall back to SSL 3.0, then exploits padding oracle behavior to decrypt cookies</td></tr>
  <tr><td><strong>Protocol downgrade</strong></td><td>Manipulates the TLS handshake to negotiate a weaker cipher suite that can be cracked</td></tr>
</table>
<div class="highlight-box">
<strong>Defense:</strong> Disable SSL 2.0/3.0 and TLS 1.0 on servers; enforce HSTS (HTTP Strict Transport Security) to prevent protocol downgrade; use TLS 1.2+ only.
</div>
""",
                        diagram="""flowchart LR
  V[Victim] -->|HTTP (downgraded)| A[Attacker proxy]
  A -->|HTTPS| S[Secure Server]
  A -.->|sslstrip rewrites HTTPS links to HTTP| V
  style V fill:#dbeafe,stroke:#3b82f6
  style A fill:#fecaca,stroke:#ef4444
  style S fill:#f0fdf4,stroke:#059669
""",
                    ),
                    step(
                        "Certificate Spoofing & Serialization Exploits",
                        """
<p><strong>{{Certificate Spoofing}}</strong> — in a MitM position, an attacker presents their own TLS certificate to the victim. If the victim ignores certificate warnings (or the attacker controls a trusted CA), the encrypted session is intercepted.</p>
<p><strong>{{Serialization Exploit}}</strong> — applications that deserialize data from untrusted sources are vulnerable to code injection:</p>
<ul>
  <li><strong>Insecure Deserialization</strong> — crafting malicious JSON/XML/YAML that triggers arbitrary code during parsing</li>
  <li><strong>XXE (XML External Entity)</strong> — exploiting XML parsers to read local files or perform SSRF</li>
  <li><strong>YAML deserialization</strong> — Python/Java YAML parsers can execute system commands when instantiating objects</li>
</ul>
<div class="highlight-box">
<strong>Defense:</strong> Validate TLS certificates properly, pin certificates for critical services, use safe deserialization libraries, never deserialize untrusted input.
</div>
""",
                    ),
                ],
                [
                    "SSL/TLS downgrade attacks strip encryption via sslstrip or exploit legacy protocol flaws like POODLE.",
                    "Certificate Spoofing enables MitM interception of encrypted sessions.",
                    "Serialization exploits in JSON/XML/YAML parsers can lead to remote code execution.",
                ],
            ),
        ],
    },
    {
        "id": "osi-l7",
        "title": "Layer 7 — Application Layer",
        "short": "Layer 7 — Application",
        "c_idx": 7,
        "lessons": [
            lesson(
                1,
                "Web Attacks, Credential Stuffing & DNS Poisoning",
                "Layer 7 is closest to the user — web browsers, email clients, and file transfers. Most real-world breaches start here because application code is complex and every user-facing feature is a potential entry point.",
                [
                    step(
                        "Protocols at Layer 7",
                        """
<div class="highlight-box">
The Application layer provides network services directly to end-user applications.
</div>
<p>Key protocols:</p>
<ul>
  <li><strong>HTTP / HTTPS</strong> — web browsing</li>
  <li><strong>SMTP, POP3, IMAP</strong> — email</li>
  <li><strong>FTP</strong> — file transfer</li>
  <li><strong>SSH</strong> — secure remote access</li>
  <li><strong>DNS</strong> — domain name resolution (often listed at L7 in practical models)</li>
</ul>
""",
                    ),
                    step(
                        "Web Application Attacks",
                        """
<p>Web applications are the most targeted attack surface. Three critical vulnerability classes:</p>
<table>
  <tr><th>Attack</th><th>Description</th><th>Impact</th></tr>
  <tr><td><strong>{{SQL Injection}} (SQLi)</strong></td><td>Injecting SQL commands through user input</td><td>Database compromise, data theft, authentication bypass</td></tr>
  <tr><td><strong>{{XSS}} (Cross-Site Scripting)</strong></td><td>Injecting client-side scripts into web pages</td><td>Session theft, phishing, defacement</td></tr>
  <tr><td><strong>{{CSRF}} (Cross-Site Request Forgery)</strong></td><td>Tricking authenticated users into submitting unwanted actions</td><td>State-changing operations without consent</td></tr>
</table>
<div class="highlight-box">
<strong>Impact:</strong> SQLi can dump entire databases. XSS can steal every user's session. CSRF can change passwords or initiate transfers on behalf of a logged-in victim.
</div>
""",
                    ),
                    step(
                        "Credential Stuffing & Brute Force",
                        """
<p><strong>{{Credential Stuffing}}</strong> exploits password reuse at scale:</p>
<ul>
  <li>Attackers obtain credential dumps from data breaches (e.g., Have I Been Pwned)</li>
  <li>Automated scripts test each username/password pair across multiple target services</li>
  <li>Success rates of 0.5-2% are typical — devastating at millions of attempts</li>
</ul>
<p><strong>Brute Force</strong> with {{Hydra}}:</p>
<pre>hydra -l admin -P rockyou.txt ssh://192.168.1.100
hydra -L users.txt -P pass.txt ftp://target.com</pre>
<div class="highlight-box">
<strong>Defense:</strong> Multi-factor authentication (MFA), rate limiting, account lockout, and breach-monitoring services.
</div>
""",
                    ),
                    step(
                        "DNS Spoofing / Poisoning",
                        """
<p><strong>{{DNS Spoofing}}</strong> (cache poisoning) manipulates how domain names are resolved to IPs.</p>
<div class="highlight-box">
The attacker corrupts a DNS resolver's cache so that legitimate domain names resolve to attacker-controlled IP addresses.
</div>
<ol>
  <li>Attacker sends forged DNS responses to a recursive resolver before the legitimate response arrives</li>
  <li>Resolver caches the fraudulent record with a longer TTL</li>
  <li>Users querying bank.example receive the attacker's IP</li>
  <li>Attacker serves a phishing page that looks identical to the real site</li>
</ol>
<p><strong>Defenses:</strong> DNSSEC (DNSSEC signs DNS records), DNS over HTTPS (DoH), using trusted resolver configurations, monitoring unexpected DNS changes.</p>
""",
                        diagram="""flowchart LR
  U[User types bank.example] --> R[DNS Resolver]
  A[Attacker] -->|Forged DNS response - bank.example = ATTACKER-IP| R
  R -->|Cached poisoned record| U
  U -->|Connects to| A
  A --> P[Phishing site / proxy]
  style U fill:#dbeafe,stroke:#3b82f6
  style A fill:#fecaca,stroke:#ef4444
  style R fill:#fef3c7,stroke:#f59e0b
  style P fill:#fecaca,stroke:#ef4444
""",
                    ),
                ],
                [
                    "SQL Injection, XSS, and CSRF are the most critical web application attack classes.",
                    "Credential Stuffing exploits password reuse across services; MFAs block most automated attacks.",
                    "DNS Spoofing redirects users to malicious sites by corrupting resolver caches.",
                ],
            ),
        ],
    },
]

QUIZ_QUESTIONS = [
    # ── Layer 1: Physical Layer (c_idx=1) ──
    {"c": 1, "q": "A USB Rubber Ducky and PoisonTap are examples of tools used in what type of attack?",
     "o": ["ARP Spoofing", "Evil Maid / Physical Tampering", "DNS Poisoning", "VLAN Hopping"],
     "a": 1, "exp": "Evil Maid attacks involve brief physical access to insert malicious USB hardware. The Rubber Ducky injects keystrokes; PoisonTap hijacks network traffic."},

    {"c": 1, "q": "The Throwing Star LAN Tap is designed to intercept traffic on what medium?",
     "o": ["Ethernet cables", "Wi-Fi radio frequencies", "Fiber optic cables", "Serial/RS-232 cables"],
     "a": 0, "exp": "The Throwing Star LAN Tap is an inline passive tap for Ethernet cables. It copies all passing traffic to a monitor port for packet capture."},

    {"c": 1, "q": "What physical layer attack involves setting up an unauthorized Wi-Fi hotspot to trick users into connecting?",
     "o": ["Rogue Access Point", "MAC Flooding", "Session Hijacking", "SYN Flood"],
     "a": 0, "exp": "A Rogue AP is an unauthorized wireless access point deployed to intercept traffic. Combined with deauthentication attacks, attackers can force clients to connect to it."},

    {"c": 1, "q": "Deauthentication attacks specifically target which communication medium?",
     "o": ["Ethernet cables", "Fiber optics", "Wi-Fi radio frequencies", "Coaxial cables"],
     "a": 2, "exp": "Deauthentication attacks send forged 802.11 deauth frames over Wi-Fi. They disconnect clients from legitimate APs, often as a precursor to rogue AP attacks."},

    {"c": 1, "q": "Which attack method requires direct physical access to a target workstation?",
     "o": ["Hardware Keylogger / Evil Maid", "ARP Spoofing", "BGP Route Hijacking", "DNS Cache Poisoning"],
     "a": 0, "exp": "Hardware keyloggers and Evil Maid attacks require someone to physically access the machine — inserting a device inline with the keyboard or plugging into a USB port."},

    # ── Layer 2: Data Link Layer (c_idx=2) ──
    {"c": 2, "q": "ARP Spoofing positions an attacker to perform what kind of network attack?",
     "o": ["Denial of Service", "Man-in-the-Middle", "Buffer Overflow", "SQL Injection"],
     "a": 1, "exp": "By associating their MAC with a legitimate IP (usually the gateway), the attacker becomes a Man-in-the-Middle — all victim traffic passes through them."},

    {"c": 2, "q": "During a MAC Flooding attack, what happens to the switch once its CAM table is full?",
     "o": ["It falls back to hub mode, broadcasting all traffic to all ports", "It reboots and restores factory settings", "It automatically enables port security", "It drops all network traffic to prevent further attacks"],
     "a": 0, "exp": "When CAM table capacity is exhausted, many switches enter a fail-open state where they behave like hubs — broadcasting all frames to every port."},

    {"c": 2, "q": "VLAN Hopping using double tagging exploits which IEEE standard?",
     "o": ["802.11", "802.1Q", "802.3", "802.1X"],
     "a": 1, "exp": "Double tagging exploits the 802.1Q VLAN tagging standard. The outer tag is stripped by the first switch; the inner tag forwards the frame into a different VLAN."},

    {"c": 2, "q": "ARP operates at which layer of the OSI model?",
     "o": ["Layer 1 — Physical", "Layer 2 — Data Link", "Layer 3 — Network", "Layer 4 — Transport"],
     "a": 1, "exp": "ARP maps IP addresses to MAC addresses for local network delivery. It operates at Layer 2 (Data Link) because it deals with MAC addressing and frames."},

    {"c": 2, "q": "What fundamental security feature does ARP lack, making spoofing attacks possible?",
     "o": ["Authentication", "Encryption", "Compression", "Fragmentation"],
     "a": 0, "exp": "ARP has no built-in authentication. Any host on the network can send a forged ARP reply, and most OSes will accept it and update their ARP cache."},

    # ── Layer 3: Network Layer (c_idx=3) ──
    {"c": 3, "q": "In an IP Spoofing attack, which part of the IP packet does the attacker modify?",
     "o": ["Payload data", "Source IP address header field", "Destination MAC address", "TCP checksum"],
     "a": 1, "exp": "IP Spoofing falsifies the source IP address in the packet header to disguise the sender's identity or impersonate a trusted host."},

    {"c": 3, "q": "A Smurf attack amplifies traffic by sending ICMP Echo Requests to what destination?",
     "o": ["A broadcast address with a spoofed victim source IP", "The target directly with oversized ping packets", "DNS servers for further amplification", "Routers with malformed BGP updates"],
     "a": 0, "exp": "The attacker sends ICMP Echo Requests to a network's broadcast address with the victim's IP as the source. All hosts on the network reply to the victim."},

    {"c": 3, "q": "BGP Route Hijacking allows an attacker to achieve what outcome?",
     "o": ["Redirect Internet traffic through attacker-controlled routers", "Spoof MAC addresses on neighboring switches", "Crash DNS servers with amplification queries", "Bypass firewall rules using packet fragmentation"],
     "a": 0, "exp": "Attackers announce IP prefixes they don't own. Upstream routers update their tables to send traffic for those prefixes to the attacker's network."},

    {"c": 3, "q": "What protocol operates at Layer 3 and is used to exchange routing information between autonomous systems on the Internet?",
     "o": ["BGP", "TCP", "ARP", "HTTP"],
     "a": 0, "exp": "BGP (Border Gateway Protocol) is the routing protocol that connects autonomous systems on the Internet. It operates at Layer 3 (Network layer)."},

    {"c": 3, "q": "The ICMP protocol is commonly abused by attackers for which purpose?",
     "o": ["Host discovery and denial of service", "Web application authentication bypass", "Session token theft", "Email phishing"],
     "a": 0, "exp": "ICMP is used for ping sweeps (host discovery), Ping Floods and Smurf Attacks (DoS), and even covert data exfiltration via ICMP tunneling."},

    # ── Layer 4: Transport Layer (c_idx=4) ──
    {"c": 4, "q": "A SYN Flood exploits which phase of the TCP protocol lifecycle?",
     "o": ["Connection termination", "Three-way handshake", "Data transfer", "Flow control"],
     "a": 1, "exp": "The attacker sends many SYN packets without completing the handshake, leaving the server with half-open connections that exhaust the connection backlog."},

    {"c": 4, "q": "Nmap's SYN stealth scan (-sS) works by sending what kind of packets?",
     "o": ["SYN packets and analyzing the response without completing the handshake", "Complete TCP connection requests to every port", "UDP datagrams with spoofed source IPs", "ICMP Echo Requests to discover live hosts"],
     "a": 0, "exp": "SYN scan sends a SYN packet for each port. A SYN-ACK response means the port is open; RST means closed. The handshake is never completed."},

    {"c": 4, "q": "UDP Amplification works because of what property of UDP services?",
     "o": ["The response to a small query can be 50-100x larger than the request", "UDP is connection-oriented and maintains session state", "UDP packets are always larger than TCP packets", "UDP requires a three-way handshake before data transfer"],
     "a": 0, "exp": "Open UDP services like DNS and NTP can generate large responses from tiny queries. With a spoofed source IP, those responses flood the victim."},

    {"c": 4, "q": "Which tool is the industry standard for port scanning and service detection?",
     "o": ["Wireshark", "Nmap", "Metasploit", "Burp Suite"],
     "a": 1, "exp": "Nmap (Network Mapper) is the standard tool for port scanning, service version detection, OS fingerprinting, and network discovery in pentesting."},

    {"c": 4, "q": "The TCP three-way handshake establishes a connection using which sequence of flags?",
     "o": ["SYN → SYN-ACK → ACK", "SYN → ACK → SYN-ACK", "ACK → SYN → SYN-ACK", "SYN → SYN → ACK"],
     "a": 0, "exp": "The client sends SYN, the server replies with SYN-ACK, and the client sends ACK. Only then is the connection established and data can flow."},

    # ── Layer 5: Session Layer (c_idx=5) ──
    {"c": 5, "q": "Session Hijacking allows an attacker to do which of the following?",
     "o": ["Impersonate an authenticated user by stealing or guessing their session token", "Flood a server with incomplete TCP connections", "Exploit ARP cache to redirect local network traffic", "Inject SQL commands into a database"],
     "a": 0, "exp": "Session Hijacking involves intercepting or predicting session tokens/cookies to impersonate a legitimate authenticated user without credentials."},

    {"c": 5, "q": "EternalBlue (MS17-010) is a famous exploit that targets which Session layer protocol on Windows?",
     "o": ["SMB / NetBIOS", "PPTP", "SOCKS", "RPC over HTTPS"],
     "a": 0, "exp": "EternalBlue exploits a buffer overflow in the SMB/NetBIOS session service. It was used by WannaCry and NotPetya to achieve remote code execution."},

    {"c": 5, "q": "Exploiting RPC services can enable an attacker to achieve what outcome?",
     "o": ["Remote Code Execution on the target system", "Physical destruction of network hardware", "Interception of radio frequency signals", "Corruption of DNS cache entries"],
     "a": 0, "exp": "Unpatched RPC implementations can allow attackers to execute arbitrary code remotely, as demonstrated by EternalBlue and other Windows RPC exploits."},

    {"c": 5, "q": "Which of the following is NOT primarily a Session layer protocol?",
     "o": ["NetBIOS", "RPC", "PPTP", "IPsec"],
     "a": 3, "exp": "NetBIOS, RPC, and PPTP are Session layer protocols. IPsec (Internet Protocol Security) operates at Layer 3 (Network layer)."},

    {"c": 5, "q": "Secure session management requires that session tokens be:",
     "o": ["Random, unpredictable, and bound to a specific authenticated session", "Short and easy to type for manual testing", "Identical for all users in the same role", "Transmitted in URL query parameters for convenience"],
     "a": 0, "exp": "Session tokens must be cryptographically random, unpredictable, and tied to one authenticated session. They should never appear in URLs."},

    # ── Layer 6: Presentation Layer (c_idx=6) ──
    {"c": 6, "q": "An SSL/TLS downgrade attack forces a connection to use what kind of protocol?",
     "o": ["An outdated version with known vulnerabilities like SSL 3.0 or TLS 1.0", "The highest available TLS version for maximum security", "No encryption at all between client and server", "UDP instead of TCP for lower latency"],
     "a": 0, "exp": "Downgrade attacks manipulate the handshake to negotiate weak protocol versions with known flaws, such as SSL 3.0 (POODLE) or TLS 1.0."},

    {"c": 6, "q": "What tool is purpose-built for SSL stripping attacks?",
     "o": ["sslstrip", "Wireshark", "Nmap", "Httpx"],
     "a": 0, "exp": "sslstrip, created by Moxie Marlinspike, intercepts HTTPS links and rewrites them to HTTP while maintaining an HTTPS connection to the real server."},

    {"c": 6, "q": "The POODLE attack targets a vulnerability in which protocol's design?",
     "o": ["SSL 3.0's block cipher padding mechanism", "TLS 1.2's handshake protocol", "TCP's sequence number generation", "HTTP's cookie handling"],
     "a": 0, "exp": "POODLE (Padding Oracle On Downgraded Legacy Encryption) exploits SSL 3.0's CBC mode padding to decrypt encrypted data byte by byte."},

    {"c": 6, "q": "Certificate Spoofing attacks rely on presenting what to the victim during an interception?",
     "o": ["A fake or self-signed TLS certificate in a MitM position", "A valid certificate from a compromised certificate authority", "A stolen private key of a legitimate certificate", "An expired certificate from the same domain"],
     "a": 0, "exp": "In an MitM attack, the attacker presents their own certificate. If the victim ignores the warning, the attacker can decrypt and re-encrypt traffic."},

    {"c": 6, "q": "Serialization exploits target vulnerabilities in how applications handle what process?",
     "o": ["Parsing and deserializing data formats like JSON, XML, or YAML", "Managing TCP connection states and handshakes", "Routing packets across network boundaries", "Encrypting data with symmetric ciphers"],
     "a": 0, "exp": "Insecure deserialization occurs when an application deserializes untrusted data, allowing attackers to craft payloads that trigger code execution during parsing."},

    # ── Layer 7: Application Layer (c_idx=7) ──
    {"c": 7, "q": "SQL Injection exploits a flaw in how an application handles what kind of input?",
     "o": ["Database queries constructed from user-supplied input", "SSL/TLS certificate validation", "Network routing table updates", "Password hashing algorithms"],
     "a": 0, "exp": "SQL injection occurs when user input is included in SQL queries without proper sanitization, allowing attackers to manipulate the query logic."},

    {"c": 7, "q": "Cross-Site Scripting (XSS) allows an attacker to do what?",
     "o": ["Execute malicious scripts in a victim's browser by injecting into web pages", "Execute SQL commands on the application backend database", "Perform ARP cache poisoning on the local network", "Decrypt HTTPS traffic between two endpoints"],
     "a": 0, "exp": "XSS injects client-side scripts into web pages viewed by others, enabling session theft, keylogging, defacement, and phishing from within the trusted site."},

    {"c": 7, "q": "Credential Stuffing exploits what common user behavior?",
     "o": ["Reusing the same password across multiple online services", "Sharing passwords with colleagues through email", "Storing passwords in browser autofill", "Using password managers with weak master passwords"],
     "a": 0, "exp": "Credential stuffing automates login attempts using username/password pairs leaked from data breaches, exploiting the fact that users often reuse passwords."},

    {"c": 7, "q": "DNS Cache Poisoning / Spoofing works by doing what?",
     "o": ["Injecting fraudulent DNS records into a resolver's cache", "Flooding a DNS server with amplified queries", "Exploiting SQL injection on DNS database servers", "Sniffing network traffic for unencrypted DNS credentials"],
     "a": 0, "exp": "DNS poisoning corrupts the resolver's cache with forged IP-to-name mappings, redirecting legitimate domain lookups to attacker-controlled IPs."},

    {"c": 7, "q": "Hydra is a tool primarily designed for what purpose?",
     "o": ["Online brute-force attacks against network authentication services", "Network packet capture and protocol analysis", "Vulnerability scanning of web applications", "Managing concurrent SSH sessions to remote servers"],
     "a": 0, "exp": "Hydra is a parallelized login cracker that supports many protocols (HTTP, SSH, FTP, SMTP, etc.) for brute-force and credential-stuffing attacks."},
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
    c.execute("DELETE FROM quiz_questions WHERE course_id = ?", (COURSE_ID,))
    c.execute("DELETE FROM courses WHERE id = ?", (COURSE_ID,))


def migrate(conn):
    c = conn.cursor()
    clear_course(c)

    c.execute(
        "INSERT OR REPLACE INTO courses (id, code, name, description, icon, course_type) VALUES (?,?,?,?,?,?)",
        (
            COURSE_ID,
            "NET-SEC",
            "ISO/OSI Layer Attacks",
            "How attackers target each of the 7 OSI layers — from physical tampering to web application exploits — structured as a TryHackMe-style walkthrough with lessons and practice quiz.",
            "📡",
            "both",
        ),
    )

    for term, definition in GLOSSARY.items():
        c.execute(
            "INSERT OR REPLACE INTO glossary (course_id, term, definition) VALUES (?,?,?)",
            (COURSE_ID, term, definition),
        )

    for ti, tut in enumerate(TUTORIALS):
        c.execute(
            "INSERT OR REPLACE INTO tutorials (id, course_id, title, short_title, c_idx, sort_order) VALUES (?,?,?,?,?,?)",
            (tut["id"], COURSE_ID, tut["title"], tut["short"], tut["c_idx"], ti),
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

    for qi, q in enumerate(QUIZ_QUESTIONS):
        c.execute(
            "INSERT INTO quiz_questions (course_id, chapter_idx, question_text, options_json, correct_idx, explanation, sort_order) VALUES (?,?,?,?,?,?,?)",
            (COURSE_ID, q["c"], q["q"], json.dumps(q["o"]), q["a"], q["exp"], qi + 1),
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
        "quiz": c.execute(
            "SELECT COUNT(*) FROM quiz_questions WHERE course_id=?", (COURSE_ID,)
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
