import contextlib
import subprocess, os

def merge_dicts(a, b):
    return dict(list(a.items()) +  list(b.items()))

# Unix, Windows and old Macintosh end-of-line
newlines = ['\n', '\r\n', '\r']
def _unbuffered(proc, stream='stdout'):
    stream = getattr(proc, stream)
    with contextlib.closing(stream):
        while True:
            out = []
            last = stream.read(1)
            # Don't loop forever
            if last == '' and proc.poll() is not None:
                break
            while last not in newlines:
                # Don't loop forever
                if last == '' and proc.poll() is not None:
                    break
                out.append(last)
                last = stream.read(1)
            out = ''.join(out)
            yield out

def proc_read(cmd, env=None):
    """gives an lines iterator over merged stdout and stderr of cmd with dict env"""
    cmd = cmd.split()
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        # Make all end-of-lines '\n'
        universal_newlines=True,
        env=merge_dicts(os.environ, env),
    )
    for line in _unbuffered(proc):
        yield(line)

