# BCL1123 Internet of Things — Test Answers

**Student Name:** Chan Jing Yi  
**Student ID:** SUOL2500321  
**Semester:** May–August 2026

## Section A: Multiple-Choice Questions

| Question | Answer | Question | Answer |
|---:|:---:|---:|:---:|
| 1 | B | 6 | C |
| 2 | D | 7 | A |
| 3 | B | 8 | B |
| 4 | C | 9 | C |
| 5 | B | 10 | B |

## Section B: Structured Questions

### Question 11(a)

The M2M era centred on direct, task-specific communication between a small number of machines. A sensor or controller normally sent telemetry to another machine through a proprietary wired link, cellular modem, or closed supervisory system. Human involvement was limited, data often remained inside an organisational silo, and adding a new vendor’s device usually required a custom gateway. M2M therefore prioritised reliable point-to-point automation rather than broad service integration.

The modern IoT ecosystem connects physical and virtual things through Internet Protocol networks, cloud or edge platforms, application programming interfaces, and user-facing applications. A single device’s data can be stored, analysed, combined with other sources, and used by several services. IoT also supports many-to-many communication, remote device management, scalable analytics, and human interaction through dashboards or mobile alerts. This openness creates more value than isolated M2M telemetry, although it also introduces wider cybersecurity, privacy, governance, and interoperability responsibilities.

### Question 11(b)

The Middleware or Processing Layer sits between device connectivity and business applications. Devices made by different manufacturers may transmit different payload formats and use protocols such as MQTT, HTTP, or CoAP. Middleware hides that heterogeneity through protocol adapters, gateways, device registries, and common application programming interfaces. It identifies each device, translates messages into a shared data model, validates units and timestamps, and exposes normalised information to applications. A dashboard can therefore consume one consistent temperature field even when the original sensors encode that reading differently.

The layer also performs message brokering, event processing, data filtering, aggregation, storage, and rule execution. For example, it can convert Fahrenheit to Celsius, reject an impossible reading, combine several sensor values, and publish a standard alarm event. Semantic metadata clarifies what a value represents, while service discovery enables authorised applications to find the appropriate device capability without depending on its manufacturer’s implementation.

Interoperability still requires governance. Middleware should enforce standard schemas and APIs, maintain version compatibility, authenticate devices, authorise access, encrypt data in transit, and record audit logs. It does not automatically correct a poorly documented proprietary protocol; an adapter or vendor-supported standard is still required. With those controls, applications remain decoupled from hardware brands and devices can be replaced or expanded without redesigning the complete IoT service.

### Question 12(a)

The first critical component is a calibrated multi-sensor data logger placed with the biological samples. A digital temperature probe provides a continuous, time-stamped record, while a humidity sensor and door-open or shock sensor can reveal condensation, handling, or package breaches. The logger needs local memory and a backup battery so that evidence is retained during aircraft loading, customs inspection, or a temporary loss of network coverage. Calibration records and device identity link every reading to the correct shipment.

The second component is a secure communications and location unit, consisting of a low-power controller, GNSS positioning, and cellular or LPWAN connectivity. It periodically sends the sensor readings, location, battery state, and shipment identifier to an IoT platform. Edge rules should trigger an audible or visual local warning when a safe threshold is crossed, while the platform alerts the control centre. Buffered store-and-forward transmission prevents a coverage gap from becoming a gap in the compliance record.

### Question 12(b)

Real-time analytics converts the sensor stream into operational decisions. The platform compares each reading with the product-specific temperature and humidity limits, checks the duration of an excursion, and combines the result with location, route, weather, and estimated arrival time. A predictive rule can warn staff before the sample becomes unusable—for example, by detecting a rising temperature trend rather than waiting for a fixed limit to be exceeded. The control centre can then instruct a driver to inspect the container, increase cooling, move the shipment to qualified storage, or reroute it to a nearer approved facility.

That early intervention reduces waste because the firm does not automatically discard every shipment after a minor event. A complete time–temperature history supports a risk-based decision on whether the biological sample remained within its validated stability envelope. Analytics can also compare lanes, carriers, containers, and packaging designs to identify repeated delays or thermal weak points. Maintenance can then be scheduled before a refrigeration unit fails, and inefficient routes or excessive refrigerant use can be corrected.

Compliance improves when the platform preserves calibrated, time-stamped, tamper-evident records and applies the correct rules for each product and destination. Automated exception reports, chain-of-custody logs, acknowledgement records, and audit trails give regulators and customers consistent evidence. Role-based access and encryption protect sensitive shipment data. Sensor calibration drift, false alarms, and missing connectivity remain risks, so the firm should use calibration schedules, redundant critical sensors, local buffering, and human review before releasing or rejecting a shipment.

### Question 13(a)

> **Student action required:** Insert a real selfie showing Chan Jing Yi seated or standing in the outdoor café seating area. The student, café table, and preferably the awning or nearby fan must be clearly visible so the selected environment matches the answers below.

### Question 13(b)

The first sensor would be a digital temperature-and-humidity sensor such as the SHT31, installed in a shaded and ventilated position within the outdoor café seating area. It is appropriate because customer comfort depends on both air temperature and relative humidity; placing it away from direct sunlight and cooking exhaust produces a more representative reading. Unlike a simple thermostat, the combined measurements allow the controller to estimate when the seating area feels hot and humid rather than reacting to temperature alone.

The second sensor would be a rain sensor mounted on the exposed edge of the café roof or awning. It is appropriate because an outdoor seating area needs an immediate indication of rainfall before tables, customers, food, or electrical equipment become wet. The sensing surface should be angled so water can drain, and the software should require several consistent readings to reduce false triggers caused by splashes or cleaning water.

### Question 13(c)

The controller would compare temperature and humidity with the café’s comfort thresholds. When conditions become hot and humid, it would switch on or increase the speed of the outdoor fan through a safe relay or smart controller. When the rain sensor confirms rainfall, the system would extend a motorised awning, notify café staff, and protect the outdoor tables. The awning should not retract until the sensor has remained dry for a set period, preventing repeated movement during intermittent rain. Manual controls and wind-safety protection must override the automation.

The platform would store time-stamped temperature, humidity, rain state, fan speed, and awning position. Café staff could review the data to identify uncomfortable periods, adjust seating arrangements, and maintain the fan or awning before failure. Customers receive a safer and more comfortable outdoor space, while the café avoids running the fan continuously and can respond to rain quickly without relying on a staff member noticing it first.

### Question 14(a)

The selected city is **Kota Bharu, Kelantan, Malaysia**. Low-lying neighbourhoods, roads, and drains near Sungai Kelantan can become unsafe during intense rainfall and the monsoon when river and drain levels rise. Floodwater disrupts travel and may leave residents or drivers entering an affected area before a warning reaches them. The Department of Irrigation and Drainage already monitors Kota Bharu stations such as Sungai Kelantan at Tambatan D’Raja, so additional local sensor nodes could increase coverage between existing stations.

An IoT network could place non-contact ultrasonic water-level sensors above critical drains and flood-prone roads, supported by tipping-bucket rain gauges at nearby locations. Each node would report water depth, rate of rise, rainfall intensity, battery condition, and location. Combining several nearby readings would give JPS Kelantan and the local authority earlier and more reliable evidence than a single visual report, allowing targeted warnings, drain inspections, road closures, evacuation preparation, and siren activation.

### Question 14(b)

LoRaWAN is a low-power wide-area technology designed for small, infrequent sensor messages. A gateway can cover a broad urban area, although buildings, terrain, antenna height, and interference reduce the practical range. Battery nodes can sleep for most of the time and wake briefly to transmit a water-level packet, supporting long service life. Its limitations are low data rate, duty-cycle constraints, and less predictable latency, so it is unsuitable for continuous high-resolution video.

5G uses licensed cellular infrastructure and provides higher capacity, mobility support, and lower-latency service classes. Coverage depends on the operator and radio band: lower-frequency cells cover wider areas, while high-frequency cells provide capacity over shorter distances. A 5G modem normally consumes more energy than a sleeping LoRaWAN node because it performs more complex radio processing and network signalling, although 5G is preferable when a site needs video, frequent large uploads, or rapid closed-loop control.

LoRaWAN is the more practical primary link for Kota Bharu’s distributed river, drain, and low-lying-road sensors because each node sends only a few bytes, many locations lack convenient mains power, and battery replacement beside waterways creates cost and safety problems. Gateways can be mounted at JPS or local-authority facilities and forward data through fibre or cellular backhaul. Critical sites should use acknowledged alarms, repeated transmissions, local sirens, and a cellular fallback because no single wireless link should be the only flood-safety control.

### Question 14(c)

> **Student action required:** Hand-draw this path on physical paper: **Water-level sensor + rain gauge near Sungai Kelantan and flood-prone drains (Physical/Perception Layer) → LoRaWAN node and gateway (Network Layer) → IoT platform, database, threshold and rising-water analysis (Middleware/Processing Layer) → JPS Kelantan/local-authority dashboard, public mobile alert, road warning sign and local siren (Application Layer).** Write **SUOL2500321** and your signature in a corner, then photograph the full sheet clearly and insert it into the answer script.

## Selected Technical Sources

- 3rd Generation Partnership Project. (2023). *Ultra reliable and low latency communications*. https://www.3gpp.org/technologies/urlcc-2022
- Department of Irrigation and Drainage Malaysia. (2026). *River water-level data: Kelantan*. https://publicinfobanjir.water.gov.my/aras-air/data-paras-air/?lang=en&state=KEL
- International Telecommunication Union. (2012). *Recommendation ITU-T Y.4000/Y.2060: Overview of the Internet of things*. https://www.itu.int/itu-t/recommendations/rec.aspx?rec=Y.2060
- LoRa Alliance. (n.d.). *What is LoRaWAN?* https://lora-alliance.org/resource_hub/what-is-lorawan/
- World Health Organization. (2026). *Cold chain equipment and dry store temperature mapping tool*. https://www.who.int/publications/m/item/cold-chain-equipment-and-dry-store-temperature-mapping-tool
