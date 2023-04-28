
def xor(x, y):
    """Return truth value of ``x`` XOR ``y``."""
    return bool(x) != bool(y)

def _parse_rttm_line(line):
    line = line.decode('utf-8').strip()
    fields = line.split()
    # 0         1                            2   3      4    5    6    7        8     9
    #SPEAKER Bonus.BleakProspect.1.Mix.Smol2 1 0.230 73.178 <NA> <NA> speaker0 <NA> <NA>
    if len(fields) < 9:
        raise IOError('Number of fields < 9. LINE: "%s"' % line)
    file_id = fields[1]
    speaker_id = fields[7]
    channel_id = fields[2]

    # Check valid turn onset.
    try:
        onset = float(fields[3])
    except ValueError:
        raise IOError('Turn onset not FLOAT. LINE: "%s"' % line)
    if onset < 0:
        raise IOError('Turn onset < 0 seconds. LINE: "%s"' % line)

    # Check valid turn duration.
    try:
        dur = float(fields[4])
    except ValueError:
        raise IOError('Turn duration not FLOAT. LINE: "%s"' % line)
    if dur <= 0:
        raise IOError('Turn duration <= 0 seconds. LINE: "%s"' % line)

    return RTTM_Turn(onset, dur=dur, speaker_id=speaker_id, file_id=file_id, channel_id=channel_id)

def load_rttm(rttmf):
    """Load speaker turns from RTTM file.
    For a description of the RTTM format, consult Appendix A of the NIST RT-09
    evaluation plan.
    Parameters
    ----------
    rttmf : str
        Path to RTTM file.
    Returns
    -------
    turns : list of Turn
        Speaker turns.
    speaker_ids : set
        Speaker ids present in ``rttmf``.
    file_ids : set
        File ids present in ``rttmf``.
    References
    ----------
    NIST. (2009). The 2009 (RT-09) Rich Transcription Meeting Recognition
    Evaluation Plan. https://web.archive.org/web/20100606041157if_/http://www.itl.nist.gov/iad/mig/tests/rt/2009/docs/rt09-meeting-eval-plan-v2.pdf
    """
    with open(rttmf, 'rb') as f:
        turns = []
        speaker_ids = set()
        file_ids = set()
        for line in f:
            if line.startswith(b'SPKR-INFO'):
                continue
            turn = _parse_rttm_line(line)
            turns.append(turn)
            speaker_ids.add(turn.speaker_id)
            file_ids.add(turn.file_id)
    return turns, speaker_ids, file_ids

#combine linear entries of speaker turns
def compress_rttm_turns(turn_list):
    curr_starting_turn = turn_list[0]
    compressed_turns = []
    for idx, turn in enumerate(turn_list[1:]):
        # print('-'*20)
        # print('current saved turn',curr_starting_turn)
        # print('current looping turn',turn)
        # z = input('waiting')
        if curr_starting_turn.speaker_id != turn.speaker_id:
            curr_starting_turn.end = turn_list[idx].end
            curr_starting_turn.dur = curr_starting_turn.end - curr_starting_turn.start
            # print('new speaker, updated tracked turn>>',curr_starting_turn)
            compressed_turns.append(curr_starting_turn)
            curr_starting_turn = turn
    compressed_turns.append(curr_starting_turn)
    return compressed_turns

#get sorted array of segments from dict
def segments_from_json(segments_array):
    records = []
    # print('segarray',segments_array)
    for segment_dict in segments_array:
        # print('segdict',segment_dict)
        records.append(
            Segment(
                segment_dict['id'],
                segment_dict['start'],
                segment_dict['end'],
                segment_dict['seek'],
                segment_dict['text']
            )
        )
    return records

class Segment:
    def __init__(self,id,start,end,seek,text):
        self.id = id
        self.start = start
        self.end = end
        self.seek = seek*.01
        self.text = text
        # if seek>0:
        #     seek = seek/100

        # self.offstart = start+seek
        # self.offstop = start+seek
    
    def __str__(self):
        return f"SEGMENT[{self.id}]||{self.start}->{self.end} (seek={self.seek}) == {self.text}"

class RTTM_Turn(object):
    """Speaker turn class.
    A turn represents a segment of audio attributed to a single speaker.
    Parameters
    ----------
    onset : float
        Onset of turn in seconds from beginning of recording.
    offset : float, optional
        Offset of turn in seconds from beginning of recording. If None, then
        computed from ``onset`` and ``dur``.
        (Default: None)
    dur : float, optional
        Duration of turn in seconds. If None, then computed from ``onset`` and
        ``offset``.
        (Default: None)
    speaker_id : str, optional
        Speaker id.
        (Default: None)
    file_id : str, optional
        File id.
        (Default: none)
    """
    def __init__(self, start, end=None, dur=None, speaker_id=None,
                file_id=None, channel_id=None):
        if not xor(end is None, dur is None):
            raise ValueError('Exactly one of offset or dur must be given')
        if start < 0:
            raise ValueError('Turn onset must be >= 0 seconds')
        if end:
            dur = end - start
        if dur <= 0:
            raise ValueError('Turn duration must be > 0 seconds')
        if not end:
            end = start + dur
        self.start = start
        self.end = end
        self.dur = dur
        self.speaker_id = speaker_id
        self.file_id = file_id
        self.channel_id = channel_id

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.onset, self.offset, self.dur, self.file_id,
                    self.speaker_id))

    def __str__(self):
        return ('RTTM_TURN||SPEAKER: %s, START: %f, END: %f, DUR: %f' %
                (self.speaker_id, self.start, self.end,
                self.dur))

    def __repr__(self):
        speaker_id = ("'%s'" % self.speaker_id if self.speaker_id is not None
                    else None)
        file_id = ("'%s'" % self.file_id if self.file_id is not None
                else None)
        return ('Turn(%f, %f, None, %s, %s)' %
                (self.onset, self.offset, speaker_id, file_id))

def combine_segments_rttm(episode_tagged_transcript_file,segment_records,rttm_turns):
    
    track_turns = 0
    track_segments = 0

    with open(episode_tagged_transcript_file,'w',encoding="UTF-8") as outfl:
        curr_speaker = rttm_turns[0].speaker_id
        curr_message = segment_records[0].text
        curr_start = 0
        curr_end = segment_records[0].end
        curr_seek = segment_records[0].seek

        #save first text for off-by-one errors
        # curr_message += segment_records[0].text

        #O(n^2) for now but oh well
        #loop all segments of extracted dialog and tag which speaker is occuring at that time segment
        for segment in segment_records:
            curr_seek = segment.seek

            # print('looping segment',segment)
            #loop all rttm speaker timestamps to find out who is speaking now
            for rttm_turn in rttm_turns:
                #if the 
                # if rttm_turn.start>=curr_seek and rttm_turn.end<=segment.end:
                if segment.start>=rttm_turn.start and segment.end<=rttm_turn.end:
                    #track rttm turns we've used
                    track_turns+=1

                    #new speaker, so save what the last speaker just said
                    if rttm_turn.speaker_id != curr_speaker:
                        tmp_line = f"{curr_start:.2f} {segment.end:.2f} {curr_speaker} {curr_message}\n"
                        # print('#'*20,'writing message to file','#'*20)
                        # print(tmp_line)
                        # print('#'*50)
                        outfl.write(tmp_line)
                        curr_message = ""
                        curr_start = segment.start

                    curr_speaker = rttm_turn.speaker_id
                    curr_message += segment.text
                    curr_end = segment.end
                    # print('found rttm turn within segment boundaries',rttm_turn)
                    # print('current message',curr_message)
                    break
        
        #adding final text & writing last message to file
        curr_message += segment_records[-1].text
        outfl.write(f"{curr_start:.2f} {curr_end:.2f} {curr_speaker} {curr_message}\n")
    print(f'utilized {track_turns} out of {len(rttm_turns)} turns')