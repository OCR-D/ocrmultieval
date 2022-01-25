# ocrmultieval

> Proof-of-concept for extensible evaluation of (intermediate) results of an OCR workflow

## Installation

```
make deps install
```

## Architecture

All evaluation functionality is provided by *backends*.

Every backend inherits from [`EvalBackend`](ocrmultieval/backend.py) and must
implement a `compare_files` method, that accepts paths to and media types of
the Ground Truth and detection results, does the actual evaluation and returns
an [`EvalReport`](ocrmultieval/report.py).

An `EvalReport` is a map of metrics to their resp. value and can be serialized
as JSON or CSV for further processing/analysis.

The glue code for running the backends is in
[`ocrmultieval.runner.py`](ocrmultieval/runner.py).

## Usage

### CLI

The `ocrmultieval compare` command line tool allows evaluating individual pages of GT
and detection with any of the available [backends](#backends).

```
Usage: ocrmultieval compare [OPTIONS] {dinglehopper|ocrevalUAtion|PrimaTextEva
                            l|CorAsvAnnEval} GT_FILE OCR_FILE

Options:
  --gt-mediatype TEXT
  --ocr-mediatype TEXT
  --format [csv|json]
  --help                Show this message and exit.
```

### OCR-D processor

The `ocrd-ocrmultieval` command line tool implments the [OCR-D processor
API](https://ocr-d.de/en/spec/cli) and can be used to process complete
workspaces.

```
Usage: ocrd-ocrmultieval [OPTIONS]

  Evaluate

  > Eval processor

Options:
  -I, --input-file-grp USE        File group(s) used as input
  -O, --output-file-grp USE       File group(s) used as output
  -g, --page-id ID                Physical page ID(s) to process
  --overwrite                     Remove existing output pages/images
                                  (with --page-id, remove only those)
  -p, --parameter JSON-PATH       Parameters, either verbatim JSON string
                                  or JSON file path
  -P, --param-override KEY VAL    Override a single JSON object key-value pair,
                                  taking precedence over --parameter
  -m, --mets URL-PATH             URL or file path of METS to process
  -w, --working-dir PATH          Working directory of local workspace
  -l, --log-level [OFF|ERROR|WARN|INFO|DEBUG|TRACE]
                                  Log level
  -C, --show-resource RESNAME     Dump the content of processor resource RESNAME
  -L, --list-resources            List names of processor resources
  -J, --dump-json                 Dump tool description as JSON and exit
  -h, --help                      This help message
  -V, --version                   Show version

Parameters:
   "backend" [string - "PrimaTextEval"]
    Backend to use
    Possible values: ["PrimaTextEval", "ocrevalUAtion", "dinglehopper"]
   "format" [string - "csv"]
    Output format
    Possible values: ["csv", "json"]
   "config" [object]
    Configuration to override default

Default Wiring:
  ['GT,OCR1'] -> ['GT_VS_OCR1']
```
