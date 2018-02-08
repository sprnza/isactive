__WARNING! The project in beta!__
# Isactive
This [beets](http://beets.io/) plugin is supposed to be used with a third party service like [album-info.ru](http://beets.io/)(ru) notifies you about new releases of you favourite artists. 

# How it works
1. It dumps your DB before import command
1. After the import command it gets what artists have been added
1. Check LastFM for the data regarding the artist activity (at this point most of errors occurs because not all artists have info like (1999-present) on their wikipage).
1. Acts accordingly with found information and (optionally) saves artists' names in the configured files
1. Returns a list of artist you can add to a release tracking service
1. Returns a list of artist failed to obtain information with respective URL, so you can check them manually.

# Installation
Just clone the repo and put the `isactive.py` to your beetsplugin directory. Normally it's `/usr/lib/pythonN.N/site-packages/beetsplugin`. And add `isactive` in `plugins:` string of your config.

# Configuration
Add `isactive` section in your config.yaml. Currently supported options:

```
   isactive:
      auto:
      lastfmkey:
      lasfmsecret:
      dest:
          alive:
          failed:
          dead:
```

`auto` - default to `no`. Isactive will ask if you want to start checking process.  
`lastfmkey` and `lasfmsecret`: get them [here](https://www.last.fm/api/account/create). It won't work without ones.  
`dest:`  
    `alive`: file to save names of alive artists  
    `failed`: file to save names of artists failed to be processed.  
    `dead`: file to save names of dead artists  

# TODO
1. Check mandatory options missing.
1. Debug the overall workflow.
1. Fix custom prompt choices.
1. Ask (album-info.ru)[http://album-info.ru] owners to have an API implemented.
.

