import zmq
import rtmidi
import mido
from time import sleep
from decimal import Decimal
from time import monotonic, sleep
from cfm1.config import (
    STEPS_MAX, TRACKS_MAX,
    NOTE_PITCH, NOTE_STATUS, NOTE_LENGTH, NOTE_INFO)


# open midi
midiout = rtmidi.MidiOut()
port = mido.open_output(midiout.get_ports()[-1])


notes_to_stop = []

def send_note_on(note):
    trackidx, step = note[NOTE_INFO]
    print("{}: {}".format(trackidx, note))
    msg = mido.Message(
        "note_on",
        note=note[NOTE_PITCH] + 24,
        channel=trackidx + 1)
    port.send(msg)
    print("ON {}", note[NOTE_PITCH] + 24)

    note[NOTE_STATUS] = note[NOTE_LENGTH]
    print(note)
    notes_to_stop.append(note)


def send_note_off(note):
    trackidx, step = note[NOTE_INFO]
    msg = mido.Message(
        "note_off",
        note=note[NOTE_PITCH] + 24,
        channel=trackidx + 1)
    port.send(msg)
    print("OFF {}", note[NOTE_PITCH] + 24)

    notes_to_stop.remove(note)


def run():
    context = zmq.Context()
    sockin = context.socket(zmq.PULL)
    sockin.bind("ipc://sequencer")
    context2 = zmq.Context()
    sockout = context2.socket(zmq.PUSH)
    sockout.connect("ipc://sequencerstatus")

    # prepare data
    play = False
    bpm = Decimal(120)
    precision = Decimal(16)
    track_length = [64] * TRACKS_MAX
    notes = [
        [[] for x in range(STEPS_MAX)]
        for x in range(TRACKS_MAX)]
    nextcall = monotonic()
    step_index = -1

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
                    track_length[args[0]] = args[1]

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
                        if step_note[NOTE_PITCH] != note[NOTE_PITCH]:
                            continue
                        step_note[NOTE_LENGTH] = note[NOTE_LENGTH]
                        break

                elif cmd == "START":
                    play = True

                elif cmd == "STOP":
                    play = False
                    step_index = -1

                elif cmd == "PAUSE":
                    play = False

                else:
                    print("[SEQ] Unhandled [{}, {}]".format(cmd, args))

            # Run the sequencer
            interval = float(60 / bpm / precision)
            nextcall = nextcall + interval

            # Play the sequence
            if play:
                step_index = (step_index + 1) % STEPS_MAX
                print("[SEQ] Play {}".format(step_index))

                # Stop previous note if needed
                to_delete = []
                for note in notes_to_stop:
                    note[NOTE_STATUS] -= 1
                    if note[NOTE_STATUS] == 0:
                        send_note_off(note)
                for note in to_delete:
                    notes_to_stop.remove(note)

                for trackidx, track in enumerate(notes):
                    step = step_index % track_length[trackidx]
                    for note in track[step]:
                        send_note_on(note)

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
