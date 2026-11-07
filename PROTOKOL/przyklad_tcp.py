"""Read-only GRYF TCP example: python przyklad_tcp.py IP --port 5000 --id 2."""
import argparse
import socket
import time

class Lines:
    def __init__(self):
        self.buffer = bytearray()

    def feed(self, chunk):
        lines = []
        for byte in chunk:
            if byte in (10, 13):
                if self.buffer:
                    lines.append(self.buffer.decode('ascii', errors='strict'))
                    self.buffer.clear()
            else:
                self.buffer.append(byte)
                if len(self.buffer) > 4096:
                    raise ValueError('Frame longer than 4096 bytes')
        return lines

def output_report(line, module_id):
    prefix, separator, text = line.partition('=')
    if not separator or prefix not in ('O', 'o'):
        return None
    try:
        values = [int(value) for value in text.split(',')]
    except ValueError:
        return None
    if len(values) not in (7, 9) or values[0] != module_id:
        return None
    if any(value not in (0, 1) for value in values[1:]):
        return None
    return values[1:]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('host')
    parser.add_argument('--port', type=int, default=5000)
    parser.add_argument('--id', type=int, required=True)
    args = parser.parse_args()
    if not 1 <= args.id <= 35:
        parser.error('ID must be 1..35')
    framing = Lines()
    with socket.create_connection((args.host, args.port), timeout=3) as conn:
        conn.sendall(f'AT+GetOut={args.id}\r'.encode('ascii'))
        deadline = time.monotonic() + 2
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError('No matching output report; state remains unknown')
            conn.settimeout(remaining)
            chunk = conn.recv(4096)
            if not chunk:
                raise ConnectionError('Disconnected; state remains unknown')
            for line in framing.feed(chunk):
                print('RX:', line)
                state = output_report(line, args.id)
                if state is not None:
                    print('Outputs:', state)
                    return
                # Other IDs, input events and acknowledgements may interleave.

if __name__ == '__main__':
    main()
