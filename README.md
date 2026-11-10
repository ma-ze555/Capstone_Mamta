# LoadIQ: Priority-Driven Delivery Load Optimisation Engine

**Capstone project CP-048** | Domain: Travel, Transport and Logistics
**Author:** Mamta Kumari Jaiswal (ISE, Atria Institute of Technology)

## Problem
A logistics hub loads vans by hand. High-priority parcels are often left behind while vans leave half-full.

## Solution
A Python console app that assigns parcels to vans automatically. Highest-priority parcels are loaded first, and no van ever exceeds its weight or volume capacity.

## Features
- Record parcels (ID, weight, volume, priority)
- Record vans (ID, weight capacity, volume capacity)
- Assign parcels to vans, highest priority first, within capacity
- List parcels that could not be loaded, with the reason
- Print a load sheet per van with total weight and volume used (and % utilisation)
- Input validation: rejects text, zero or negative values, bad priorities and duplicate IDs
- Sample data option for quick demos

## How it works
1. Sort parcels by priority (1 = High, 2 = Medium, 3 = Low). Within the same priority, heavier parcels go first.
2. For each parcel, place it in the first van that has enough weight AND volume left.
3. If no van fits, the parcel goes to the "not loaded" list with a reason.

This is a **greedy heuristic**. It is fast and easy to explain, but it does not always find the perfect arrangement (a knapsack-style problem).

## Run it
Requires Python 3.8+. No external libraries.

```
python loadiq.py
```

Quick demo: choose `7` (load sample data), then `4` (assign), `5` (load sheet), `6` (not loaded).

## Sample output
```
Van VAN-A
  P3    60.0 kg  0.80 m3  High
  P1    40.0 kg  0.50 m3  High
  P4    90.0 kg  1.00 m3  Medium
  Weight used: 190.0 / 200.0 kg (95%)

Parcels NOT loaded
  P5   Medium -> Heavier than the biggest van
```

## Limitations
- Greedy result is not always optimal
- Data is stored in memory only (lost on exit)

## Future work
- Compare priority-first plan with a value-per-weight plan
- Balance load evenly across vans
- Save and load data from a file
- GUI version
