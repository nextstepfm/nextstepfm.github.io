
import re
import xml.etree.ElementTree as ET 
import datetime
import os
import pprint
import time
import urllib.error
import urllib.request
from urllib.parse import urlparse
from pathlib import Path

# layout: podcast
# categories: podcast # podcast
# title: jekyll podcast sample
# author: sayo melu
# season: 2
# episode: 9
# episodeType: full # full | trailer | bonus
# explicit: false # true | false
# audio: https://feeds.soundcloud.com/stream/308137777-nextstepfm-003a.m4a
# length: 3927 # in seconds
# type: podcast
# starring: ["sonson_twit", "7gano", "k_katsumi"]

markdown_template = """---
layout: soundcloud
categories: podcast
title: %s
author: nextstep.fm
season: 1
episode: %d
episodeType: full
explicit: false
audio: %s
length: %s
type: podcast
link: %s
itunes_duration: %s
pubdate: %s
starring: [%s]
---

%s
"""

class Enclosure:
    def __init__(self):
        self.type = ""
        self.url = ""
        self.length = 0

class Item:
    def __init__(self):
        self.hosting = "soundcloud"
        self.title = "hoge"
        self.author = "nextstep.fm"
        self.starring = ["k_katsumi", "sonson_twit"]
        self.link = "podcast url"
        self.itunes_duration = "01:50:26"
        self.pubdate = "Thu, 08 Oct 2020 22:46:52 +0000"
        self.description = ""
        self.enclosure = None

    def __repr__(self):
        disp = ""
        disp = disp + self.description + "\n"
        disp = disp + self.pubdate + "\n"
        return disp
    
    def get_episode_number(self):
        try:
            pattern = "^\\#(\d+)"
            result = re.match(pattern, self.title)
            return int(result.group(1))
        except:
            return 0

    def get_description_for_markdown(self):
        return re.sub('(https?://[\w/:%#\$&\?\(\)~\.=\+\-]+)', r'[\1](\1)', self.description)

    def filename(self):
        date_dt = datetime.datetime.strptime(self.pubdate, '%a, %d %b %Y %H:%M:%S %z')
        return '%s-episode-%04d' % (date_dt.strftime('%Y-%m-%d'), self.get_episode_number())

    def get_title_removed_number(self):
        return re.sub(r'^#\d+\s*', "", self.title)

    def get_starring_array(self):
        return ','.join(self.starring)

    def output(self):
        
        # update starring member
        # start member
        case1 = [0, 1]
        # with special guest, tamadeveloper
        case2 = [18]
        # with 7gano
        case3 = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19]

        if self.get_episode_number() in case1:
            self.starring = ["7gano", "k_katsumi"]
        elif self.get_episode_number() in case2:
            self.starring = ["sonson_twit", "7gano", "k_katsumi", "tamadeveloper"]
        elif self.get_episode_number() in case3:
            self.starring = ["sonson_twit", "7gano", "k_katsumi"]

        data = (
            "'%s'" % self.get_title_removed_number(),
            self.get_episode_number(),
            self.enclosure.url,
            self.enclosure.length,
            self.link,
            self.itunes_duration,
            self.pubdate,
            self.get_starring_array(),
            self.get_description_for_markdown(),
        )
        return markdown_template % data

# /Users/sonson/Downloads/hoge/_posts/
def main(root, output_path=None):
    channel = list(filter(lambda x: x.tag == "channel", root))
    item_array = list(filter(lambda x: x.tag == "item", channel[0]))

    def map_item_2_class(item):
        new_item = Item()

        for entry in item:
            keys = ["title", "description", "pubDate", "link", "itunes:duration"]
            props = ["title", "description", "pubdate", "link", "itunes_duration"]
            prop_dict = {}
            for (key, prop) in zip(keys, props):
                prop_dict[key] = prop
                
            if entry.tag in keys:
                setattr(new_item, prop_dict[entry.tag], entry.text)

            if entry.tag == "enclosure":
                enclosure = Enclosure()
                for key in ["type", "url", "length"]:
                    setattr(enclosure, key, entry.attrib[key])
                new_item.enclosure = enclosure
        return new_item

    array = list(map(lambda x: map_item_2_class(x), item_array))

    if output_path != None:
        for a in array:
            path = "%s/%s.md" % (output_path, a.filename())
            with open(path, mode='w') as f:
                f.write(a.output())
    else:
        for a in array:
            print(a)

def download_audio_file(root, output_path=None):
    channel = list(filter(lambda x: x.tag == "channel", root))
    item_array = list(filter(lambda x: x.tag == "item", channel[0]))

    for item in item_array:
        titles = list(filter(lambda x: x.tag == "title", item))
        print(titles[0].text)
        candidates = list(filter(lambda x: x.tag == "enclosure", item))
        print(candidates[0].attrib['url'])

        url = candidates[0].attrib['url']

        file_name = titles[0].text
        suffix = Path(urlparse(url).path).suffix

        if output_path != None:
            destination_path = "%s/%s%s" % (output_path, file_name, suffix)
            print(destination_path)
            if not os.path.exists(destination_path):
                try:
                    with urllib.request.urlopen(url) as web_file:
                        data = web_file.read()
                        with open(destination_path, mode='wb') as local_file:
                            local_file.write(data)
                except urllib.error.URLError as e:
                    print(e)

url = "https://feeds.soundcloud.com/users/soundcloud:users:281879883/sounds.rss"

try:
    with urllib.request.urlopen(url) as web_file:
        data = web_file.read()
        tree = ET.fromstring(data)
        print(tree)
        # main(tree)
        download_audio_file(tree, output_path="/Users/sonson/Documents/podcast")
except urllib.error.URLError as e:
    print(e)