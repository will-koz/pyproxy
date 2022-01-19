# Pyproxy

A Python implementation of a MTG (or any card game, with a bit of tinkering) Proxy PDF creator.

![PyProxy Logo](pyrpoxy_logo.png)

## Installation

`git clone` this repository, and run with `python3 main.py`. It defaults to running with conf.json, but you can change the configuration by running `python3 main.py conf2.json`, or whatever your configuration file is called.

## Images Used

In the demomonstration deck, demo.txt, two files I did not create are explicitly:

- [Mountain](https://c1.scryfall.com/file/scryfall-cards/large/front/3/b/3ba24a61-e529-4490-8536-6276ea77c511.jpg?1637115137)
- [Negate](https://i.pinimg.com/originals/ba/e4/e5/bae4e5787efedb0e7ffdcaa66bf0de3b.png)

But of course, credit goes to the artists of all of the cards, Wizards of the Coast, and Scryfall.com.

## TODO List

- [x] Add delay to API Requests
- [x] Load images
- [x] Create PDFs with Pillow
- [x] Export PDFs
- [ ] Add CLI Options / Clean Up Code / Add Comments

## Logo Credits

The Logo uses parts from these images:

- [Python Logo](https://commons.wikimedia.org/wiki/File:Python-logo-notext.svg)
- [MTG Blog](https://magic.wizards.com/en/articles/archive/news/venturing-outward-new-magic-logo-2018-03-27)
