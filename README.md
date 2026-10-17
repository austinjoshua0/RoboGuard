# RoboGuard

**Robot health, made legible.** RoboGuard is an open-source robotics diagnostic dashboard that helps an engineer spot unusual telemetry and turn it into a practical next inspection. The demo follows a warehouse rover with a heating left wheel motor and an encoder mismatch.

**Live demo:** <https://austinjoshua0.github.io/RoboGuard/>. It runs the simulated dashboard in your browser. Open-weight AI explanations use the optional local Ollama setup below.

## Why this exists

A robot can keep moving while a motor overheats or its wheels stop behaving alike. Those signals are easy to miss in raw logs. RoboGuard puts the live readings, trend lines, alerts, and a plain-language diagnostic in one place.

## What it does

- Streams realistic simulated motor temperature, chassis vibration, battery voltage, and wheel-speed-delta readings.
- Visualizes recent trends and highlights elevated temperature and wheel encoder drift.
- Asks a locally running open-weight model to explain correlated telemetry, state uncertainty, and suggest a safe inspection.
- Exports a JSON diagnostic snapshot and a CSV event log.
- Runs locally. Telemetry stays in the browser; the optional model request goes to your local Ollama service.

## Run the dashboard

Requires Python 3.9+ and a modern browser. No Python packages are needed.

```bash
python server.py
```

Open <http://localhost:8000>. The telemetry simulator and heuristic guidance work without an AI model. To enable generated explanations, install [Ollama](https://ollama.com/) and pull a small open-weight model:

```bash
ollama pull gemma3:1b
```

Then start Ollama and click **Ask AI to diagnose**. RoboGuard sends the latest readings to Ollama's local `/api/chat` endpoint; model output is an advisory explanation, not an autonomous control command. Choose another Ollama model with `OLLAMA_MODEL` (for example `qwen3:4b`) and a custom local endpoint with `OLLAMA_URL` before starting the server.

```bash
# macOS / Linux
OLLAMA_MODEL=qwen3:4b python server.py

# PowerShell
$env:OLLAMA_MODEL='qwen3:4b'; python server.py
```

## How the AI fits

RoboGuard uses a locally served open-weight language model (Gemma 3 1B by default) to interpret a structured telemetry snapshot alongside recent trends. It connects multiple readings into a human-readable hypothesis and inspection step. The displayed demo indicators are intentionally transparent threshold-based signals; the model explains them, while the UI does not pretend a threshold is machine learning. Ollama and Gemma are optional and are not bundled with this repository.

## Current scope and next steps

This is a hack-day prototype with synthetic telemetry, illustrative event history, and no robot-control interface. It is not validated for safety-critical maintenance. Good next contributions include ROS 2 / MQTT ingestion, configurable sensor thresholds, persistent event history, and evaluation against labeled failure traces.

## Stack

- HTML, CSS, and vanilla JavaScript
- Python standard library HTTP server (no third-party dependencies)
- Ollama local API and Gemma 3 1B (optional open-weight inference)

## License

MIT. See [LICENSE](LICENSE).

