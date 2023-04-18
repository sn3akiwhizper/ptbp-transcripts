
from jinja2 import Environment, FileSystemLoader
import csv

environment = Environment(loader=FileSystemLoader("jinja-templates/"))
template = environment.get_template("episode_table_row.txt")

episodes = []
with open('ptbp-generator-episode-guide.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        print(', '.join(row))
        episodes.append({
            "episode_id":row[0],
            "season_episode_number":f"S{row[1]}E{row[2]}",
            "episode_wiki_page":row[5],
            "episode_title_clean":row[4],
            "episode_release_date":row[6],
            "itunes_link":row[13],
            "spotify_link":row[12],
            "transcript_link":f"Transcript:S{row[1]}E{row[2]}",
            "episode_description":row[11],
            }
        )

generated_row_content = []

for episode in episodes:
    generated_row_content.append(
        template.render(
            episode
        )
    )

with open("rendered_episode_rows.txt", mode="w", encoding="utf-8") as message:
    for row in generated_row_content:
        message.write(row+"\n")
