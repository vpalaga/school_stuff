from sound_render import play_tone_rt

class UnknownNote(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def A3_scale(x:float|int)->float:
    return 55 * (2 ** x)

class Note:
    notes_lookup = {
        3: "C",
        4: "C#",
        5: "D",
        6: "D#",
        7: "E",
        8: "F",
        9: "F#",
        10: "G",
        11: "G#",
        0: "A",
        1: "A#",
        2: "B"
    }
    notes = len(notes_lookup)

    def __init__(self, note:int, octave:int)->None:
        self.note = note # from 0 to 11
        self.octave = octave

        if not 0 <= note <= 11:
            raise UnknownNote(f"Note: {self.note} isn't between 0 and 11")

        self.frequency = self.calculate_frequency()

    def __repr__(self):
        return Note.notes_lookup[self.note]+str(self.octave)

    def calculate_frequency(self)->float:
        # check reademe.md for derivation
        raw_note = (self.note / Note.notes) + self.octave
        return A3_scale(raw_note)


class Chord:
    def __init__(self, *notes:Note)->None:
        self.notes = notes
        self.duration_s = .3

    def render(self):
        # render the note
        play_tone_rt(frequencies=[n.frequency for n in self.notes], duration=self.duration_s)

    def __repr__(self):
        return str([n.__repr__() for n in self.notes])

if __name__ == "__main__":

    for octave in range(1, 7):
        for note in range(12):
            ch1 = Chord(
                Note(note,octave)
            )
            print(ch1)
            ch1.render()

