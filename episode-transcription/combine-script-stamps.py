
#script to combine the transcription output with the diarization output for fully timestamped speaker labelled transcript

from utils import *

from pyannote.core import Annotation, Timeline

#Segment=
#Annotation=
#Timeline=

from utils import *
import os, json

transcript_folder = 'transcriptions-json'
diarize_folder = 'diarizations-rttm'
tagged_output_path = "speaker-tagged-transcriptions"

#loop all transcriptions files
for episode_json_file in os.listdir(transcript_folder):
    episode_name = episode_json_file.split('.')
    if len(episode_name)>2:
        episode_name = '.'.join(episode_name[:-1])
    else:
        episode_name = episode_name[0]
    
    episode_tagged_transcript_file = os.path.join(tagged_output_path,f"{episode_name}.txt")
    #skip this episode if the combined file already exists
    if os.path.exists(episode_tagged_transcript_file):
        continue

    print('-'*40)
    print('-'*40)
    print('working on episode: ',episode_name)
    episode_json_file = f"{episode_name}.json"

    #read episode json transcription into memory
    episode_json = {}
    with open(os.path.join(transcript_folder,episode_json_file),'r') as tfile:
        episode_json = json.loads(tfile.read())

    #create custom pyannote segments from json information
    sorted_segment_dicts = sorted(episode_json['segments'], key=lambda d: d['start'])
    segment_records = segments_from_json(sorted_segment_dicts)

    #read episode rttm diarization into memory
    episode_rttm_file = f"{episode_name}.rttm"
    #rttm_turns:list(Turn), rttm_speakers, rttm_file_ids
    rttm_turns, rttm_speakers, rttm_file_ids = load_rttm(os.path.join(diarize_folder,episode_rttm_file))

    print('unique channels found',len(set([x.channel_id for x in rttm_turns])))

    #compress rttm turns for when the same speaker does multiple turns in a row
    turns_before = len(rttm_turns)
    rttm_turns = compress_rttm_turns(rttm_turns)
    print(f'compressed rttm turns from {turns_before} to {len(rttm_turns)}')

    #combine segments and rttm speaker tags and write to file
    combine_segments_rttm(episode_tagged_transcript_file,segment_records,rttm_turns)

#Annotation object: https://pyannote.github.io/pyannote-core/reference.html#annotation
