# MLH project submission draft

**Project name:** RoboGuard

**Tagline:** Robot health, made legible.

**Short description:** RoboGuard is an AI-powered robotics diagnostic dashboard that turns robot sensor telemetry into understandable maintenance guidance. It visualizes motor temperature, vibration, battery voltage, and wheel encoder drift, flags unusual readings, and uses a locally run open-weight model to explain related signals and suggest a safe next inspection.

**Problem:** Robot operators often have raw telemetry but no quick way to spot a developing issue or connect symptoms across sensors. A rising motor temperature plus uneven wheel speeds may indicate mechanical drag before the robot stops.

**What the AI does:** RoboGuard sends a structured sensor snapshot and recent trend to Gemma 3 1B through Ollama on the user's machine. The model produces a concise, uncertainty-aware hypothesis and inspection suggestion. The demo also labels threshold-based alerts transparently, without presenting them as AI predictions.

**How to run:** Install Python 3.9+ and Ollama, run `ollama pull gemma3:1b`, start `python server.py`, then open `http://localhost:8000`.

**Technology:** Vanilla JavaScript, HTML/CSS, Python standard library, Ollama, Gemma 3 1B.

**Repository:** Add the public GitHub repository URL after publishing.

**Demo:** Run locally using the instructions above. The demo uses simulated rover telemetry and is not connected to a physical robot.
