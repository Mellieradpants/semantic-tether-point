Running the Prototype

This repository includes a minimal demonstration of the Semantic Tether Point concept.

The prototype script shows how anchored interpretation can be generated from defined tether points.


Requirements

Python 3.x


Run the Prototype

From the repository root directory run:

python prototype/tether_extractor.py


Expected Result

The script will produce structured output showing:

anchor
observation
operationalMeaning


Example Flow

document
→ anchor reference
→ interpretation
→ structured tethered output


Purpose

This prototype demonstrates the core rule of the system:

Interpretation must remain connected to a tether point.

If interpretation becomes detached from its source, analysis must return to the last verified tether point.
