import argparse
import sys
import traceback
import queue
import threading

from agent.graph import run_agent_thread


def main():
    parser = argparse.ArgumentParser(description="Run engineering project planner")
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="Max execution time in seconds (default: 60)"
    )

    args = parser.parse_args()

    try:
        user_prompt = input("Enter your project prompt: ")

        log_q = queue.Queue()

        # ✅ Run agent in separate thread (prevents freezing)
        agent_thread = threading.Thread(
            target=run_agent_thread,
            args=(user_prompt, log_q),
            daemon=True
        )

        agent_thread.start()

        print("\n🚀 Running Agent...\n")

        start_time = 0

        # ✅ Live log streaming
        while agent_thread.is_alive() or not log_q.empty():
            try:
                event = log_q.get(timeout=1)

                if event[0] == "log":
                    level = event[1]
                    msg = event[2]

                    if level == "error":
                        print(f"❌ {msg}")
                    elif level == "success":
                        print(f"✅ {msg}")
                    else:
                        print(f"ℹ️ {msg}")

                elif event[0] == "stage":
                    print(f"\n🔄 Stage: {event[1].upper()}")

                elif event[0] == "plan":
                    print("\n📐 Plan Generated:")
                    print(event[2])

                elif event[0] == "task_plan":
                    print("\n🧠 Task Plan:")
                    print(event[2])

                elif event[0] == "done":
                    print("\n🎉 Project generation completed!")

                elif event[0] == "error":
                    print("\n❌ Agent failed!")

            except queue.Empty:
                continue

        agent_thread.join(timeout=args.timeout)

        if agent_thread.is_alive():
            print("\n⚠️ Timeout reached. Stopping execution.")

    except KeyboardInterrupt:
        print("\n⛔ Operation cancelled by user.")
        sys.exit(0)

    except Exception as e:
        traceback.print_exc()
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()