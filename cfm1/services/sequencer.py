import zmq
from time import sleep
from decimal import Decimal
from time import monotonic, sleep
from cfm1.config import (
    STEPS_MAX, TRACKS_MAX,
    NOTE_PITCH, NOTE_STATUS, NOTE_LENGTH, NOTE_INFO)


def send_note(trackidx, note):
    print("{}: {}".format(trackidx, note))


def run():
    context = zmq.Context()
    sockin = context.socket(zmq.PULL)
    sockin.bind("ipc://sequencer")
    context2 = zmq.Context()
    sockout = context2.socket(zmq.PUSH)
    sockout.connect("ipc://sequencerstatus")

    # prepare data
    play = True
    bpm = Decimal(120)
    precision = Decimal(16)
    track_length = [64] * TRACKS_MAX
    notes = [
        [[] for x in range(STEPS_MAX)]
        for x in range(TRACKS_MAX)]
    nextcall = monotonic()
    step_index = 0

    try:
        sockout.send_json(("READY", ))
        while True:
            # Poll message received from the UI
            while sockin.poll(timeout=1):
                msg = sockin.recv_json()
                cmd, args = msg[0], msg[1:]
                if cmd == "EXIT":
                    raise SystemExit()

                elif cmd == "BPM":
                    bpm = Decimal(args[0])

                elif cmd == "TRACK_LENGTH":
                    track_length[args[1]] = args[2]

                elif cmd == "NOTEADD":
                    note = args[0]
                    track, step = note[NOTE_INFO]
                    notes[track][step].append(note)

                elif cmd == "NOTEDEL":
                    note = args[0]
                    track, step = note[NOTE_INFO]
                    step_notes = notes[track][step]
                    for step_note in step_notes:
                        if step_note[NOTE_PITCH] != note[NOTE_PITCH]:
                            continue
                        step_notes.remove(step_note)
                        break

                elif cmd == "NOTEUPD":
                    note = args[0]
                    track, step = note[NOTE_INFO]
                    step_notes = notes[track][step]
                    for step_note in step_notes:
                        if step_note[NOTE_PITCH] == note[NOTE_PITCH]:
                            continue
                        step_notes[NOTE_LENGTH] = note[NOTE_LENGTH]
                        break

                elif cmd == "START":
                    play = True

                elif cmd == "STOP":
                    play = False
                    step_index = 0

                elif cmd == "PAUSE":
                    play = False

                else:
                    print("[SEQ] Unhandled [{}, {}]".format(cmd, args))

            # Run the sequencer
            interval = float(60 / bpm / precision)
            nextcall = nextcall + interval
            step_index += 1

            # Play the sequence
            if play:
                for trackidx, track in enumerate(notes):
                    step = step_index % track_length[trackidx]
                    for note in track[step]:
                        send_note(trackidx, note)

            # Check for the next loop
            now = monotonic()
            if nextcall - now > 0:
                sleep(nextcall - now)
            else:
                nextcall = monotonic()


    finally:
        sockout.send_json(("LEAVING", ))
        sockin.close()
        sockout.close()

if __name__ == "__main__":
    while True:
        try:
            run_restart()
        except SystemExit:
            break
