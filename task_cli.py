#!/usr/bin/env python3
import sys, os, json
from datetime import datetime

TASKS_FILE = "tasks.json"
VALID_STATUSES = ("todo", "in-progress", "done")

def now_iso():
    return datetime.now().isoformat(timespec='seconds')

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        return json.load(open(TASKS_FILE, "r", encoding="utf-8"))
    except:
        return []

def save_tasks(tasks):
    json.dump(tasks, open(TASKS_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

def next_id(tasks):
    return max([t.get("id",0) for t in tasks]+[0]) + 1

def find_task(tasks, tid):
    try:
        tid = int(tid)
    except:
        return None
    for t in tasks:
        if int(t.get("id",0)) == tid:
            return t
    return None

def cmd_add(args):
    if not args:
        print("Error: description required")
        return
    tasks = load_tasks()
    t = {"id": next_id(tasks), "description": args[0], "status":"todo", "createdAt":now_iso(), "updatedAt":now_iso()}
    tasks.append(t)
    save_tasks(tasks)
    print(f"Task added (ID: {t['id']})")

def cmd_update(args):
    if len(args)<2: return print("Error: usage update ID \"new description\"")
    t = find_task(load_tasks(), args[0])
    if not t: return print(f"Error: task {args[0]} not found")
    t["description"] = args[1]
    t["updatedAt"] = now_iso()
    save_tasks(load_tasks())
    tasks = load_tasks()
    save_tasks(tasks)
    print(f"Task {args[0]} updated")

def cmd_delete(args):
    if not args: return print("Error: usage delete ID")
    tid=args[0]
    tasks=load_tasks()
    t=find_task(tasks, tid)
    if not t: return print(f"Error: task {tid} not found")
    tasks=[x for x in tasks if int(x.get("id",0))!=int(tid)]
    save_tasks(tasks)
    print(f"Task {tid} deleted")

def cmd_mark(args, status):
    if not args: return print(f"Error: usage {status} ID")
    t=find_task(load_tasks(), args[0])
    if not t: return print(f"Error: task {args[0]} not found")
    t["status"]=status
    t["updatedAt"]=now_iso()
    save_tasks(load_tasks())
    tasks=load_tasks()
    save_tasks(tasks)
    print(f"Task {args[0]} marked as {status}")

def cmd_list(args):
    tasks=load_tasks()
    if len(args)>=1 and args[0] in VALID_STATUSES:
        tasks=[t for t in tasks if t["status"]==args[0]]
    for t in tasks:
        print(f"[{t['id']}] ({t['status']}) {t['description']}\n    created: {t['createdAt']}, updated: {t['updatedAt']}")
    if tasks: print(f"\n{len(tasks)} task(s) listed.")

def main():
    if len(sys.argv)<2: return print("Usage: add/update/delete/mark-in-progress/mark-done/list")
    cmd=sys.argv[1].lower()
    args=sys.argv[2:]
    if cmd=="add": cmd_add([" ".join(args)] if len(args)>1 else args)
    elif cmd=="update": cmd_update([args[0], " ".join(args[1:])])
    elif cmd=="delete": cmd_delete(args)
    elif cmd=="mark-in-progress": cmd_mark(args,"in-progress")
    elif cmd=="mark-done": cmd_mark(args,"done")
    elif cmd=="list": cmd_list(args)
    else: print("Unknown command")

if __name__=="__main__":
    main()

