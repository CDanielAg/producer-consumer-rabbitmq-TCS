from datetime import datetime, timezone
import os
from pathlib import Path
import subprocess
import sys
import time


root = Path(__file__).resolve().parents[1]
app = root / "app"
message = "Hola desde el ejemplo Producer Consumer"
environment = os.environ.copy()
local_dependencies = root / ".deps"
if local_dependencies.exists():
    environment["PYTHONPATH"] = str(local_dependencies)

consumer = subprocess.Popen(
    [sys.executable, "-u", str(app / "receive.py"), "--once"],
    cwd=app,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    env=environment,
)

time.sleep(1)
producer = subprocess.run(
    [sys.executable, "-u", str(app / "send.py"), message],
    cwd=app,
    capture_output=True,
    text=True,
    check=True,
    env=environment,
)

consumer_output, _ = consumer.communicate(timeout=15)
if consumer.returncode != 0:
    raise SystemExit(consumer_output)

evidence = "\n".join(
    [
        "EVIDENCIA PRODUCER CONSUMER CON RABBITMQ",
        "Fecha UTC: " + datetime.now(timezone.utc).isoformat(),
        "",
        "SALIDA DEL PRODUCTOR",
        producer.stdout.strip(),
        "",
        "SALIDA DEL CONSUMIDOR",
        consumer_output.strip(),
        "",
        "RESULTADO: mensaje enviado y recibido correctamente.",
        "",
    ]
)
output = root.parent / "docs" / "evidencia-ejecucion.txt"
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(evidence, encoding="utf-8")
print(evidence)
print("Evidencia guardada en " + str(output))
