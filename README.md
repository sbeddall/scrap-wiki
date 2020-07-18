# Scrap Wiki

**tl;dr** The lightest weight of lightweight wiki solutions. 

As a user, I got sick of coming up with wonky ways of making my scrap notes organizable/usable. OneNote didn't do it for me, and a lot of the solutions that I've seen don't really do what I want as far as simplicity.

ScrapWiki features:

- [x] Docs written in MARKDOWN. Needs to be SIMPLE DAMNIT!
- [x] Reference other markdown files via relative path. The path will be taken resolved for you.
- [x] Anything under `source/` will be built into the equivalent folder in `target/` as html.

Shit I want, so it'll get implemented:
- [ ] Custom Tagging
- [ ] Search files by tag
- [ ] Add git hook that runs a cred check to prevent accidental commit of secrets

# Invocation Instructions

1. `python -m pip install -r _internal/requirements.txt`
2. `python rebuilt.py`

Just gotta dust off my js.

Check the github.io for this project. Intent is to place documentation into the source folder for this repo to use as an example. 