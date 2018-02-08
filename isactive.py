""" Gets a list of imported artists and tryes to aquire information from lastfm if the artist still active or not"""
import pylast
from beets.plugins import BeetsPlugin
from beets import config
from bs4 import BeautifulSoup
import urllib.request
import os

API_KEY=config['isactive']['lastfmkey'].get()
API_SECRET=config['isactive']['lastfmsecret'].get()
new_artists=[]
alive=[]
dead=[]
failed=[]
iartists=set()
iseen=set()

def is_artist_alive(artist):
    last = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
    try:
        l_artist = last.get_artist_by_mbid(artist)
    except:
        return ["artist_not_found", artist]
    url = l_artist.get_url()
    if not url:
        return ["url_not_found", artist]
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    page = mybytes.decode("utf8")
    fp.close()
    soup = BeautifulSoup(page, 'html.parser')
    try:
        years = soup.find('p', {'class': 'factbox-summary'}).text
    except:
        return ["dates_not_found", artist, url]
    if years.find("present") > 0:
        return ["alive"]
    else:
        return ["dead"]

#### Plugin logic
class isactive(BeetsPlugin):
    def __init__(self):
        super(isactive, self).__init__()
        self.register_listener('library_opened', self.initialised)
        self.register_listener('import', self.imported)
        self.config['lastfmkey'].redact = True
        self.config['lastfmsecret'].redact = True

    def initialised(self, lib):
        for album in lib.albums():
            if album.albumartist not in iseen:
                iseen.add(album.albumartist)
                iartists.add(album.albumartist)

    def imported(self, lib, paths):
        for album in lib.albums():
            if album.albumartist not in iartists:
                new_artists.append((album.albumartist, album.mb_albumartistid))
        if len(new_artists) > 0:
            check_choise=""
            if self.config['auto'].get() == "no":
                while check_choise not in ['a', 'n']:
                    check_choise = input("\n\nIsactive plugin: \n"+str(len(new_artists))+" new artists found. Would you like to start is[a]ctive check or [n]ot? Default: a ") or 'a'
            if self.config['auto'] == "yes" or check_choise == 'a':
                print("\n\nIsactive plugin: checking just imported artists has started.")
                for artist in new_artists:
                    while True:
                        try:
                            res = is_artist_alive(artist[1])
                            print("Artist: "+artist[0]+" is "+res[0])
                        except:
                            continue
                        break
                if res[0] == "alive":
                    alive.append([artist[0]])
                elif res[0] == "dead":
                    dead.append([artist[0]])
                elif res[0] == "url_not_found":
                    failed.append([artist[0], "URL not found"])
                elif res[0] == "artist_not_found":
                    failed.append([artist[0], "Artist not found"])
                elif res[0] == "date_not_found":
                    failed.append([artist[0], "Dates not found", res[2]])
                
                df=""
                if len(alive) > 0:
                    if self.config["dest"]["alive"].exists():
                        dest_file=self.config["dest"]["alive"].get()
                        df = open(os.path.expanduser(af), "a")
                    else:
                        print("WARNING! A file for alive artists is not set! You'll loose the information once you close this window!")
                    print("It appears that these artists are active and could be tracked for new albums:")
                    for item in alive:
                        print(*item)
                        if df:
                            for item in alive:
                                df.write(*item)
                    if type(df) is not str:
                        df.close()

                if len(dead) > 0:
                    if self.config["dest"]["dead"].exists():
                        dest_file=self.config["dest"]["dead"].get()
                        df=open(os.path.expanduser(df), "a")
                    else:
                        print("WARNING! A file for dead artists is not set! You'll loose the information once you close this window!")
                    print("It appears that these artists are dead:")
                    for item in dead:
                        print(*item)
                        if df:
                            for item in dead:
                                df.write(*item)
                    if type(df) is not str:
                        df.close()

                if len(failed) > 0:
                    if self.config["dest"]["failed"].exists():
                        dest_file=self.config["dest"]["failed"].get()
                        df=open(os.path.expanduser(ff), "a")
                    else:
                        print("WARNING! A file for failed artists is not set! You'll loose the information once you close this window!")
                    print("Not possible to find current state for these artists, you will want to do it manually:")
                    for item in failed:
                        print(*item)
                        if df:
                            for item in failed:
                                df.write(*item)
                    if type(df) is not str:
                        df.close()
                print("Finished.")
            else:
                print("It's not a bad choice either!")
        else:
            print("Isacive plugin: no new artists have been found")


        
        
