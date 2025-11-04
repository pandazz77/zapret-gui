import subprocess
import platform


def get_pid_by_name_windows(process_name: str) -> int | None:
    result = subprocess.run(
        ['tasklist', '/FI', f'IMAGENAME eq {process_name}', '/FO', 'CSV'],
        capture_output=True,
        text=True,
        check=True
    )
    if result.stdout.count("\n") == 1:
        return None
    header, content = result.stdout.strip().split('\n')
    content = map(lambda s: s.replace("\"",""),content.split(","))
    image_name, pid, session_name, session, mem_usage = content
    return int(pid)

def get_pid_by_name(process_name: str) -> int | None:
    if platform.system() == "Windows":
        return get_pid_by_name_windows(process_name)