#------------------AMINU-EDIT------------------#
# Classic one-line subtitles for the credits, synced to the audio.
# A line appears and disappears instantly, and only one line is on screen at a time.
#
# Two subtitle files are used (see the notes at the top of each):
#   game/credits_monologue.txt   Monika's spoken monologue before the credits (bgm/end-voice.ogg)
#   game/credits_lyrics.txt      the song lyrics during the credits (bgm/credits.ogg)
# credits.rpy shows each screen at the moment its audio starts, so every line's time is counted
# from that moment.

init -1 python:
    # credits2 starts the song with "<from 50.0>bgm/credits.ogg". Times in credits_lyrics.txt are
    # positions in the song itself, so this is subtracted from them.
    credits_sub_song_offset = 50.0

    # The monologue screen is shown right when bgm/end-voice.ogg starts from its beginning.
    credits_monologue_offset = 0.0

    credits_sub_max_hold = 5.0      # longest a line stays up when you don't give it an end time
    credits_sub_default_len = 2.0   # how long the very last line stays when it has no end time

init python:
    import re

    def credits_sub_parse(text, offset):
        # Format of a line:  [mm:ss.xx] lyric      or      [mm:ss.xx-mm:ss.xx] lyric
        pattern = re.compile(r"^\[(\d+):(\d+(?:\.\d+)?)(?:-(\d+):(\d+(?:\.\d+)?))?\]\s*(.*\S)\s*$")

        entries = []
        no_time = 0
        too_early = 0

        for raw in text.splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue

            m = pattern.match(line)
            if not m:
                no_time += 1
                continue

            start = int(m.group(1)) * 60 + float(m.group(2))
            end = None
            if m.group(3) is not None:
                end = int(m.group(3)) * 60 + float(m.group(4))

            # Anything before the point where the screen starts is ignored
            # (for the lyrics, that is the part already shown by credits).
            if start < offset:
                too_early += 1
                continue

            entries.append((start, end, m.group(5)))

        entries.sort(key=lambda e: e[0])

        result = []
        for i, (start, end, line) in enumerate(entries):
            next_start = entries[i + 1][0] if i + 1 < len(entries) else None

            if end is None:
                if next_start is not None:
                    end = min(next_start, start + credits_sub_max_hold)
                else:
                    end = start + credits_sub_default_len
            elif next_start is not None:
                # Never overlap the next line: only one line is shown at a time.
                end = min(end, next_start)

            delay = start - offset
            hold = max(end - start, 0.1)
            result.append((delay, hold, line))

        return result, no_time, too_early

    def credits_sub_load(filename, offset):
        try:
            f = renpy.file(filename)
            try:
                data = f.read()
            finally:
                f.close()

            if isinstance(data, bytes):
                data = data.decode("utf-8")
            data = data.lstrip(u"﻿")

            result, no_time, too_early = credits_sub_parse(data, offset)
            print("credits subtitles:", filename + ":", len(result), "lines loaded,", no_time, "without a time,", too_early, "before the start point (ignored)")
            return result
        except Exception as e:
            print("credits subtitles: couldn't load", filename + ":", repr(e))
            return []

    credits_subtitle_list = credits_sub_load("credits_lyrics.txt", credits_sub_song_offset)
    credits_monologue_list = credits_sub_load("credits_monologue.txt", credits_monologue_offset)

# Same look as the lyrics already shown in credits.rpy, a little smaller, with an outline
# so the text stays readable over the credits pictures.
# xmaximum is wide so a lyric stays on one line; lower the size if a long line ever wraps.
init 1 style credits_subtitle is monika_credits_text:
    kerning 2
    size 45
    xmaximum 1240
    text_align 0.5
    outlines [(5, "#000", 0, 0), (1, "#b59", 0, 0)]

# Hidden until its time, then shown instantly for `hold` seconds, then hidden again.
transform credits_subtitle_fx(delay, hold):
    xalign 0.5 yalign 0.95
    alpha 0.0
    linear delay alpha 0.0
    alpha 1.0
    linear hold alpha 1.0
    alpha 0.0

screen credits_subtitles():
    zorder 100
    for delay, hold, line in credits_subtitle_list:
        text _(line) style "credits_subtitle" at credits_subtitle_fx(delay, hold)

screen credits_monologue_subtitles():
    zorder 100
    for delay, hold, line in credits_monologue_list:
        text _(line) style "credits_subtitle" at credits_subtitle_fx(delay, hold)
#----------------------------------------------#
