
import os
import time
import docker
from datetime import datetime

client = docker.from_env()

target_label = os.getenv("TARGET_LABEL", "self-healing=true")
interval = int(os.getenv("CHECK_INTERVAL", "5"))

def log(message):
    print(f"{datetime.now()} - {message}", flush=True)

log("Self-Healing Monitor Started")

while True:
    try:
        containers = client.containers.list(
            all=True,
            filters={"label": target_label}
        )

        if not containers:
            log("WARNING: No matching containers found")

        for container in containers:
            container.reload()
            status = container.status

            if status != "running":
                log(f"FAULT: {container.name} is {status}")
                container.start()
                log(f"RECOVERY: Restarted {container.name}")

            else:
                health = container.attrs.get(
                    "State", {}
                ).get("Health", {}).get("Status", "unknown")

                if health == "unhealthy":
                    log(f"FAULT: {container.name} is unhealthy")
                    container.restart()
                    log(f"RECOVERY: Restarted {container.name}")
                else:
                    log(f"HEALTHY: {container.name} is running")

    except Exception as error:
        log(f"MONITOR ERROR: {error}")

    time.sleep(interval)
