<div align="center">
<pre>                                                                    
                                    ,,           ,,    ,,                  
`7MMM.     ,MMF'                    db         `7MM    db            mm    
  MMMb    dPMM                                   MM                  MM    
  M YM   ,M MM  ,pW"Wq.`7M'   `MF'`7MM  .gP"Ya   MM  `7MM  ,pP"Ybd mmMMmm  
  M  Mb  M' MM 6W'   `Wb VA   ,V    MM ,M'   Yb  MM    MM  8I   `"   MM    
  M  YM.P'  MM 8M     M8  VA ,V     MM 8M""""""  MM    MM  `YMMMa.   MM    
  M  `YM'   MM YA.   ,A9   VVV      MM YM.    ,  MM    MM  L.   I8   MM    
.JML. `'  .JMML.`Ybmd9'     W     .JMML.`Mbmmd'.JMML..JMML.M9mmmP'   `Mbmo 
</pre>
</div>

# Movielist

A lightweight CLI tool to search and manage movies and TV series using the TMDB API.                                                        
                                                                           
## Features

- **Search** movies and TV shows via TMDB
- **Local library** to save titles, mark them as watched or not, and add your own notes

## Requirements

- Python 3.12+ (only needed if using pip/uv install or development)
- A free [TMDB API Read Access Token](SETUP.md)

## Installation

### Option 1: Download the executable (recommended for most people)

Grab the latest `.exe`, `.app`, or Linux binary from the [Releases](https://github.com/dhanaan/Movielist/releases) page.

### Option 2: Install as a package

```bash
pip install git+https://github.com/dhanaan/Movielist
```

or with `uv`:

```bash
uv tool install git+https://github.com/dhanaan/Movielist
```

### Option 3: Run from source (development)

```bash
git clone https://github.com/dhanaan/Movielist
cd Movielist
uv run movielist
```

## Roadmap

- [x] ~~**Handle HTTP errors gracefully** instead of crashing (priority)~~
- [x] ~~Add color & style to the terminal output~~
- [x] ~~Settings menu, including:~~
  - [x] ~~Reset/Change API key~~
- [ ] Update in-library movie/show data (refetch)
- [ ] View your library even without authentication or an internet connection
- [x] ~~Add notes to movies/shows~~
- [x] ~~Show 5 search results per query (instead of 20)~~
- [x] ~~Bundle the project with PyInstaller into `.exe`, `.app`, and a Linux binary, with GitHub Actions to build them automatically~~

## Contributing

Issues and PRs are welcome!

## License

[MIT](LICENSE)