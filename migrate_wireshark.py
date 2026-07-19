#!/usr/bin/env python3
"""Migrate Wireshark & Network Analysis (Ch 18) into the secplus course."""

import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "progress.db"

COURSE_ID = "secplus"

GLOSSARY = {
    "Wireshark": "The world's most widely used network protocol analyzer. Captures and inspects packets in real-time or from saved PCAP files. Used extensively in network troubleshooting, forensics, and cybersecurity analysis.",
    "PCAP": "Packet Capture — a file format (.pcap, .pcapng) that stores captured network traffic. PCAP files can be analyzed offline in tools like Wireshark for forensic or troubleshooting purposes.",
    "Packet Dissection": "The process of breaking down a network packet into its constituent protocol layers (Ethernet, IP, TCP, HTTP) so each field can be examined individually. Wireshark performs automatic dissection on all captured packets.",
    "Display Filter": "A query expression in Wireshark used to show only packets matching specific criteria. Examples: http, dns, ip.addr == 192.168.1.1, tcp.port == 443. Operates on already-captured packets instead of capture-time filtering.",
    "Ethernet Frame": "The Layer 2 data unit containing source/destination MAC addresses, an EtherType field identifying the upper-layer protocol, and a Frame Check Sequence (FCS) for error detection.",
    "OSI Model": "Open Systems Interconnection model — standardizes network communication into seven layers: Physical (1), Data Link (2), Network (3), Transport (4), Session (5), Presentation (6), Application (7). Wireshark dissects packets according to this layered model.",
    "Capture Filter": "A filter applied before capture begins — packets that do not match are discarded entirely (not recorded). Uses tcpdump/pcap-filter syntax. Example: port 80.",
    "Follow Stream": "A Wireshark feature that reassembles the complete application-layer conversation between two endpoints, displaying the full data (e.g., entire HTTP request and response).",
    "File Carving": "The process of extracting files from raw data, such as reassembling an image transferred over HTTP from a PCAP file. Wireshark can export HTTP/SMB/TFTP objects.",
    "Beaconing": "A periodic communication pattern where compromised systems check in with a C2 server. Visible in Wireshark as regular, periodic traffic to the same IP at consistent intervals — a key IOC.",
    "C2 Traffic": "Command and Control traffic — communications between a compromised system and an attacker-controlled server. Often disguised as normal HTTP/HTTPS or DNS traffic.",
    "HTTP Request/Response": "The message exchange pattern of HTTP. Client sends a request (GET, POST, etc.) with headers; server responds with a status code (200 OK, 404, etc.), headers, and body.",
    "DNS Resolution": "The process of converting a domain name into an IP address via DNS queries/responses. Visible in Wireshark — essential for detecting DNS-based attacks, tunneling, or C2.",
    "ICMP": "Internet Control Message Protocol — used for diagnostic and error-reporting. Most common as Echo Request (ping) and Echo Reply (pong), plus Destination Unreachable and TTL Exceeded.",
    "Three-Way Handshake": "The process TCP uses to establish a connection: SYN, SYN-ACK, ACK. Each step visible in Wireshark with specific TCP flags. Key indicator of successful connection establishment.",
    "SYN Flood": "A denial-of-service attack that sends many TCP SYN packets without completing the three-way handshake. Visible in Wireshark as many SYN packets with no corresponding SYN-ACK responses.",
}

TUTORIALS = [
    {
        "id": "ch18",
        "title": "Ch 18 — Wireshark & Network Analysis",
        "short": "Ch 18",
        "lessons": [
            {
                "number": 1,
                "title": "Wireshark & PCAP Fundamentals",
                "intro": "Wireshark is the world's most widely used network protocol analyzer. Understanding how to capture and inspect packets is fundamental to network troubleshooting, forensics, and cybersecurity investigations.",
                "steps": [
                    {
                        "title": "What is Wireshark?",
                        "body": (
                            "<strong>{{Wireshark}}</strong> is an open-source network protocol analyzer that captures and inspects packets in real time or from saved capture files. It is one of the most important tools in a cybersecurity professional's toolkit.\n\n"
                            "<strong>What Wireshark can do:</strong>\n"
                            "<ul>\n"
                            "  <li><strong>Live capture</strong> — capture packets directly from a network interface in real time</li>\n"
                            "  <li><strong>Offline analysis</strong> — open saved capture files ({{PCAP}}/PCAPNG format) for forensic review</li>\n"
                            "  <li><strong>Deep inspection</strong> — dissect packets down to individual protocol fields (bit-level)</li>\n"
                            "  <li><strong>Filtering</strong> — isolate specific traffic using powerful {{Display Filter}} expressions</li>\n"
                            "  <li><strong>Statistics</strong> — generate protocol hierarchy charts, conversation lists, IO graphs, and endpoint statistics</li>\n"
                            "  <li><strong>Follow streams</strong> — reassemble complete TCP, UDP, or TLS conversations between endpoints</li>\n"
                            "</ul>\n\n"
                            "<strong>Why it matters for Security+:</strong>\n"
                            "<div class=\"exam-note\"><strong>Exam Tip:</strong> Wireshark skills appear across multiple Security+ domains — network attacks (Ch 12), malware IOCs (Ch 3), forensics (Ch 15), and log analysis (Ch 14). Being able to identify malicious traffic in a PCAP is a key skill for both the exam and real-world cybersecurity work.</div>"
                        ),
                    },
                    {
                        "title": "PCAP Files — The Evidence",
                        "body": (
                            "<strong>{{PCAP}} (Packet Capture)</strong> files are the standard format for storing captured network traffic. Common extensions: .pcap and .pcapng.\n\n"
                            "<strong>Where PCAP files come from:</strong>\n"
                            "<ul>\n"
                            "  <li><strong>Wireshark/TShark</strong> — direct live capture saved to file</li>\n"
                            "  <li><strong>tcpdump</strong> — command-line packet capture on Linux/macOS</li>\n"
                            "  <li><strong>Security tools</strong> — IDS/IPS, SIEM, and forensic tools export PCAPs for investigation</li>\n"
                            "  <li><strong>CTF challenges</strong> — PCAP analysis is a staple of cybersecurity competitions</li>\n"
                            "  <li><strong>Incident response</strong> — captured traffic during an active breach becomes forensic evidence</li>\n"
                            "</ul>\n\n"
                            "<strong>Chain of custody for PCAPs:</strong> Just like any forensic evidence, PCAP files must be handled with care — hash the file (SHA-256), work on a copy, document the capture time and location, and maintain strict chain of custody."
                        ),
                    },
                    {
                        "title": "Wireshark in Cybersecurity Careers",
                        "body": (
                            "<strong>Wireshark skills are used across the entire cybersecurity field:</strong>\n\n"
                            "<table>\n"
                            "  <tr><th>Role</th><th>How Wireshark is Used</th></tr>\n"
                            "  <tr><td><strong>Network Defender/SOC Analyst</strong></td><td>Investigating alerts, identifying malicious traffic patterns, analyzing beaconing C2 traffic</td></tr>\n"
                            "  <tr><td><strong>Incident Responder</strong></td><td>Opening forensic PCAPs from breached systems, tracing attacker lateral movement, extracting exfiltrated data</td></tr>\n"
                            "  <tr><td><strong>Digital Forensics Analyst</strong></td><td>Examining network captures as part of broader forensic investigations, identifying IOCs in network traffic</td></tr>\n"
                            "  <tr><td><strong>Penetration Tester</strong></td><td>Verifying exploit traffic, analyzing protocol-level behavior, capturing authentication material for offline cracking</td></tr>\n"
                            "  <tr><td><strong>Malware Analyst</strong></td><td>Running malware in a sandbox while capturing traffic, identifying C2 traffic, DNS tunneling, or data exfiltration patterns</td></tr>\n"
                            "</table>\n\n"
                            "<div class=\"highlight-box\"><strong>Bottom line:</strong> Wireshark is not just a tool — it's a mindset. Learning to think in terms of packets and protocol layers transforms how you understand network security. Every attack leaves traces in the traffic; Wireshark helps you find them.</div>"
                        ),
                    },
                ],
                "recap": [
                    "Wireshark is the standard tool for network protocol analysis — used for live capture, offline PCAP analysis, and deep packet inspection.",
                    "PCAP files are forensic evidence — maintain chain of custody, hash the file, and work on copies.",
                    "Wireshark skills apply across SOC, incident response, forensics, pen testing, and malware analysis roles.",
                ],
            },
            {
                "number": 2,
                "title": "The Wireshark Interface",
                "intro": "Wireshark's interface is organized into three panes that work together. Mastering the interface is the first step to efficient packet analysis.",
                "steps": [
                    {
                        "title": "The Three Main Panes",
                        "body": (
                            "Wireshark's main window is divided into three panes, each showing a different view of the selected packet:\n\n"
                            "<table>\n"
                            "  <tr><th>Pane</th><th>What It Shows</th></tr>\n"
                            "  <tr><td><strong>Packet List (Top)</strong></td><td>Summary of each packet — one row per packet. Columns: No., Time, Source, Destination, Protocol, Length, Info</td></tr>\n"
                            "  <tr><td><strong>Packet Details (Middle)</strong></td><td>Protocol tree of the selected packet — expandable hierarchy from Frame, Ethernet, IP, TCP, up to Application</td></tr>\n"
                            "  <tr><td><strong>Packet Bytes (Bottom)</strong></td><td>Raw hexadecimal and ASCII representation. Each byte is highlighted to match the selected protocol field</td></tr>\n"
                            "</table>\n\n"
                            "<strong>Key column information:</strong>\n"
                            "<ul>\n"
                            "  <li><strong>No.</strong> — packet number (sequential, starting at 1)</li>\n"
                            "  <li><strong>Time</strong> — time since start of capture (or absolute time, configurable)</li>\n"
                            "  <li><strong>Source/Destination</strong> — IP addresses (or MAC for local traffic)</li>\n"
                            "  <li><strong>Protocol</strong> — highest-level protocol detected (HTTP, DNS, TCP, etc.)</li>\n"
                            "  <li><strong>Length</strong> — packet size in bytes (headers + payload)</li>\n"
                            "  <li><strong>Info</strong> — human-readable summary of the packet contents</li>\n"
                            "</ul>"
                        ),
                    },
                    {
                        "title": "Color Coding & Visual Patterns",
                        "body": (
                            "Wireshark applies a default color scheme to help analysts quickly identify different traffic types:\n\n"
                            "<table>\n"
                            "  <tr><th>Color</th><th>Typically Indicates</th><th>Example</th></tr>\n"
                            "  <tr><td><strong>Light Purple</strong></td><td>TCP traffic</td><td>TCP segments, acknowledgements</td></tr>\n"
                            "  <tr><td><strong>Light Blue</strong></td><td>UDP traffic</td><td>DNS queries, DHCP, SNMP</td></tr>\n"
                            "  <tr><td><strong>Green</strong></td><td>HTTP traffic</td><td>HTTP requests and responses</td></tr>\n"
                            "  <tr><td><strong>Yellow/Brown</strong></td><td>Routing protocols</td><td>ARP, OSPF, BGP</td></tr>\n"
                            "  <tr><td><strong>Red/Pink</strong></td><td>TCP problems</td><td>TCP retransmissions, duplicate ACKs, RST packets</td></tr>\n"
                            "  <tr><td><strong>Light Green</strong></td><td>SMB traffic</td><td>Windows file sharing</td></tr>\n"
                            "</table>\n\n"
                            "<div class=\"highlight-box\"><strong>Pro tip:</strong> In a large capture, look for red/suspicious coloring first. Retransmissions, resets, and malformed packets often indicate network problems or malicious activity.</div>"
                        ),
                    },
                    {
                        "title": "Capture vs Display Filters",
                        "body": (
                            "<strong>Opening a PCAP file:</strong> File, Open (or drag-and-drop the file into Wireshark). The packet list immediately populates with all captured packets.\n\n"
                            "<strong>Starting a live capture:</strong>\n"
                            "<ol>\n"
                            "  <li>Select the correct network interface (e.g., en0 for Wi-Fi, eth0 for Ethernet)</li>\n"
                            "  <li>Click the blue shark fin icon (or Capture, Start)</li>\n"
                            "  <li>Apply a capture filter if needed (e.g., host 192.168.1.1)</li>\n"
                            "  <li>Click the red stop icon to end the capture</li>\n"
                            "  <li>Save the capture (File, Save) to a PCAP file</li>\n"
                            "</ol>\n\n"
                            "<strong>Critical distinction:</strong>\n"
                            "<ul>\n"
                            "  <li><strong>{{Capture Filter}}:</strong> Applied before capture — packets that don't match are discarded (not recorded). Uses tcpdump syntax. Example: <code>port 80</code></li>\n"
                            "  <li><strong>{{Display Filter}}:</strong> Applied after capture — all packets exist but only matching ones are shown. Uses Wireshark's own syntax. Example: <code>tcp.port == 80</code></li>\n"
                            "</ul>\n\n"
                            "<div class=\"exam-note\"><strong>Exam Tip:</strong> Know the difference! Capture filters save resources by discarding unwanted traffic at capture time. Display filters hide but don't delete — filtered-out packets remain in the file.</div>"
                        ),
                    },
                ],
                "recap": [
                    "Three panes: Packet List (summary), Packet Details (protocol tree), Packet Bytes (hex dump).",
                    "Color coding: red = TCP problems, green = HTTP, blue = UDP, purple = general TCP.",
                    "Capture filters discard (save resources); Display filters hide (all data preserved).",
                ],
            },
            {
                "number": 3,
                "title": "Packet Dissection & OSI Layers",
                "intro": "Every packet is a series of nested protocols. Wireshark automatically dissects packets from the physical layer up to the application layer, showing exactly how each layer encapsulates the next.",
                "steps": [
                    {
                        "title": "The Encapsulation Model",
                        "body": (
                            "Network packets are <strong>encapsulated</strong>: each protocol layer wraps the one above it. When you expand a packet in Wireshark's middle pane, you see this hierarchy:\n\n"
                            "<pre>\n"
                            "Frame 123: 342 bytes on wire\n"
                            "└── Ethernet II: Src MAC, Dst MAC\n"
                            "    └── Internet Protocol Version 4: Src IP, Dst IP\n"
                            "        └── Transmission Control Protocol: Src Port, Dst Port\n"
                            "            └── Hypertext Transfer Protocol\n"
                            "                └── Line-based text data (application data)\n"
                            "</pre>\n\n"
                            "Each indented line is a different protocol layer that was stripped off (at the sender) or added (at the receiver). An {{Ethernet Frame}} carries an IP packet, which carries a TCP segment, which carries application data."
                        ),
                    },
                    {
                        "title": "Mapping Wireshark to the {{OSI Model}}",
                        "body": (
                            "This is one of the most important concepts to internalize. Here is how Wireshark's dissection maps to OSI layers:\n\n"
                            "<table>\n"
                            "  <tr><th>Wireshark Layer</th><th>OSI Layer</th><th>What You See</th><th>Example</th></tr>\n"
                            "  <tr><td><strong>Frame</strong></td><td>Layer 1 — Physical</td><td>Packet metadata</td><td>Frame number, arrival time, length</td></tr>\n"
                            "  <tr><td><strong>Ethernet II</strong></td><td>Layer 2 — Data Link</td><td>MAC addresses</td><td>fe:ff:20:00:01:00 aA 00:1b:44:11:3a:b7</td></tr>\n"
                            "  <tr><td><strong>IPv4 / IPv6</strong></td><td>Layer 3 — Network</td><td>IP addresses</td><td>216.239.59.99 aA 145.254.160.237</td></tr>\n"
                            "  <tr><td><strong>TCP / UDP</strong></td><td>Layer 4 — Transport</td><td>Ports, flags, sequence numbers</td><td>Src Port 80, Dst Port 3371</td></tr>\n"
                            "  <tr><td><strong>HTTP / DNS / FTP</strong></td><td>Layer 7 — Application</td><td>Protocol commands and headers</td><td>GET /index.html HTTP/1.1</td></tr>\n"
                            "  <tr><td><strong>Application Data</strong></td><td>Layer 7 — Payload</td><td>Actual transmitted content</td><td>HTML page, image, JSON</td></tr>\n"
                            "</table>\n\n"
                            "<strong>Note:</strong> Wireshark groups OSI Layers 5 (Session) and 6 (Presentation) together with Layer 7 (Application). The Packet Details pane jumps directly from TCP to the application protocol — session and presentation functions are embedded within the application protocol itself."
                        ),
                    },
                    {
                        "title": "Reading a Packet — Step-by-Step",
                        "body": (
                            "<div class=\"example-box\"><strong>Example:</strong> An HTTP GET request from a browser to a web server.</div>\n\n"
                            "<strong>1. Frame (Layer 1):</strong>\n"
                            "<ul>\n"
                            "  <li>Arrival Time: Jul 14, 2024 14:32:17.123456 UTC</li>\n"
                            "  <li>Frame Length: 342 bytes on the wire</li>\n"
                            "</ul>\n\n"
                            "<strong>2. Ethernet II (Layer 2):</strong>\n"
                            "<ul>\n"
                            "  <li>Destination MAC: fe:ff:20:00:01:00 (the router/gateway)</li>\n"
                            "  <li>Source MAC: 00:1b:44:11:3a:b7 (the client's NIC)</li>\n"
                            "  <li>Type: 0x800 (IPv4)</li>\n"
                            "</ul>\n\n"
                            "<strong>3. Internet Protocol (Layer 3):</strong>\n"
                            "<ul>\n"
                            "  <li>Source IP: 145.254.160.237 (the client)</li>\n"
                            "  <li>Destination IP: 216.239.59.99 (the web server)</li>\n"
                            "  <li>TTL: 128 (remaining hops)</li>\n"
                            "</ul>\n\n"
                            "<strong>4. TCP (Layer 4):</strong>\n"
                            "<ul>\n"
                            "  <li>Source Port: 3371 (ephemeral)</li>\n"
                            "  <li>Destination Port: 80 (HTTP)</li>\n"
                            "  <li>Flags: PSH, ACK (push data, acknowledge)</li>\n"
                            "</ul>\n\n"
                            "<strong>5. HTTP (Layer 7):</strong>\n"
                            "<ul>\n"
                            "  <li>Request: GET /index.html HTTP/1.1</li>\n"
                            "  <li>Host: www.example.com</li>\n"
                            "  <li>User-Agent: Mozilla/5.0</li>\n"
                            "</ul>\n\n"
                            "<div class=\"exam-note\"><strong>Exam Tip:</strong> Given a scenario, identify which OSI layer a piece of information belongs to. Source/destination IP = Layer 3. MAC addresses = Layer 2. Port numbers = Layer 4. HTTP method = Layer 7. Frame metadata = Layer 1.</div>"
                        ),
                    },
                ],
                "recap": [
                    "Packet encapsulation: Frame (L1) aA Ethernet (L2) aA IP (L3) aA TCP/UDP (L4) aA Application (L7).",
                    "Frame = L1 metadata, Ethernet = L2 (MACs), IP = L3 (IPs), TCP/UDP = L4 (ports), HTTP/DNS = L7 (commands).",
                    "Wireshark groups Session/Presentation/Application into the Application layer in its protocol tree.",
                ],
            },
            {
                "number": 4,
                "title": "Protocol Analysis — TCP, DNS, HTTP, ICMP",
                "intro": "Wireshark lets you observe common protocols in action. Understanding how normal traffic looks makes it much easier to spot the abnormal.",
                "steps": [
                    {
                        "title": "TCP — The {{Three-Way Handshake}}",
                        "body": (
                            "Before any TCP-based application (HTTP, HTTPS, SSH, FTP) can exchange data, the client and server must establish a connection:\n\n"
                            "<ol>\n"
                            "  <li><strong>Packet 1:</strong> Client aA Server — [SYN] flag, Seq=0 (relative)</li>\n"
                            "  <li><strong>Packet 2:</strong> Server aA Client — [SYN, ACK] flags, Ack=1</li>\n"
                            "  <li><strong>Packet 3:</strong> Client aA Server — [ACK] flag, connection established</li>\n"
                            "</ol>\n\n"
                            "<strong>TCP flags to recognize:</strong>\n"
                            "<table>\n"
                            "  <tr><th>Flag</th><th>Meaning</th><th>Used When</th></tr>\n"
                            "  <tr><td><strong>SYN</strong></td><td>Synchronize — initiate connection</td><td>Start of handshake</td></tr>\n"
                            "  <tr><td><strong>ACK</strong></td><td>Acknowledge — confirm receipt</td><td>Almost every packet after SYN</td></tr>\n"
                            "  <tr><td><strong>FIN</strong></td><td>Finish — graceful close</td><td>End of connection</td></tr>\n"
                            "  <tr><td><strong>RST</strong></td><td>Reset — abort connection</td><td>Error, rejected connection, scan</td></tr>\n"
                            "  <tr><td><strong>PSH</strong></td><td>Push — deliver to app now</td><td>When data should not be buffered</td></tr>\n"
                            "</table>\n\n"
                            "<div class=\"exam-note\"><strong>Security+ Relevance:</strong> A {{SYN Flood}} sends many SYN packets without completing the handshake. A port scan (Nmap SYN scan) sends SYNs and looks for SYN-ACK responses. A RST means the port is closed. These patterns are common forensic tasks in Wireshark.</div>"
                        ),
                    },
                    {
                        "title": "DNS — Looking Up Names",
                        "body": (
                            "<strong>{{DNS Resolution}}</strong> converts domain names to IP addresses (UDP port 53). Every website visit generates DNS traffic.\n\n"
                            "<strong>How a DNS query looks:</strong>\n"
                            "<ul>\n"
                            "  <li><strong>Query:</strong> Standard query 0x1234 A www.example.com</li>\n"
                            "  <li><strong>Response:</strong> Standard query response 0x1234 A 93.184.216.34</li>\n"
                            "</ul>\n\n"
                            "<strong>Key fields to examine:</strong>\n"
                            "<table>\n"
                            "  <tr><th>Field</th><th>What It Tells You</th></tr>\n"
                            "  <tr><td><strong>Transaction ID</strong></td><td>Matches query to response — mismatched IDs indicate spoofed responses</td></tr>\n"
                            "  <tr><td><strong>Flags</strong></td><td>QR: 0=query, 1=response. Response code: 0=success, 3=NXDOMAIN</td></tr>\n"
                            "  <tr><td><strong>Queries</strong></td><td>The domain name being resolved</td></tr>\n"
                            "  <tr><td><strong>Answers</strong></td><td>The resolved IP address(es)</td></tr>\n"
                            "  <tr><td><strong>TTL</strong></td><td>How long the client should cache the result</td></tr>\n"
                            "</table>\n\n"
                            "<strong>Security significance:</strong> DNS tunneling (long subdomain names), DNS poisoning (wrong response IPs), DGA domains (random-looking queries), and C2 beaconing via DNS."
                        ),
                    },
                    {
                        "title": "HTTP & ICMP",
                        "body": (
                            "<strong>{{HTTP Request/Response}}:</strong>\n\n"
                            "<strong>Request:</strong>\n"
                            "<pre>GET /index.html HTTP/1.1\nHost: www.example.com\nUser-Agent: Mozilla/5.0\nAccept: text/html</pre>\n\n"
                            "<strong>Response:</strong>\n"
                            "<pre>HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: 1234\n\n&lt;html&gt;Hello World!&lt;/html&gt;</pre>\n\n"
                            "<strong>Key HTTP status codes:</strong>\n"
                            "<ul>\n"
                            "  <li><strong>200 OK</strong> — success</li>\n"
                            "  <li><strong>301/302</strong> — redirect (could indicate compromise)</li>\n"
                            "  <li><strong>403 Forbidden</strong> — access denied</li>\n"
                            "  <li><strong>404 Not Found</strong> — resource missing</li>\n"
                            "  <li><strong>500 Internal Server Error</strong> — server error (possibly from injection)</li>\n"
                            "</ul>\n\n"
                            "<strong>{{ICMP}} — Diagnostics:</strong>\n"
                            "<table>\n"
                            "  <tr><th>Type</th><th>Meaning</th><th>Security Relevance</th></tr>\n"
                            "  <tr><td>0/8</td><td>Echo Reply / Echo Request (ping)</td><td>Host discovery / reconnaissance</td></tr>\n"
                            "  <tr><td>3</td><td>Destination Unreachable</td><td>Firewall blocking (Type 3, Code 13 = prohibited)</td></tr>\n"
                            "  <tr><td>11</td><td>Time Exceeded (TTL expired)</td><td>Traceroute — also routing loops</td></tr>\n"
                            "  <tr><td>5</td><td>Redirect</td><td>Potential on-path attack</td></tr>\n"
                            "</table>\n\n"
                            "<div class=\"highlight-box\"><strong>ICMP tunneling:</strong> Attackers can tunnel data inside ICMP echo packets. Firewalls often allow ping, making this a bypass technique. Look for unusually large or frequent ICMP packets.</div>"
                        ),
                    },
                ],
                "recap": [
                    "TCP handshake: SYN, SYN-ACK, ACK. RST = port closed; SYN flood = many incomplete handshakes.",
                    "DNS maps names to IPs (UDP 53). Suspicious: tunneling, DGA domains, mismatched transaction IDs.",
                    "HTTP response codes: 200=OK, 403=Forbidden, 404=Not Found, 500=Server Error.",
                    "ICMP: ping for discovery, Destination Unreachable for firewall blocking, Redirect for on-path attacks.",
                ],
            },
            {
                "number": 5,
                "title": "Filtering Traffic Like a Pro",
                "intro": "The power of Wireshark isn't in capturing packets — it's in finding the right packets among thousands. Display filters are your most important tool for efficient analysis.",
                "steps": [
                    {
                        "title": "Display Filter Syntax",
                        "body": (
                            "Wireshark's {{Display Filter}} language lets you build precise expressions to isolate traffic.\n\n"
                            "<strong>Comparison operators:</strong>\n"
                            "<table>\n"
                            "  <tr><th>Operator</th><th>Meaning</th><th>Example</th></tr>\n"
                            "  <tr><td><code>==</code></td><td>Equal to</td><td><code>ip.src == 192.168.1.1</code></td></tr>\n"
                            "  <tr><td><code>!=</code></td><td>Not equal to</td><td><code>ip.src != 192.168.1.1</code></td></tr>\n"
                            "  <tr><td><code>contains</code></td><td>Substring match</td><td><code>http.request.uri contains \"login\"</code></td></tr>\n"
                            "</table>\n\n"
                            "<strong>Logical operators:</strong>\n"
                            "<ul>\n"
                            "  <li><code>and</code> / <code>&&</code> — both conditions must be true</li>\n"
                            "  <li><code>or</code> / <code>||</code> — either condition can be true</li>\n"
                            "  <li><code>not</code> / <code>!</code> — negate the condition</li>\n"
                            "</ul>"
                        ),
                    },
                    {
                        "title": "Essential Display Filters Cheat Sheet",
                        "body": (
                            "<strong>By Address:</strong>\n"
                            "<ul>\n"
                            "  <li><code>ip.addr == 192.168.1.1</code> — all traffic to/from that IP</li>\n"
                            "  <li><code>ip.src == 10.0.0.1</code> — traffic from that source only</li>\n"
                            "  <li><code>eth.addr == 00:1b:44:11:3a:b7</code> — traffic by MAC address</li>\n"
                            "</ul>\n\n"
                            "<strong>By Protocol:</strong>\n"
                            "<ul>\n"
                            "  <li><code>http</code>, <code>dns</code>, <code>icmp</code>, <code>arp</code>, <code>tcp</code>, <code>udp</code> — all traffic for that protocol</li>\n"
                            "  <li><code>tls</code> or <code>ssl</code> — encrypted HTTPS traffic</li>\n"
                            "</ul>\n\n"
                            "<strong>By Port:</strong>\n"
                            "<ul>\n"
                            "  <li><code>tcp.port == 80</code> — TCP traffic on port 80</li>\n"
                            "  <li><code>tcp.dstport == 22</code> — traffic to SSH server</li>\n"
                            "</ul>\n\n"
                            "<strong>Combined Patterns:</strong>\n"
                            "<ul>\n"
                            "  <li><code>http and ip.src == 192.168.1.100</code> — HTTP from a specific host</li>\n"
                            "  <li><code>!(arp or icmp or dns)</code> — exclude noise, show interesting traffic</li>\n"
                            "  <li><code>http.response.code >= 400</code> — client/server errors only</li>\n"
                            "</ul>\n\n"
                            "<div class=\"exam-note\"><strong>Exam Tip:</strong> Security+ expects you to identify the correct filter for a scenario. \"Which filter shows only HTTP traffic?\" aA <code>http</code>. \"Traffic to/from an IP?\" aA <code>ip.addr == 10.0.0.1</code>.</div>"
                        ),
                    },
                    {
                        "title": "Following Streams & Exporting Objects",
                        "body": (
                            "<strong>{{Follow Stream}}</strong> reassembles the complete application-layer conversation between two endpoints.\n\n"
                            "<strong>How to follow a stream:</strong>\n"
                            "<ol>\n"
                            "  <li>Right-click any packet in the conversation</li>\n"
                            "  <li>Select Follow, TCP Stream (or UDP/TLS Stream)</li>\n"
                            "  <li>A window shows the complete conversation — client data in red, server in blue</li>\n"
                            "</ol>\n\n"
                            "<strong>What you can see:</strong>\n"
                            "<ul>\n"
                            "  <li>Full HTTP request/response (headers and body)</li>\n"
                            "  <li>Passwords sent in plaintext (FTP, HTTP Basic Auth, Telnet)</li>\n"
                            "  <li>File contents transferred over the stream</li>\n"
                            "  <li>Malicious payloads sent by an attacker</li>\n"
                            "</ul>\n\n"
                            "<strong>Exporting objects:</strong> File, Export Objects, HTTP — extract images, documents, ZIPs, etc. transferred over HTTP. Also supports SMB and TFTP.\n\n"
                            "<div class=\"highlight-box\"><strong>Forensic use:</strong> If an attacker exfiltrated a file via HTTP POST, you can extract it directly from the PCAP using Export Objects. This is why encryption (HTTPS/TLS) is critical for protecting data in transit.</div>"
                        ),
                    },
                ],
                "recap": [
                    "Display filters use protocol.field: ip.addr, tcp.port, http, dns — combined with and/or/not.",
                    "Essential patterns: ip.addr == X, tcp.port == 80, http, dns, !(arp or icmp).",
                    "Follow Stream reassembles full conversations; Export Objects extracts transferred files.",
                ],
            },
            {
                "number": 6,
                "title": "Wireshark in Security+ & Forensics",
                "intro": "Wireshark skills directly support Security+ exam domains and real-world cybersecurity investigations. This card ties everything together with practical scenarios.",
                "steps": [
                    {
                        "title": "Detecting Network Scans in Wireshark",
                        "body": (
                            "<strong>Port Scan (Nmap SYN scan):</strong>\n"
                            "<ul>\n"
                            "  <li>Many SYN packets from one IP to different ports on the same target</li>\n"
                            "  <li>SYN-ACK = open port, RST = closed, no response = filtered</li>\n"
                            "  <li><strong>Filter:</strong> <code>tcp.flags.syn == 1 and tcp.flags.ack == 0</code></li>\n"
                            "</ul>\n\n"
                            "<strong>Ping Sweep (ICMP scan):</strong>\n"
                            "<ul>\n"
                            "  <li>ICMP Echo Requests to many IPs in sequence</li>\n"
                            "  <li>Replies indicate live hosts</li>\n"
                            "  <li><strong>Filter:</strong> <code>icmp.type == 8</code></li>\n"
                            "</ul>\n\n"
                            "<strong>ARP Spoofing:</strong>\n"
                            "<ul>\n"
                            "  <li>Multiple ARP replies from one MAC claiming different IPs</li>\n"
                            "  <li>Gratuitous ARP replies without corresponding requests</li>\n"
                            "  <li><strong>Filter:</strong> <code>arp.opcode == 2</code></li>\n"
                            "</ul>"
                        ),
                    },
                    {
                        "title": "Malware Traffic Patterns — {{Beaconing}} & {{C2 Traffic}}",
                        "body": (
                            "Identifying compromised hosts in network traffic is a core SOC skill:\n\n"
                            "<strong>Beaconing (Periodic Callbacks):</strong>\n"
                            "<ul>\n"
                            "  <li>Consistent time intervals between connections (e.g., exactly every 60s)</li>\n"
                            "  <li>Small, similar-sized packets each time</li>\n"
                            "  <li>Unusual destination IP, possibly in a different country</li>\n"
                            "  <li><strong>Detection:</strong> IO Graph (Statistics, IO Graph) shows regular spikes</li>\n"
                            "</ul>\n\n"
                            "<strong>DNS Tunneling:</strong>\n"
                            "<ul>\n"
                            "  <li>Excessive DNS queries to the same domain from one host</li>\n"
                            "  <li>Unusually long subdomain names (encoded data)</li>\n"
                            "  <li><strong>Filter:</strong> <code>dns.qry.name.len &gt; 40</code></li>\n"
                            "</ul>\n\n"
                            "<strong>Data Exfiltration:</strong>\n"
                            "<ul>\n"
                            "  <li>Large amounts of data leaving to an external destination</li>\n"
                            "  <li>Unusual outbound connections (workstation using SSH)</li>\n"
                            "  <li><strong>Filter:</strong> <code>ip.dst != 192.168.0.0/16 and frame.len &gt; 1000</code></li>\n"
                            "</ul>\n\n"
                            "<div class=\"highlight-box\"><strong>IR workflow:</strong> 1) Find all traffic from suspicious host IP. 2) Look for unusual destinations/ports. 3) Check for periodic patterns (beaconing). 4) Follow streams. 5) Export transferred files. 6) Create IOCs from C2 IPs/domains.</div>"
                        ),
                    },
                    {
                        "title": "Wireshark & Order of Volatility",
                        "body": (
                            "In forensics, capture volatile evidence before it disappears:\n\n"
                            "<table>\n"
                            "  <tr><th>Priority</th><th>Evidence</th><th>Volatility</th><th>Wireshark Role</th></tr>\n"
                            "  <tr><td>1</td><td>CPU registers, cache</td><td>Nanoseconds</td><td>N/A</td></tr>\n"
                            "  <tr><td>2</td><td>RAM / Memory</td><td>Seconds</td><td>Live connections visible in memory</td></tr>\n"
                            "  <tr><td>3</td><td>Network connections</td><td>Seconds to minutes</td><td><strong>Capture live traffic NOW</strong></td></tr>\n"
                            "  <tr><td>4</td><td>Running processes</td><td>Minutes</td><td>Cross-reference with Wireshark</td></tr>\n"
                            "  <tr><td>5</td><td>Disk storage</td><td>Hours to years</td><td>Saved PCAPs analyzed here</td></tr>\n"
                            "  <tr><td>6</td><td>Backups / Archives</td><td>Years</td><td>Historical PCAP archives</td></tr>\n"
                            "</table>\n\n"
                            "<strong>During incident response:</strong>\n"
                            "<ol>\n"
                            "  <li>Start a capture immediately on the suspected host or at the network chokepoint</li>\n"
                            "  <li>Save the capture with a forensically sound filename (hostname-date-time.pcap)</li>\n"
                            "  <li>Document the capture interface, time, and reason</li>\n"
                            "  <li>Preserve the PCAP — compute SHA-256 hash, store on write-protected media</li>\n"
                            "  <li>Analyze offline — work from a copy, never the original</li>\n"
                            "</ol>\n\n"
                            "<strong>{{File Carving}} from PCAPs:</strong> Beyond Export Objects, tools like Foremost, Binwalk, and NetworkMiner recover files from captures by header/footer signatures.\n\n"
                            "<div class=\"exam-note\"><strong>Exam Tip:</strong> Network connections are Priority 3 in order of volatility — capture them immediately after memory, before processes or disk.</div>"
                        ),
                    },
                ],
                "recap": [
                    "Scan detection: many SYNs to different ports (port scan), many ICMP requests (ping sweep), duplicate ARP replies (spoofing).",
                    "Malware traffic: beaconing (periodic callbacks), DNS tunneling (long queries), data exfiltration (large outbound data).",
                    "Order of volatility: CPU aA RAM aA Network (capture NOW!) aA Processes aA Disk aA Backups.",
                    "Forensic workflow: capture aA save aA hash aA copy aA analyze. Never work on the original PCAP.",
                ],
            },
        ],
    },
]

QUIZ_QUESTIONS = [
    {
        "chapter_idx": 17,
        "question": "Which Wireshark pane shows the protocol hierarchy of a selected packet?",
        "options": ["Packet List pane", "Packet Details pane", "Packet Bytes pane", "Protocol Statistics pane"],
        "correct": 1,
        "explanation": "The Packet Details (middle) pane shows the expandable protocol tree — from Frame through Ethernet, IP, TCP, up to the application layer. The Packet List pane shows summaries; the Packet Bytes pane shows raw hex.",
        "card_ref": 2,
    },
    {
        "chapter_idx": 17,
        "question": "Which Wireshark display filter shows all HTTP traffic from a specific source IP?",
        "options": ["ip.src == 192.168.1.1 and http", "http and ip.dst == 192.168.1.1", "ip.addr == 192.168.1.1", "tcp.port == 80 and ip.src == 192.168.1.1"],
        "correct": 0,
        "explanation": "The correct filter combines the protocol filter 'http' with a source IP condition using 'ip.src == 192.168.1.1'. This shows only HTTP packets originating from that IP.",
        "card_ref": 5,
    },
    {
        "chapter_idx": 17,
        "question": "What is the key difference between a capture filter and a display filter in Wireshark?",
        "options": ["Capture filters are faster than display filters", "Capture filters discard non-matching packets entirely; display filters only hide them", "Capture filters use Wireshark syntax; display filters use tcpdump syntax", "There is no functional difference"],
        "correct": 1,
        "explanation": "Capture filters discard packets at capture time (saving resources), while display filters only hide non-matching packets from view — all data remains in the file and can be revealed by changing the filter.",
        "card_ref": 2,
    },
    {
        "chapter_idx": 17,
        "question": "In Wireshark, which OSI layer do MAC addresses belong to?",
        "options": ["Layer 1 — Physical", "Layer 2 — Data Link", "Layer 3 — Network", "Layer 4 — Transport"],
        "correct": 1,
        "explanation": "MAC addresses are Layer 2 (Data Link) identifiers. They are used for local network segment communication. IP addresses belong to Layer 3 (Network), and port numbers belong to Layer 4 (Transport).",
        "card_ref": 3,
    },
    {
        "chapter_idx": 17,
        "question": "Which TCP flag indicates that a connection is being gracefully closed?",
        "options": ["SYN", "ACK", "FIN", "RST"],
        "correct": 2,
        "explanation": "The FIN (Finish) flag indicates a graceful connection close. RST (Reset) abruptly aborts a connection. SYN initiates a connection, and ACK acknowledges received data.",
        "card_ref": 4,
    },
    {
        "chapter_idx": 17,
        "question": "An analyst sees periodic traffic from a workstation to the same external IP every 60 seconds with small, consistent packet sizes. What pattern is this?",
        "options": ["DNS tunneling", "Beaconing (C2 callback)", "Normal web browsing", "ARP spoofing"],
        "correct": 1,
        "explanation": "Beaconing is characterized by regular, periodic traffic to the same destination with consistent packet sizes — this is a common indicator of malware checking in with a Command and Control (C2) server.",
        "card_ref": 6,
    },
    {
        "chapter_idx": 17,
        "question": "Where do port numbers appear in a Wireshark packet dissection?",
        "options": ["Ethernet II section", "Internet Protocol section", "Transmission Control Protocol section", "Frame section"],
        "correct": 2,
        "explanation": "Port numbers appear in the TCP (or UDP) section of the packet details. Source and destination ports identify the communicating applications. Ethernet handles MAC addresses, and IP handles logical addressing.",
        "card_ref": 3,
    },
    {
        "chapter_idx": 17,
        "question": "In the order of volatility, when should network traffic be captured during incident response?",
        "options": ["First — before anything else", "Second — after memory/CPU", "Third — after memory, before processes", "Last — after disk and backups"],
        "correct": 2,
        "explanation": "Network connections are Priority 3 in the order of volatility. Capture memory (Priority 2) first, then capture live network traffic immediately (Priority 3), before processes (Priority 4) or disk (Priority 5).",
        "card_ref": 6,
    },
]


def clear(c):
    c.execute(
        "DELETE FROM lesson_recaps WHERE lesson_id IN (SELECT l.id FROM lessons l JOIN tutorials t ON l.tutorial_id = t.id WHERE t.course_id = ? AND t.id = 'ch18')",
        (COURSE_ID,),
    )
    c.execute(
        "DELETE FROM lesson_steps WHERE lesson_id IN (SELECT l.id FROM lessons l JOIN tutorials t ON l.tutorial_id = t.id WHERE t.course_id = ? AND t.id = 'ch18')",
        (COURSE_ID,),
    )
    c.execute(
        "DELETE FROM lessons WHERE tutorial_id IN (SELECT id FROM tutorials WHERE course_id = ? AND id = 'ch18')",
        (COURSE_ID,),
    )
    c.execute("DELETE FROM tutorials WHERE course_id = ? AND id = 'ch18'", (COURSE_ID,))
    c.execute(
        "DELETE FROM glossary WHERE course_id = ? AND term IN ({})".format(
            ",".join("?" for _ in GLOSSARY)
        ),
        (COURSE_ID, *GLOSSARY.keys()),
    )
    c.execute(
        "DELETE FROM quiz_questions WHERE course_id = ? AND chapter_idx = 17",
        (COURSE_ID,),
    )


def migrate(conn):
    c = conn.cursor()
    clear(c)

    for term, definition in GLOSSARY.items():
        c.execute(
            "INSERT OR REPLACE INTO glossary (course_id, term, definition) VALUES (?,?,?)",
            (COURSE_ID, term, definition),
        )

    for ti, tut in enumerate(TUTORIALS):
        sort_order = 17
        c.execute(
            "INSERT OR REPLACE INTO tutorials (id, course_id, title, short_title, c_idx, sort_order) VALUES (?,?,?,?,?,?)",
            (tut["id"], COURSE_ID, tut["title"], tut["short"], 17, sort_order),
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
                    (lesson_id, st["title"], st["body"].strip(), None, si),
                )
            for ri, text in enumerate(les["recap"]):
                c.execute(
                    "INSERT INTO lesson_recaps (lesson_id, text, sort_order) VALUES (?,?,?)",
                    (lesson_id, text, ri),
                )

    # Get the last sort_order for existing quiz questions of secplus
    last_order = c.execute(
        "SELECT COALESCE(MAX(sort_order), 0) FROM quiz_questions WHERE course_id = ?",
        (COURSE_ID,),
    ).fetchone()[0]
    for qi, qq in enumerate(QUIZ_QUESTIONS):
        c.execute(
            "INSERT INTO quiz_questions (course_id, chapter_idx, question_text, options_json, correct_idx, explanation, card_ref, sort_order) VALUES (?,?,?,?,?,?,?,?)",
            (
                COURSE_ID,
                qq["chapter_idx"],
                qq["question"],
                json.dumps(qq["options"]),
                qq["correct"],
                qq["explanation"],
                qq.get("card_ref"),
                last_order + qi + 1,
            ),
        )

    conn.commit()

    counts = {
        "tutorials": c.execute(
            "SELECT COUNT(*) FROM tutorials WHERE course_id=?", (COURSE_ID,)
        ).fetchone()[0],
        "glossary": c.execute(
            "SELECT COUNT(*) FROM glossary WHERE course_id=?", (COURSE_ID,)
        ).fetchone()[0],
        "quiz": c.execute(
            "SELECT COUNT(*) FROM quiz_questions WHERE course_id=? AND chapter_idx=17",
            (COURSE_ID,),
        ).fetchone()[0],
    }
    print(f"Migrated Wireshark Ch18 into {COURSE_ID}: {counts}")
    return counts


if __name__ == "__main__":
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    migrate(conn)
    conn.close()
    print("Migration complete")
