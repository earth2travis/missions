#!/usr/bin/env python3
"""Read-only mission board probe.

Usage:
    python3 tools/board-probe.py <mission-slug>            # board overview
    python3 tools/board-probe.py <mission-slug> --runs t_x # run history for one card

Opens ~/.hermes/kanban.db with SQLite-enforced read-only mode (mode=ro);
this script cannot write to the board. Output is plain text for pasting
back to the architect agent.

Healthy readings:
  - status running with hb_age_s under 3600 (Hermes's own staleness
    threshold, DEFAULT_CLAIM_HEARTBEAT_MAX_STALE_SECONDS)
  - fails 0 everywhere
Anything else: paste the raw output to the architect before acting.
"""
import os
import sqlite3
import sys
import time

DB = os.environ.get("HERMES_KANBAN_DB") or os.path.expanduser("~/.hermes/kanban.db")
STALE = 3600  # seconds; mirrors DEFAULT_CLAIM_HEARTBEAT_MAX_STALE_SECONDS


def utc(ts):
    return time.strftime("%Y-%m-%d %H:%M", time.gmtime(ts)) if ts else "-"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not args:
        sys.exit(__doc__.strip())
    slug = args[0]
    run_task = args[1] if "--runs" in sys.argv and len(args) > 1 else None

    if not os.path.exists(DB):
        sys.exit(f"board DB not found at {DB} — run this on the host where the "
                 "Hermes fleet lives (or set HERMES_KANBAN_DB)")
    db = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    now = int(time.time())

    if run_task:
        rows = db.execute(
            "SELECT id, profile, status, outcome, started_at, ended_at,"
            "       last_heartbeat_at, substr(coalesce(summary,''),1,300) AS summary,"
            "       substr(coalesce(error,''),1,300) AS error"
            " FROM task_runs WHERE task_id = ? ORDER BY id",
            (run_task,),
        ).fetchall()
        if not rows:
            sys.exit(f"no runs found for {run_task}")
        for r in rows:
            hb = f"{now - r['last_heartbeat_at']}s ago" if r["last_heartbeat_at"] else "-"
            print(f"run {r['id']}  profile={r['profile']}  status={r['status']}"
                  f"  outcome={r['outcome'] or '-'}")
            print(f"  started={utc(r['started_at'])}  ended={utc(r['ended_at'])}"
                  f"  heartbeat={hb}")
            if r["summary"]:
                print(f"  summary: {r['summary']}")
            if r["error"]:
                print(f"  error:   {r['error']}")
        comments = db.execute(
            "SELECT author, body, created_at FROM task_comments"
            " WHERE task_id = ? ORDER BY id",
            (run_task,),
        ).fetchall()
        if comments:
            print(f"\nCOMMENTS ({len(comments)}):")
            for c in comments:
                print(f"--- {c['author']} @ {utc(c['created_at'])} ---")
                print(c["body"])
        return

    rows = db.execute(
        "SELECT id, substr(title, length(?) + 6, 44) AS card, assignee, status,"
        "       completed_at, last_heartbeat_at, consecutive_failures AS fails"
        " FROM tasks WHERE title LIKE ? ORDER BY created_at",
        (slug, f"[m:{slug}]%"),
    ).fetchall()
    if not rows:
        sys.exit(f"no cards found for mission slug '{slug}'")

    fmt = "{:<12} {:<44} {:<22} {:<8} {:<17} {:>9} {:>5}"
    print(fmt.format("id", "card", "assignee", "status", "done_utc", "hb_age_s", "fails"))
    flags = []
    for r in rows:
        hb_age = (now - r["last_heartbeat_at"]) if r["last_heartbeat_at"] else None
        print(fmt.format(r["id"], r["card"] or "", r["assignee"] or "-", r["status"],
                         utc(r["completed_at"]),
                         str(hb_age) if hb_age is not None else "-", r["fails"]))
        if r["status"] == "running" and hb_age is not None and hb_age > STALE:
            flags.append(f"{r['id']}: heartbeat stale ({hb_age}s > {STALE}s)")
        if r["fails"]:
            flags.append(f"{r['id']}: consecutive_failures={r['fails']}")
    if flags:
        print("\nFLAGS:")
        for f in flags:
            print(f"  - {f}")


if __name__ == "__main__":
    main()
