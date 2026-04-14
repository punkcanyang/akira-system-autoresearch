#!/usr/bin/env python3
"""autoresearch-run: 单 skill 迭代的 CLI 入口。

用法:
    python scripts/run.py <skill-name> [--mode run|reason|scenario] [--rounds N]

也可在 Hermes 中直接触发，不需要手动调用。
"""
import argparse, subprocess, sys, os, json
from datetime import datetime

EVAL_DIR = os.path.join(os.path.dirname(__file__), '..', 'evals')
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

def main():
    parser = argparse.ArgumentParser(description="Akira Autoresearch Runner")
    parser.add_argument("skill", help="skill name to iterate")
    parser.add_argument("--mode", choices=["run", "reason", "scenario"], default="run")
    parser.add_argument("--rounds", type=int, default=3)
    args = parser.parse_args()

    results = []
    for i in range(args.rounds):
        t0 = datetime.now()
        # Phase 2/6: eval
        eval_cmd = [sys.executable, os.path.join(EVAL_DIR, "run_eval.py"), args.skill]
        try:
            out = subprocess.check_output(eval_cmd, text=True, timeout=30)
            data = json.loads(out)
        except Exception as e:
            print(f"[round {i+1}] eval failed: {e}", file=sys.stderr)
            results.append({"round": i+1, "error": str(e)})
            continue

        elapsed = (datetime.now() - t0).total_seconds()
        data["round"] = i + 1
        data["elapsed_s"] = round(elapsed, 1)
        results.append(data)
        print(f"[round {i+1}] score={data.get('total_score')} ({elapsed:.1f}s)")

    # save history
    history_file = os.path.join(DATA_DIR, "history.jsonl")
    with open(history_file, "a") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Saved to {history_file}")

if __name__ == "__main__":
    main()
