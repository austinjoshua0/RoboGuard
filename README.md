# RoboGuard

**Robot stats made easier for all to read.** RoboGuard is an open source robotic and micro controller diagnostic dashboard that helps an any engineer spot unusual activity and turn it into a practical and easier next inspection. The demo follows a warehouse rover with a heating left wheel motor and an encoder mismatch.

**Live demo of the software:** <https://austinjoshua0.github.io/RoboGuard/>. It runs the simulated dashboard in the browser of your choice. AI explanations use the optional local Ollama setup below.

## Why does this exist?

A robot can keep on moving even while a motor overheats or its wheels stop behaving properly. These signals are easy to miss in raw logs and lead to many complex problems on the long run. RoboGuard puts the real live data and  readings, trend lines, alerts, and a plain easy to read language diagnostics all in one place.

## Who might find this useful?

Many freshers who are getting into the world of robotics, or who are quite new to this field who have no idea on how to build, and who do not know what to do when something goes wrong. If their robot or personal passion project using microcontrollers go wrong, or has an error or bug, may it be physical or software, it should be easy to read, and easy to solve with the agent built in. When something goes wrong, it should not be an hassle to fix it, but it is how we learn on how to fix it by ourselves, and solve it. To minimize stress and worry when something goes wrong for someone who is new to robotics and engineering, and to not discourage them. 

## What does it do?

1. Streams real simulated motor temperature, chassis vibration, battery voltage, and wheel spin readings/recordings. 
2. Visual trends and highlights elevateing temperature and wheel encoder drift.
3. Asks a local running open weight model to explain correlated telemetry, state uncertainty, and suggest a safe inspection. Just like a mentor always there to help. 
4. Always exports a JSON diagnostic snapshot and a CSV event log.
5. Always runs locally. Telemetry stays in the browser; the optional model request goes to your local Ollama service.

## To run in the dashboard

Requires Python 3.9 or newer and a modern browser. No Python packages are required.

```bash
python server.py
```

Open <http://localhost:8000>. The telemetry simulator and heuristic guidance work without an AI assisted model. To enable generated explanations, install [Ollama](https://ollama.com/) and pull a small open weighted model:

```bash
ollama pull gemma3:1b
```

Then start Ollama and click **Ask AI to diagnose**. RoboGuard sends the latest readings to Ollama's local `/api/chat` endpoint server; and the model output is an advisory mentor explanation, and not an autonomous control command. Choose another Ollama model with `OLLAMA_MODEL` (for example `qwen3:4b`) and a custom local end point with `OLLAMA_URL` before starting the server.

```bash
# macOS / Linux
OLLAMA_MODEL=qwen3:4b python server.py

# PowerShell
$env:OLLAMA_MODEL='qwen3:4b'; python server.py
```

## How the AI works

RoboGuard uses a local served open weight language model (Gemma 3 1B by default) to interpret a structured telemetry snapshot alongside recent trends. It connects multiple readings into a easy to read human script and step by step inspection to help. The displayed demo shown indicators are intentionally transparent threshold based signals; and the model explains them, while the UI does not pretend a threshold is machine learning. Ollama and Gemma are optional and are not bundled with this repository.

## Current scope and next steps

This is a hack day prototype with synthetic telemetry, illustrative event history, and no robot-control interface. It is not validated for safety-critical maintenance. Good next contributions include ROS 2 / MQTT ingestion, configurable sensor thresholds, persistent event history, and evaluation against labeled failure traces.

## Stack

- HTML, CSS, and vanilla JavaScript
- Python standard library HTTP server (no third-party dependencies)
- Ollama local API and Gemma 3 1B (optional open-weight inference)

## License

MIT. See [LICENSE](LICENSE).

