""" In case you want to delete all logs, just run me :) """

import os


def clear_all_logs(log_dir='./'):
    files = os.listdir(log_dir)

    for file in files:
        if file.endswith('.log'):
            os.remove(os.path.join(log_dir, file))


if __name__ == "__main__":
    clear_all_logs()
    print("Logs were deleted")
