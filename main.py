import os
import subprocess
import sys
import json

# Global path to mkvmerge
sw_path = r"C:\Program Files\MKVToolNix\mkvmerge.exe"


def identify_and_parse_tracks(file_path):
    cmd = [sw_path, "--identify", "--identification-format", "json", file_path]

    last_audio_track_id = None
    last_english_subtitle_track_id = None

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', check=True)
        track_info = json.loads(result.stdout)

        print(f"Track information for {file_path}:")

        for track in track_info.get('tracks', []):
            track_id = track.get('id', 'N/A')
            track_lang = track['properties'].get('language_ietf', track['properties'].get('language', 'und'))
            track_type = track['type']

            print(f"  - Track ID: {track_id}, Type: {track_type}, Language: {track_lang}")

            if track_type == 'audio' and 'en' in track_lang:
                last_audio_track_id = track_id
            if track_type == 'subtitles' and 'en' in track_lang:
                last_english_subtitle_track_id = track_id



    except subprocess.CalledProcessError as e:
        print(f"Error while identifying tracks: {e}")

    return last_audio_track_id, last_english_subtitle_track_id


def remove_subtitles_and_audio(input_path, output_path, sub_to_keep, audio_to_keep):
    cmd = [
        sw_path,
        "-o", output_path,
        "--audio-tracks", f"{audio_to_keep}",
        "--subtitle-tracks", f"{sub_to_keep}",
        input_path
    ]

    try:
        subprocess.run(cmd, check=True)
        print(
            f"Processed {os.path.basename(input_path)}: kept audio track {audio_to_keep} and subtitle track {sub_to_keep}, saved to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing {os.path.basename(input_path)}: {e}")


def process_files(input_folder, output_folder, manual, audio_track_to_keep, subtitle_track_to_keep):
    output_changed_folder = os.path.join(input_folder, output_folder)
    if not os.path.exists(output_changed_folder):
        os.makedirs(output_changed_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".avi", ".mkv", ".mp4", ".m4v")):
            input_path = os.path.join(str(input_folder), str(filename))
            output_path = os.path.join(str(output_changed_folder), str(filename))

            if not manual:
                audio_track_to_keep, subtitle_track_to_keep = identify_and_parse_tracks(input_path)
                print(f"I will keep Track ID: {audio_track_to_keep} for audio and {subtitle_track_to_keep} for subs")
            else:
                identify_and_parse_tracks(input_path)

            if audio_track_to_keep and subtitle_track_to_keep:
                remove_subtitles_and_audio(input_path, output_path, str(subtitle_track_to_keep),
                                           str(audio_track_to_keep))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: script.py <input_folder>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = "output_folder"
    manual = False  # Set to True if you want to manually specify tracks
    audio_track_to_keep = 1  # This will be used if manual is True
    subtitle_track_to_keep = 1  # This will be used if manual is True

    process_files(input_folder, output_folder, manual, audio_track_to_keep, subtitle_track_to_keep)
