# Transcription & Diarization Process

- [Transcription](#transcription)
	- [Windows](#windows)
	- [Linux/Mac Bash](#linuxmac-bash)
- [Diarization](#diarization)
	- [Windows](#windows-1)
	- [Linux/Bash](#linuxbash)
- [Transcription/Diarization Combo](#transcriptiondiarization-combo)
- [File Type Reference](#file-type-reference)

## Transcription

This project uses the [OpenAI/whisper](https://huggingface.co/openai/whisper-base) model and its accompanying [whisper](https://github.com/openai/whisper) python library to perform speech recognition on episodes of the podcast. This speech recognition converts the audio to text and saves the results to different output file formats. What follows are the instructions for setting up an environment to perform the transcription on your own system. These steps assume that Python is installed on your system along with the conda package manager.

```bash
#create a new conda environment
conda create -n ptbp-transcription python=3.8

#activate the new environment
conda activate ptbp-transcription

#install a specific version of pytorch and the cuda toolkit to run on GPU
conda install pytorch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 cudatoolkit=11.3 -c pytorch -c nvidia

#install special audio processing libraries 
conda install -c conda-forge hmmlearn libsndfile

#install main python libraries stored in requirements file
pip install -r _code/requirements.txt

#test installation
whisper --help
diart.stream --help
```

After installing all of this, we should now be able to run OpenAI's `whisper` command from the terminal running our conda environment. Download the podcast episodes, I use [gpodder](https://gpodder.github.io/) to download my favorites. The following commands show how to transcribe a single episode or the entire folder, on both Windows and Linux/Mac type of bash terminals.

Command options explanation:

- `--model medium.en` Use the medium sized english model, see [full list here](https://huggingface.co/openai)
- `--language en` The podcast is english, so specify english to prevent the model performing auto-detection
- `--device cuda` Run on GPU, much faster than on CPU
- `--output_dir "A:\PTBP_Episodes\transcriptions"` Define where transcription files are written to
- `--output_format all` Output all types of transcript files, options are "txt", "json", "tsv", "srt", "vtt", "all"
- `--task transcribe` Tell the model to transcribe instead of generating audio

### Windows

For these examples the folder containing the episodes is located at `A:\PTBP_Episodes\`

Transcribe single episode:

```cmd
whisper --model medium.en --language en --device cuda --output_dir "A:\PTBP_Episodes\transcriptions" --output_format all --task transcribe "A:PTBP_Episodes\BUSH1mix.mp3"
```

Transcribe entire folder:

```cmd
for /f %f in ('dir /b "A:\PTBP_Episodes"') do whisper --model medium.en --language en --device cuda --output_dir "A:\PTBP_Episodes\transcriptions" --output_format all --task transcribe "A:PTBP_Episodes\%f"
```

### Linux/Mac Bash

For these examples the folder containing the episodes is located at `/tmp/PTBP_Episodes`

Transcribe single episode:

```bash
whisper --model medium.en --language en --device cuda --output_dir "/home/user/PTBP_Episodes/transcriptions" --output_format all --task transcribe "/home/user/PTBP_Episodes/BUSH1mix.mp3"
```

Transcribe entire folder:

```bash
for FILE in $(ls /home/user/PTBP_Episodes); do whisper --model medium.en --language en --device cuda --output_dir "/home/user/PTBP_Episodes/transcriptions" --output_format all --task transcribe "/home/user/PTBP_Episodes/$FILE"
```

## Diarization

The [pyannote](https://huggingface.co/pyannote) library provides the capability for doing speaker recognition which would allow for tagging the transcript text with a specific speaker. I've been trying to work with this [pyannote-whisper](https://github.com/yinruiqing/pyannote-whisper) project for this task. However, I haven't figured out how to get this working in a manner that doesn't require 20+ hours to analyze a single episode. If anyone has tips on this I'm all ears, otherwise we'll need to manually do speaker tagging unfortunately.

To run this model you will need a huggingface account, accept the TOS for this model, and generate an API key to use. WARNING: there is a lot of telemetry associated with this python package so if you're concerned about privacy you'll need to do some digging into the source to see what they send.

Command options explanation:

- `--max-speaker 7` Define the max number of speakers for the model to attempt to distinguish, defaults to 20 but *might* speed up the process by selecting number closer to the actual number of speakers
- `--output folder_path` where to save the diarization output file
- `--hf-token YOUR_TOKEN` Huggingface API token that allows you to access the pyannote model after accepting their TOS
- `--no-plot` don't display the plot. The plot significantly slows down the diarization, but is cool to look at the first couple of times running
- `--cpu` This process defaults to GPU, so if you need to run on CPU only then use this option

### Windows

```cmd
diart.stream "A:\PTBP_Episodes\transcriptions\BUSH1mix.mp3" --max-speakers 7 --output "A:\PTBP_Episodes\diarized_output" --no-plot --hf-token <YOUR_TOKEN>
```

### Linux/Bash

```bash
diart.stream "/home/user/PTBP_Episodes/transcriptions/BUSH1mix.mp3" --max-speakers 7 --no-plot --output "/home/user/PTBP_Episodes/diarized_output" --hf-token <YOUR_TOKEN>
```

## Transcription/Diarization Combo

This part isn't very well solved yet.

Runing `python _code\combine-script-stamps.py` will attempt to combine the Whisper JSON transcripts with the Pyannote RTTM diarizations to get speaker tagged transcripts in `speaker-tagged-transcriptions/`. The process isn't perfect and I haven't validated that it combines all the text in a perfect way, so use caution when using files in that output folder. If you can improve that script please do and open a Pull Request with your changes, that would be greatly appreciated.

## File Type Reference

JSON format

```json
{
	"text":"all text from the episode stored in here, usually very big",
	"segments":[
		{
			"id": 0,
			"seek": 0,
			"start": 0.0,
			"end": 2.0,
			"text": " What's snazzy, my pips?",
			"tokens": [
				50363,
				1867,
				338,
				3013,
				1031,
				7357,
				11,
				616,
				279,
				2419,
				30,
				50463
			],
			"temperature": 0.0,
			"avg_logprob": -0.2453594207763672,
			"compression_ratio": 1.4508928571428572,
			"no_speech_prob": 0.04931340366601944
		},
	],
	"language":"end"
}
```

SRT format

```srt
1
00:00:00,000 --> 00:00:02,000
What's snazzy, my pips?
```

TSV format (tab separated values)

```tsv
start	end	text
0	2000	What's snazzy, my pips?
```

VTT format

```vtt
WEBVTT

00:00.000 --> 00:02.000
What's snazzy, my pips?
```

TXT format

```txt
What's snazzy, my pips?
```

RTTM format

```rttm
#speaker_tag filename channel_id onset duration orthography speaker_type speaker_name confidence signal_lookahead
SPEAKER Bonus.BleakProspect.1.Mix.Smol2 1 0.230 73.178 <NA> <NA> speaker0 <NA> <NA>
```
