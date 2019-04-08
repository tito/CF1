# IPC Protocol

CFM1 UI is starting few background process to handle:
- Sequencer
- Encoder GPIO input
- Midi Dyn INPUT
- Midi USB INPUT

Communication is handled with ZMQ under ipc transport
(address could be changed at any time later to support fully
system background process if needed.)

Message are JSON based, with this format:

    ["CMD", arg1, arg2...]

For example:

    ["BPM", 127]
    ["TRACK_LENGTH", 1, 128]

## UI <-> Sequencer

There is 2 communications channels using PUSH/PULL:
- `ipc://sequencer`: UI (PUSH) -> Sequencer (PULL)
- `ipc://sequencerstatus`: Sequencer (PUSH) -> UI (PULL)

The UI can send to the sequencer:

- `["EXIT"]`
  - Sequencer process must exit asap
- `["BPM", bpm]`
  - Change the BPM
  - `bpm`: new BPM
- `["TRACK_LENGTH", trackindex, steps]`
  - Change the BPM to `bpm`
  - `trackindex`: Index of the track, from 0 to 7
  - `steps`: New track length, from 0 to STEPS_MAX
- `["NOTEADD", note]`:
  - Add a new note in the sequencer
  - `note`: Note is an array that contains:
    - 0: Pitch of the note
    - 1: Status of the note (ignored)
    - 2: Length of the note in steps
    - 3: Array of [Track index, Step index]
- `["NOTEDEL", note]`:
  - Delete a note from the sequencer.
  - `note`: Note is an array that contains:
    - 0: Pitch of the note
    - 1: Status of the note (ignored)
    - 2: Length of the note in steps
    - 3: Array of [Track index, Step index]
- `["NOTEUPD", note]`:
  - Update the note length of the sequencer
  - `note`: Note is an array that contains:
    - 0: Pitch of the note
    - 1: Status of the note (ignored)
    - 2: New length of the note in steps
    - 3: Array of [Track index, Step index]
- `["PLAY"]`
  - Start the sequencer
- `["PAUSE"]`
  - Pause the sequencer (the step index is not resetted)
- `["STOP"]`
  - Stop the sequencer (the step index is back to 0)

The sequencer gives feedback to the UI with:

- `["STEP", stepindex]`
  - Current step playing
  - `stepindex`: Index of the current step, from 0 to STEPS_MAX - 1
