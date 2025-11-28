import json
import sys
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

class Task:
    def __init__(self, id, description, status, created_at, updated_at):
        self.id = id
        self.description = description
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at
        }


class TaskManager:
    def __init__(self):
        self.tasks = self.load()

    def load(self):
        if not os.path.exists(TASKS_FILE):
            return []
        try:
            data = json.load(open(TASKS_FILE, "r"))
            tasks = []
            for t in data:
                tasks.append(Task(
                    t.get("id"),
                    t.get("description"),
                    t.get("status"),
                    t.get("createdAt"),
                    t.get("updatedAt")
                ))
            return tasks
        except:
            return []

    def save(self):
        data = []
        for t in self.tasks:
            data.append(t.to_dict())
        json.dump(data, open(TASKS_FILE, "w"), indent=2)

    def next_id(self):
        if not self.tasks:
            return 1
        ids = [t.id for t in self.tasks]
        return max(ids) + 1

    def find(self, id):
        try:
            id = int(id)
        except:
            return None
        for t in self.tasks:
            if t.id == id:
                return t
        return None

    def add(self, desc):
        time_now = datetime.now().isoformat(timespec='seconds')
        new_task = Task(
            self.next_id(),
            desc,
            "todo",
            time_now,
            time_now
        )
        self.tasks.append(new_task)
        self.save()
        print("Task added")

    def update(self, id, new_desc):
        task = self.find(id)
        if not task:
            print("Task not found")
            return
        task.description = new_desc
        task.updated_at = datetime.now().isoformat(timespec='seconds')
        self.save()
        print("Task updated")

    def delete(self, id):
        task = self.find(id)
        if not task:
            print("Task not found")
            return
        self.tasks = [t for t in self.tasks if t.id != task.id]
        self.save()
        print("Task deleted")

    def set_status(self, id, status):
        task = self.find(id)
        if not task:
            print("Task not found")
            return
        task.status = status
        task.updated_at = datetime.now().isoformat(timespec='seconds')
        self.save()
        print("Status changed")

    def list_all(self, filter_status=None):
        items = self.tasks
        if filter_status:
            items = [t for t in items if t.status == filter_status]
        for t in items:
            print(f"[{t.id}] ({t.status}) {t.description}")
        if items:
            print(str(len(items)) + " task(s)")


def main():
    if len(sys.argv) < 2:
        print("Usage: add/update/delete/start/done/list")
        return

    cmd = sys.argv[1]
    args = sys.argv[2:]

    manager = TaskManager()

    if cmd == "add":
        if not args:
            print("Description required")
            return
        manager.add(" ".join(args))

    elif cmd == "update":
        if len(args) < 2:
            print("Usage: update ID text")
            return
        manager.update(args[0], " ".join(args[1:]))

    elif cmd == "delete":
        manager.delete(args[0])

    elif cmd == "start":
        manager.set_status(args[0], "in-progress")

    elif cmd == "done":
        manager.set_status(args[0], "done")

    elif cmd == "list":
        if len(args) >= 1:
            manager.list_all(args[0])
        else:
            manager.list_all()

    else:
        print("Unknown command")


if __name__ == "__main__":
    main()
