```text
.
├── .streamlit/              <- Streamlit folder
│   └── config.toml          <- Streamlit configuration
├── assets/                  <- Static assets
│   ├── images/              <- Images
│   │   └── logo.png         <- Application logo
│   └── styles/              <- Custom CSS styles
│       ├── chat.css         <- Style for the chat page
│       ├── preprocess.css   <- Style for the preprocess page
│       └── upload.css       <- Style for the upload page
├── benchmarks               <- Performance benchmarking
│   ├── const.py             <- Constants for benchmarking
│   ├── pdf_urls.json        <- PDFs to benchmark
│   └── preprocessing        <- Preprocessing pipeline benchmark
│       ├── run_benchmark.py <- Script to run the preprocessing benchmark
│       └── report.json      <- Preprocessing pipeline benchmark report
├── LICENSE                  <- License defining project usage rights
├── Makefile                 <- Automation commands
├── PROJECT_STRUCTURE.md     <- Project structure overview (this file)
├── README.md                <- Project overview
├── pyproject.toml           <- Project configuration, dependencies, and build settings
├── .gitignore               <- Files/folders ignored by Git
├── .pre-commit-config.yaml  <- Pre-commit hooks configuration
└── src/                     <- Source code
    ├── app.py               <- Entry point and page navigation
    ├── chat.py              <- Document conversational analysis
    ├── config.py            <- Project configuration
    ├── const.py             <- Global constants
    ├── preprocess.py        <- Document preprocessing
    └── upload.py            <- Document uploading
```
