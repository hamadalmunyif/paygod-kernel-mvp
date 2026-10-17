#!/usr/bin/env python3
"""Synthetic Docker replay smoke for opt-in typed-v1 only.

Run generated receipt replay with an existing bind-mounted output PARENT and
a previously nonexistent CHILD. Does not prove bitwise receipt equality,
source authenticity, time authority, or production authorization.
"""
import argparse
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "examples/policy-typed-comparisons"
IMAGE = "paygod/typed-replay-ci:local"


def run(args, *, env=None):
    return subprocess.run(args, cwd=ROOT, env=env, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cli", required=True)
    args = parser.parse_args()
    cli = str(Path(args.cli).resolve())
    assert Path(cli).is_file(), cli
    assert shutil.which("docker"), "Docker must be installed for replay smoke"

    with tempfile.TemporaryDirectory(prefix="paygod-typed-docker-replay-") as d:
        tmp = Path(d)
        build_dir = tmp / "docker-build"
        build_dir.mkdir()
        shutil.copytree(ROOT / "out", build_dir / "out")
        (build_dir / "Dockerfile").write_text(
            'FROM mcr.microsoft.com/dotnet/runtime:8.0\n'
            'COPY out/ /app/\n'
            'WORKDIR /app\n'
            'ENTRYPOINT ["/app/paygod"]\n',
            encoding="utf-8",
        )
        build = run(["docker", "build", "-t", IMAGE, str(build_dir)])
        assert build.returncode == 0, (build.stdout[-4000:], build.stderr[-4000:])
        image_id = run(["docker", "image", "inspect", IMAGE, "--format", "{{.Id}}"])
        assert image_id.returncode == 0, image_id.stderr
        print("Observed local Docker test image ID:", image_id.stdout.strip())

        source = tmp / "admitted-synthetic-input.json"
        source.write_text('{"input":{"block":false}}', encoding="utf-8")
        original_dir = tmp / "original"
        parent_dir = tmp / "replay-parent"
        parent_dir.mkdir()
        environment = os.environ.copy()
        environment.update({
            "PAYGOD_CLOCK": "2026-10-17T00:00:00Z",
            "PAYGOD_RUNNER_IMAGE": IMAGE,
            "PAYGOD_RUNNER_DIGEST": image_id.stdout.strip(),
        })
        first = run([cli, "run", "--pack", str(PACK), "--input", str(source),
                     "--out", str(original_dir)], env=environment)
        assert first.returncode == 0, (first.stdout, first.stderr)
        original = json.loads((original_dir / "receipt.json").read_text(encoding="utf-8"))
        replay = original["replay"]["command"]
        assert '-v "<OUT_PARENT_DIR>:/out-parent:rw"' in replay
        assert "--out /out-parent/<NEW_RUN_SUBDIR>" in replay
        replacements = {
            "<OUT_PARENT_DIR>": str(parent_dir),
            "<NEW_RUN_SUBDIR>": "fresh-replay",
            "<PACK_DIR>": str(PACK),
            "<INPUT_FILE>": str(source),
        }
        for old, new in replacements.items():
            assert replay.count(old) == 1, (old, replay)
            replay = replay.replace(old, new)
        assert "<" not in replay and ">" not in replay, replay

        command = shlex.split(replay)
        assert command[0:2] == ["docker", "run"], command
        try:
            first_replay = run(command)
            assert first_replay.returncode == 0, (
                first_replay.stdout[-4000:], first_replay.stderr[-4000:])
            replay_dir = parent_dir / "fresh-replay"
            replay_receipt = replay_dir / "receipt.json"
            assert replay_receipt.is_file()
            observed = json.loads(replay_receipt.read_text(encoding="utf-8"))
            assert observed["verdict"]["value"] == original["verdict"]["value"] == "allow"
            assert observed["input"]["canonical_hash"] == original["input"]["canonical_hash"]
            assert observed["pack"]["digest_sha256"] == original["pack"]["digest_sha256"]
            assert (replay_dir / "manifest.json").is_file()
            print("PASS: actual Docker replay completed into a new child, same bounded verdict/input/Pack")
    
            previous_bytes = replay_receipt.read_bytes()
            repeated = run(command)
            assert repeated.returncode == 2, (repeated.stdout, repeated.stderr)
            assert "OUTPUT_DIRECTORY_NOT_FRESH" in repeated.stderr, repeated.stderr
            assert replay_receipt.read_bytes() == previous_bytes
            print("PASS: second replay refused stale child without modifying prior receipt")
        finally:
            # Docker writes bind-mounted files as root by default. Reassign
            # ONLY our isolated test parent to the invoking runner user
            # before Python TemporaryDirectory cleanup; never chmod shared
            # filesystem paths or alter canonical evidence during testing.
            cleanup = run([
                "docker", "run", "--rm", "--entrypoint", "/bin/chown",
                "-v", f"{parent_dir}:/out-parent:rw",
                IMAGE, "-R", f"{os.getuid()}:{os.getgid()}", "/out-parent",
            ])
            assert cleanup.returncode == 0, (cleanup.stdout, cleanup.stderr)

    print("PASS: bounded typed-v1 Docker replay smoke; NOT bitwise receipt identity")


if __name__ == "__main__":
    main()
