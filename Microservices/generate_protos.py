import subprocess
import sys
from pathlib import Path

for service in ("recommendations", "marketplace"):
    subprocess.run(
        [sys.executable, "-m", "grpc_tools.protoc", "-I", "../protos",
         "--python_out=.", "--pyi_out=.", "--grpc_python_out=.", "../protos/recommendations.proto"],
        cwd=service,
        check=True,
    )
    print(service, "→", sorted(p.name for p in Path(service).glob("recommendations_pb2*")))