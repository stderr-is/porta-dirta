---
type: architecture
status: active
tags: [strategy, beds24, data-flow]
---

# 🧠 Master Architecture & Parameters — Porta D'irta

## The "Single Source of Truth"
**Beds24** is the absolute master database for guest identity and dates. 
* **TastyIgniter** (Restaurant) and **Hi.Events** (Collabs/Ticketing) are downstream dependents. 
* Data flows strictly in **one direction**: from the room reservation to the experience upsell. Never the reverse.

## The Critical Path
1. Beds24 Booking.com API Authorization
2. Cloudify/Railway Docker Deployment
3. Astro Frontend Integration

> [!warning] The Booking.com Bottleneck
> If Booking.com delays the XML connection approval by one day, the entire public launch is delayed by one day. We **cannot** launch the site manually without OTA sync protection.
