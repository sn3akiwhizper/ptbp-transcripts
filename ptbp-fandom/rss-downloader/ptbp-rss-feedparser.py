#ptbp-rss-feedparser.py
#sn3akiwhizper
#to easily list episode information from the episode rss feed

import feedparser
import sys, os
from datetime import datetime

PTBP_FEED_URL="https://pinecast.com/feed/pretending-to-be-people"
LOCAL_DETAILS_FOLDER="rss-feed-downloads"
LOCAL_DETAILS_FILE="local_rss_details"
CSV_SEPERATOR="||"#to deal with any weirdness with quotes and commas

def main():
    '''
    Main function to perform the argument parsing and redirect control to the appropriate functions
    '''
    this_feed = feedparser.parse(PTBP_FEED_URL)
    # print(this_feed.entries[0])
    current_date = datetime.now().strftime("%m-%d-%y")
    with open(
        os.path.join(
            LOCAL_DETAILS_FOLDER,
            f"{LOCAL_DETAILS_FILE}-{current_date}.csv"
        ),'w') as outfile:
        outfile.write(CSV_SEPERATOR.join(['id','published_date','published_date_struct','title','duration','description','link\n']))
        for entry in this_feed.entries:
            episode_duration = entry.get("itunes_duration","n/a")
            clean_summary = entry.summary.replace("\n","<br>")
            outfile.write(
                CSV_SEPERATOR.join([entry.id,entry.published,str(entry.published_parsed),entry.title,episode_duration,clean_summary,entry.link])+"\n"
            )
        print(f'wrote {len(this_feed.entries)} entries')

if __name__=="__main__":
    main()

# example episode entry
# $ python ptbp-rss-feedparser.py update
# {
# 	'title': 'S1E1 - Blunt Force Trauma', 
# 	'title_detail': {
# 		'type': 'text/plain', 
# 		'language': None, 
# 		'base': 'https: //pinecast.com/feed/pretending-to-be-people', 
# 		'value': 'S1E1 - Blunt Force Trauma'
# 	}, 
# 	'id': 'https://pinecast.com/guid/5a59133a-050b-4d37-b564-4aadcdf931b3',
# 	'guidislink': False, 
# 	'published': 'Mon, 19 Nov 2018 05:40:04 -0000', 
# 	'published_parsed': time.struct_time(tm_year=2018, tm_mon=11, tm_mday=19, tm_hour=5, tm_min=40, tm_sec=4, tm_wday=0, tm_yday=323, tm_isdst=0), 
# 	'itunes_duration': '01: 10: 23', 
# 	'links': [
# 			{
# 				'rel': 'alternate', 
# 				'type': 'text/html', 
# 				'href': 'http: //pretendingpod.com/episode/5a59133a050b4d37/blunt-force-trauma'
# 			}, {
# 				'length': '85880804', 
# 				'type': 'audio/mpeg', 
# 				'href': 'https://pinecast.com/listen/5a59133a-050b-4d37-b564-4aadcdf931b3.mp3?source=rss&aid=dbca8f86-3f5b-43a4-88e7-989cc85b6aac.mp3', 'rel': 'enclosure'
# 			}
# 	], 
# 	'link': 'http://pretendingpod.com/episode/5a59133a050b4d37/blunt-force-trauma', 
# 	'summary': '<p>Pants are worn. Birthdays are forgotten. Faces are smashed. </p>\n<p>Support the show on <a href="https://www.patreon.com/pretendingpod" rel="nofollow">Patreon</a>.</p>\n<p>Follow along on <a href="https://www.instagram.com/pretendingpod/" rel="nofollow">Instagram</a>, <a href="https://twitter.com/PretendingPod" rel="nofollow">Twitter</a>, and <a href="https://www.facebook.com/PretendingPod/" rel="nofollow">Facebook</a>.</p>\n<p>Find other listeners on <a href="https://discord.com/invite/ejuQSSw" rel="nofollow">Discord</a> and <a href="https://www.reddit.com/r/PretendingToBePeople/" rel="nofollow">Reddit</a>.</p>\n<p><a href="https://www.youtube.com/playlist?list=PLAfSa2b8HXoAO8yr9bEwTvncXxhqhZ0SL" rel="nofollow">Soundtrack</a> by Justin Sala.</p>\n<p>Wolf played "<a href="https://www.youtube.com/watch?v=8WDKCDNmn_I&amp;t=90s" rel="nofollow">No Backbone</a>" by <a href="https: //kudzukudzukudzu.bandcamp.com/" rel="nofollow">Kudzu</a>. </p>\n<p>Published by arrangement with the Delta Green Partnership. The intellectual property known as Delta Green is a trademark and copyright owned by the Delta Green Partnership, who has licensed its use here. The contents of this document are ©Pretending Productions, excepting those elements that are components of the Delta Green intellectual property.</p>', 
# 	'summary_detail': {
# 		'type': 'text/html', 
# 		'language': None, 
# 		'base': 'https: //pinecast.com/feed/pretending-to-be-people', 
# 		'value': '<p>Pants are worn. Birthdays are forgotten. Faces are smashed. </p>\n<p>Support the show on <a href="https://www.patreon.com/pretendingpod" rel="nofollow">Patreon</a>.</p>\n<p>Follow along on <a href="https://www.instagram.com/pretendingpod/" rel="nofollow">Instagram</a>, <a href="https://twitter.com/PretendingPod" rel="nofollow">Twitter</a>, and <a href="https://www.facebook.com/PretendingPod/" rel="nofollow">Facebook</a>.</p>\n<p>Find other listeners on <a href="https://discord.com/invite/ejuQSSw" rel="nofollow">Discord</a> and <a href="https://www.reddit.com/r/PretendingToBePeople/" rel="nofollow">Reddit</a>.</p>\n<p><a href="https://www.youtube.com/playlist?list=PLAfSa2b8HXoAO8yr9bEwTvncXxhqhZ0SL" rel="nofollow">Soundtrack</a> by Justin Sala.</p>\n<p>Wolf played "<a href="https://www.youtube.com/watch?v=8WDKCDNmn_I&amp;t=90s" rel="nofollow">No Backbone</a>" by <a href="https://kudzukudzukudzu.bandcamp.com/" rel="nofollow">Kudzu</a>. </p>\n<p>Published by arrangement with the Delta Green Partnership. The intellectual property known as Delta Green is a trademark and copyright owned by the Delta Green Partnership, who has licensed its use here. The contents of this document are ©Pretending Productions, excepting those elements that are components of the Delta Green intellectual property.</p>'
# 	}, 
# 	'itunes_title': 'Blunt Force Trauma', 
# 	'itunes_explicit': True, 
# 	'itunes_season': '1', 
# 	'itunes_episode': '1'
# }

# feedrss docs: <https://feedparser.readthedocs.io/en/latest/common-rss-elements.html>
