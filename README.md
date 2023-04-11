# Pretending To Be People Transcripts

AI-generated transcripts for the Pretending to Be People podcast, stay greasy Wolf 🐺. Made for fans by fans to help with accessibility and the [wiki](https://pretending-to-be-people.fandom.com/f).

Transcript files have been sorted into folders in this repo by the format of the output transcription: json, srt, tsv, vtt, and txt.

**Most Recent Episode Transcription:** Currently performing bulk catchup.

Note! This project does not contain the transcripts for the Patreon-only episodes, [go support them](https://www.patreon.com/pretendingpod/posts) and generate them for yourselves you filthy animals.

## Intellectual Property Notice

All the code in this project was integrated by sn3akiwhizper using examples from other leaders in the areas of using AI for audio forms of data. Besides that, all content is the intellectual property of the Pretending to Be People crew. We make no claims of ownership over the amazing stories that they tell. This project is solely for increasing the accessibility and reach of the podcast so they may continue bringing us entertainment to the holes of our ears. And now the obligitory disclaimer that Delta Green is the intellectual property of Arc Dream Publishing, the PTBP folks have received permission from Arc Dream for their podcast (this project has not contacted or been contacted by Arc Dream or PTBP, if they have a problem they can find me on Twitter or Discord).

## Process

### Transcription

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
pip install -r requirements.txt

#test installation
whisper --help
```

After installing all of this, we should now be able to run OpenAI's `whisper` command from the terminal running our conda environment. Download the podcast episodes, I use [gpodder](https://gpodder.github.io/) to download my favorites. The following commands show how to transcribe a single episode or the entire folder, on both Windows and Linux/Mac type of bash terminals.

Command options explanation:

- `--model medium.en` Use the medium sized english model, see [full list here](https://huggingface.co/openai)
- `--language en` The podcast is english, so specify english to prevent the model performing auto-detection
- `--output_dir "A:\PTBP_Episodes\transcriptions"` Define where transcription files are written to
- `--output_format all` Output all types of transcript files, options are "txt", "json", "tsv", "srt", "vtt", "all"
- `--task transcribe` Tell the model to transcribe instead of generating audio

#### Windows

For these examples the folder containing the episodes is located at `A:\PTBP_Episodes\`

Transcribe single episode:

```cmd
whisper --model medium.en --language en --output_dir "A:\PTBP_Episodes\transcriptions" --output_format all --task transcribe "A:PTBP_Episodes\BUSH1mix.mp3"
```

Transcribe entire folder:

```cmd
for /f %f in ('dir /b "A:\PTBP_Episodes"') do whisper --model medium.en --language en --output_dir "A:\PTBP_Episodes\transcriptions" --output_format all --task transcribe "A:PTBP_Episodes\%f"
```

#### Linux/Mac Bash

For these examples the folder containing the episodes is located at `/tmp/PTBP_Episodes`

Transcribe single episode:

```bash
TODO
```

Transcribe entire folder:

```bash
TODO
```

### Diarization

The [pyannote](https://huggingface.co/pyannote) library provides the capability for doing speaker recognition which would allow for tagging the transcript text with a specific speaker. I've been trying to work with this [pyannote-whisper](https://github.com/yinruiqing/pyannote-whisper) project for this task. However, I haven't figured out how to get this working in a manner that doesn't require 20+ hours to analyze a single episode. If anyone has tips on this I'm all ears, otherwise we'll need to manually do speaker tagging unfortunately.

To run this model you will need a huggingface account, accept the TOS for this model, and generate an API key to use.

```bash
#download project code from repo (using git or straight from website)
git clone https://github.com/yinruiqing/pyannote-whisper

#install the requirements for this project, they are used in pyannote-whisper as well
pip install -r requirements.txt

#navigate into the project folder
cd pyannote-whisper/

#install the project
pip install .

#run the transcribe/diarize command
python -m pyannote_whisper.cli.transcribe "A:PTBP_Episodes\BUSH1mix.mp3" --model medium.en --diarization True --output_dir "A:PTBP_Episodes\diarized_output" --task transcribe --language en
```

## Future Work

- [ ] complete bulk catchup of transcription, diarization, combination to produce speaker-tagged transcripts
- [ ] parse speaker-tagged transcripts and validate each speaker's name
- [ ] upload scripts to automatically perform the transcription, diarization, and combination
- [ ] AI generated summaries of podcast episodes
- [ ] Transcript book (markdown -> epub, pdf, mobi) complete with AI illustrations
