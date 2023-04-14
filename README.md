# BugOSS: A Regression Bug Benchmark for Evaluating Fuzzing Techniques

BugOSS is a benchmark of real-world regression bugs found in [OSS-Fuzz](https://github.com/google/oss-fuzz) for experimenting with regression fuzzing techniques. 
To reproduce the real project
context where the bugs were introduced, each study artifact of BugOSS indicates the exact bug-inducing commit, and provides the information about the target bug, together with the existing bugs in the same commit. Currently, 18 artifacts from 18 C/C++ programs are registered. 
These 18 bug artifacts encompass various cases of regression bugs in real-world. 
We belive that BugOSS offers a useful basis for empirically investigating regression fuzzing techniques.

## Citing BugOSS


    @INPROCEEDINGS{BugOSS,
         author={Kim, Jeewoong and Hong, Shin},
         booktitle={IEEE International Conference on Software Testing, Verification, and Validation (ICST)}, 
         title={{Poster}: {BugOSS}: A Regression Bug Benchmark for Evaluating Fuzzing Techniques}, 
         year={2023}
    }


## Bug artifact
Each artifact provides a realistic regression bug context to reproduce the reported failure: 
- fuzz target: the latest version before the oss-fuzz issue report time which successfully reproduce a failure
- bug-revealing input: an input for a fuzz target, that induces a failure (attached in an OSS-Fuzz issue)
- bug-inducing commit: the program change that newly adds the target bug to the target program
- fix-inducing commit: the program change that repairs the target bug
- failure symptom: failure type, crash message, or patterns of stack trace for the expected failure
- other failures by pre-existing bugs
- an initial seed corpus at a bug-inducing commit (`seed_corpus.tar`)
- experiment results with 2 baseline fuzzers (libFuzzer, AFL++) using the initial seed corpus


| artifact           | failure type     | changed lines in BIC | changed lines in FIC | 
| ------------------ | ---------------- | --------------------:| --------------------:|
| aspell-18462       | buffer-overrun   |               5      |               18     |
| curl-8000          | buffer-overrun   |              51      |                2     |
| exiv2-50315        | integer-overflow |              45      |                3     |
| file-30222         | null-dereference |              21      |               11     |
| gdal-47716         | buffer-overrun   |              10      |                4     |
| grok-28418         | memory-leak      |             101      |               55     |
| leptonica-25212    | null-dereference |              25      |               26     |
| libhtp-17198       | buffer-overrun   |              26      |               29     |
| libxml2-17737      | use-after-free   |              32      |                8     |
| ndpi-49057         | integer-overflow |              51      |               10     |
| openh264-26220     | buffer-overrun   |               7      |                5     |
| openssl-17715      | buffer-overrun   |              91      |               47     |
| pcapplusplus-23592 | buffer-overrun   |              32      |               13     |
| poppler-35789      | null-dereference |               3      |               20     |
| readstat-13262     | buffer-overrun   |               5      |               10     |
| usrsctp-18080      | use-after-free   |               6      |                8     |
| yara-38952         | buffer-overrun   |             277      |               17     |
| zstd-21970         | null-dereference |             280      |              247     |


## How to build an artifact
1. Clone the BugOSS reprository to your machine
   ``` 
   git clone https://github.com/ARISE-Handong/BugOss.git
   ```

2. Clone the OSS-Fuzz repository since BugOSS uses docker images of the OSS-Fuzz
   ```
   git clone https://github.com/google/oss-fuzz.git
   ```

3. Copy all files in an artifact directory to a `oss-fuzz/projects/project-name/`   
    all the given files (e.g., fuzz_target.cpp) should be located in the same directory with a Dockerfile, for example:  
   ```
   cp BugOss/aspell-18462/* oss-fuzz/projects/aspell/ 
   ```

4. Build the artifact with the given failure-reproducing-information from BugOSS using `oss-fuzz/infra/build_specified_commit.py`, for example:
   ```
   python3 oss-fuzz/infra/build_specified_commit.py 
               --project_name aspell  
               --commit e0646f9b063b23754951f1254f1ecb7af8ca36f3 
               --engine libfuzzer 
               --sanitizer address
   ``` 
