#!/usr/bin/env python3
"""
Capture a block-bound deployment identity witness for the current Virtuals ACP
contract on Base mainnet.

Research tooling only. It performs JSON-RPC reads and does not sign or send
transactions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

from Crypto.Hash import keccak


EXPECTED_CHAIN_ID = 8453
PROXY_ADDRESS = "0x238E541BfefD82238730D00a2208E5497F1832E0"
IMPLEMENTATION_SLOT = (
    "0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc"
)
METHOD_VERSION = "x1-deployment-binding/v0.1"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--rpc-url",
        default=os.environ.get("BASE_RPC_URL", "https://mainnet.base.org"),
    )
    parser.add_argument(
        "--block",
        help="Exact decimal/0x block number. Omit to anchor to the RPC finalized block.",
    )
    parser.add_argument("--out-dir", default="deployment-witness-out")
    return parser.parse_args()


class RpcRecorder:
    def __init__(self, url: str) -> None:
        self.url = url
        self.calls: list[dict[str, Any]] = []
        self._id = 0

    def call(self, method: str, params: list[Any]) -> Any:
        self._id += 1
        payload = {
            "jsonrpc": "2.0",
            "id": self._id,
            "method": method,
            "params": params,
        }
        request_bytes = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        request = Request(
            self.url,
            data=request_bytes,
            headers={"content-type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=30) as response:
            response_bytes = response.read()

        decoded = json.loads(response_bytes.decode("utf-8"))
        self.calls.append({"request": payload, "response": decoded})

        if decoded.get("id") != self._id:
            raise RuntimeError(f"RPC id mismatch for {method}")
        if "error" in decoded:
            raise RuntimeError(f"RPC error for {method}: {decoded['error']}")
        if "result" not in decoded:
            raise RuntimeError(f"RPC result missing for {method}")
        return decoded["result"]


def quantity(value: int) -> str:
    return hex(value)


def decode_address_from_slot(raw: str) -> str:
    if not isinstance(raw, str) or not raw.startswith("0x"):
        raise RuntimeError("implementation slot is not a 0x-prefixed storage word")
    word = raw[2:]
    if len(word) != 64:
        raise RuntimeError(f"implementation slot is {len(word)} hex chars, expected 64")
    if int(word, 16) == 0:
        raise RuntimeError(
            "implementation slot is zero; beacon/proxy branch must be investigated explicitly"
        )
    return "0x" + word[-40:]


def code_bytes(raw: str, label: str) -> bytes:
    if not isinstance(raw, str) or not raw.startswith("0x"):
        raise RuntimeError(f"{label} code is not 0x-prefixed")
    if raw == "0x":
        raise RuntimeError(f"{label} code is empty at sampled block")
    try:
        return bytes.fromhex(raw[2:])
    except ValueError as exc:
        raise RuntimeError(f"{label} code is not valid hex") from exc


def keccak256(data: bytes) -> str:
    digest = keccak.new(digest_bits=256)
    digest.update(data)
    return "0x" + digest.hexdigest()


def sha256(data: bytes) -> str:
    return "0x" + hashlib.sha256(data).hexdigest()


def main() -> None:
    args = parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    rpc = RpcRecorder(args.rpc_url)

    chain_raw = rpc.call("eth_chainId", [])
    chain_id = int(chain_raw, 16)
    if chain_id != EXPECTED_CHAIN_ID:
        raise RuntimeError(
            f"wrong chain: got {chain_id}, expected Base mainnet {EXPECTED_CHAIN_ID}"
        )

    if args.block:
        block_number = int(args.block, 0)
        anchor_source = "explicit_block"
    else:
        finalized = rpc.call("eth_getBlockByNumber", ["finalized", False])
        if not finalized or not finalized.get("number"):
            raise RuntimeError("RPC did not return a finalized block")
        block_number = int(finalized["number"], 16)
        anchor_source = "rpc_finalized_tag"

    block_tag = quantity(block_number)
    block = rpc.call("eth_getBlockByNumber", [block_tag, False])
    if not block:
        raise RuntimeError(f"block {block_tag} not found")
    if int(block["number"], 16) != block_number:
        raise RuntimeError("exact block lookup returned a different block number")
    block_hash = block.get("hash")
    if not isinstance(block_hash, str) or not block_hash.startswith("0x"):
        raise RuntimeError("sampled block has no canonical hash in RPC response")

    raw_slot = rpc.call(
        "eth_getStorageAt",
        [PROXY_ADDRESS, IMPLEMENTATION_SLOT, block_tag],
    )
    implementation = decode_address_from_slot(raw_slot)

    proxy_code_raw = rpc.call("eth_getCode", [PROXY_ADDRESS, block_tag])
    implementation_code_raw = rpc.call("eth_getCode", [implementation, block_tag])

    proxy_code = code_bytes(proxy_code_raw, "proxy")
    implementation_code = code_bytes(implementation_code_raw, "implementation")

    raw_path = out_dir / "raw_rpc.json"
    witness_path = out_dir / "DEPLOYMENT_WITNESS_001.json"

    raw_payload = {
        "artifact_type": "paygod/x1-deployment-binding-raw-rpc/v0.1",
        "rpc_endpoint": args.rpc_url,
        "calls": rpc.calls,
    }
    raw_bytes = (
        json.dumps(raw_payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")
    raw_path.write_bytes(raw_bytes)

    witness = {
        "artifact_type": "paygod/x1-deployment-binding-witness/v0.1",
        "status": "BOUND",
        "method_version": METHOD_VERSION,
        "chain_id": chain_id,
        "block_number": block_number,
        "block_number_hex": block_tag,
        "block_hash": block_hash,
        "block_timestamp_chain_metadata": int(block["timestamp"], 16),
        "anchor_source": anchor_source,
        "proxy_address": PROXY_ADDRESS,
        "implementation_slot": IMPLEMENTATION_SLOT,
        "raw_slot_value": raw_slot,
        "implementation_address": implementation,
        "proxy_code_bytes": len(proxy_code),
        "proxy_code_keccak256": keccak256(proxy_code),
        "proxy_code_sha256": sha256(proxy_code),
        "implementation_code_bytes": len(implementation_code),
        "implementation_code_keccak256": keccak256(implementation_code),
        "implementation_code_sha256": sha256(implementation_code),
        "raw_rpc_sha256": sha256(raw_bytes),
        "raw_evidence_file": raw_path.name,
        "rpc_endpoint": args.rpc_url,
        "limitations": [
            "Block timestamp is chain metadata, not independent trusted time.",
            "This witness binds deployed proxy/implementation bytecode identity at the sampled block only.",
            "It does not establish source equivalence, contract safety, evaluator quality, or PayGod authority.",
        ],
    }
    witness_path.write_text(
        json.dumps(witness, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(witness, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
