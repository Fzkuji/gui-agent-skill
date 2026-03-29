# OSWorld Multi-Apps Domain — GUI Agent Skills Results

> 101 tasks total | **1 passed / 1 attempted** | 100 remaining | 2026-03-30

## Summary

| Metric | Value |
|--------|-------|
| Total tasks | 101 |
| ✅ Pass (score > 0) | 1 |
| ❌ Fail (score = 0) | 0 |
| 🔲 Not attempted | 100 |
| **Pass rate (attempted)** | **1/1** (100%) |
| **Pass rate (total)** | **1/101** (1.0%) |

**Test environment:** Ubuntu ARM VM (VMware Fusion), 1920×1080
**Evaluation:** Official OSWorld evaluator (`DesktopEnv.evaluate()`)
**Agent approach:** GUI Skills (screenshot → detect → act → verify → save) for ALL tasks
**Coordinate system:** ImageContext (pixel coords from detect_all, no scale conversion for crops)

> ⚠️ **Full reset on 2026-03-30 02:07 HKT**: All previous results cleared. Re-running all 101 tasks using the full GUI skills pipeline (OBSERVE → LEARN → ACT → VERIFY → SAVE). Previous run (48/61 pass, 78.7%) used mostly CLI shortcuts without GUI skills.

## Detailed Results

| # | Task ID | Instruction | Score | Status | Notes |
|---|---------|-------------|-------|--------|-------|
| 1 | `2b9493d7` | Force quit frozen LibreOffice Writer from command line | 1.0 | ✅ | GUI: screenshot → detect terminal → click → type killall → verify |
| 2 | `2c9fc0de` | Push changes from commandline to origin main with commit "daily update" | — | 🔲 | |
| 3 | `2fe4b718` | Create Animated GIF from video using VLC and GIMP | — | 🔲 | |
| 4 | `3680a5ee` | Merge file1.xlsx and file2.ods columns via command line to CSV | — | 🔲 | |
| 5 | `46407397` | Export charts from docx in email (Google Drive) | — | 🔲 | Google Drive task |
| 6 | `4e9f0faf` | Extract table data from Google Drive invoice | — | 🔲 | Google Drive task |
| 7 | `510f64c8` | Start VS Code in ~/Desktop/project from terminal | — | 🔲 | |
| 8 | `51f5801c` | Extract speaker notes from Impress to notes.docx | — | 🔲 | |
| 9 | `58565672` | Open first link from latest email in Bills folder | — | 🔲 | |
| 10 | `78aed49a` | Save email attachments to another folder (Google Drive) | — | 🔲 | Google Drive task |
| 11 | `897e3b53` | Convert form.docx to PDF and upload (Google Drive) | — | 🔲 | Google Drive task |
| 12 | `937087b6` | Set default video player as VLC on Ubuntu | — | 🔲 | |
| 13 | `a0b9dc9c` | Backup Bills emails as .eml files (Google Drive) | — | 🔲 | Google Drive task |
| 14 | `b52b40a5` | Merge PDF files from email attachment (Google Drive) | — | 🔲 | Google Drive task |
| 15 | `c867c42d` | Export Thunderbird contacts to CSV | — | 🔲 | |
| 16 | `d9b7c649` | Extract latest 5 emails from Thunderbird to xlsx | — | 🔲 | |
| 17 | `e135df7c` | Convert .xlsx to .html and view in Chrome | — | 🔲 | |
| 18 | `ee9a3c83` | Convert opened .ods file to CSV via terminal | — | 🔲 | |
| 19 | `f7dfbef3` | Convert all .doc files to PDF in command line | — | 🔲 | |
| 20 | `f8cfa149` | Copy cell B6 data and search it in Chrome | — | 🔲 | |
| 21 | `6d72aad6` | Convert Impress presentation to video (infeasible) | — | 🔲 | |
| 22 | `f918266a` | Complete code and run calculator.py | — | 🔲 | |
| 23 | `da52d699` | Analyze book reading spreadsheet | — | 🔲 | |
| 24 | `bc2b57f3` | Data analysis from reminder.docx requirements | — | 🔲 | |
| 25 | `74d5859f` | Set up web extension project | — | 🔲 | |
| 26 | `b5062e3e` | Extract first author info from PDF papers | — | 🔲 | |
| 27 | `00fa164e` | Include experiment results from xlsx into docx | — | 🔲 | |
| 28 | `acb0f96b` | Clone instructor-embedding repo | — | 🔲 | |
| 29 | `69acbb55` | Configure word embedding environment | — | 🔲 | Google Drive task |
| 30 | `48d05431` | Install conda and datasets package | — | 🔲 | |
| 31 | `68a25bd4` | Download PDF and citation from spreadsheet links | — | 🔲 | |
| 32 | `eb303e01` | Insert speaker notes from notes.docx into slides | — | 🔲 | |
| 33 | `0c825995` | Comprehensive report for environmental policy review | — | 🔲 | Google Drive task |
| 34 | `c7c1e4c3` | Collect professor contact info from homepage links | — | 🔲 | |
| 35 | `d1acdb87` | Hong Kong restaurant recommendations in LO Calc | — | 🔲 | |
| 36 | `deec51c9` | Find foundation language models from Oct 11 2023 | — | 🔲 | |
| 37 | `8e116af7` | Update bookkeeping sheet with recent transactions | — | 🔲 | |
| 38 | `337d318b` | Cross-check invoices with bank statements | — | 🔲 | |
| 39 | `82e3c869` | Sift through event photos for presenter photos | — | 🔲 | |
| 40 | `185f29bd` | Transfer Excel data to PDF form | — | 🔲 | |
| 41 | `869de13e` | Organize desktop files into categories | — | 🔲 | |
| 42 | `2c1ebcd7` | Review case study and check references | — | 🔲 | |
| 43 | `3a93cae4` | Add lecture slot to weekly timetable | — | 🔲 | |
| 44 | `1f18aa87` | Grade grammar tests and create answer file | — | 🔲 | |
| 45 | `26150609` | Fix Snake game grid alignment | — | 🔲 | |
| 46 | `9219480b` | Fix Tetris game rotation | — | 🔲 | |
| 47 | `881deb30` | Find Early Career Scheme faculty jobs in HK | — | 🔲 | |
| 48 | `7e287123` | Apply for General Research Fund | — | 🔲 | |
| 49 | `e2392362` | Set up academic homepage from template | — | 🔲 | |
| 50 | `5bc63fb9` | Process JSON LLM response data | — | 🔲 | |
| 51 | `26660ad1` | Test network quality with monitoring | — | 🔲 | |
| 52 | `a82b78bb` | Find personal webpages of paper authors | — | 🔲 | |
| 53 | `36037439` | Find Google Scholar page of corresponding author | — | 🔲 | |
| 54 | `716a6079` | Find secret.docx file on computer | — | 🔲 | |
| 55 | `873cafdd` | Install recommended VS Code plugins | — | 🔲 | |
| 56 | `a74b607e` | Install custom Chrome extension | — | 🔲 | |
| 57 | `6f4073b8` | Count ML conference meeting cities | — | 🔲 | |
| 58 | `da922383` | Store blog articles in local folder | — | 🔲 | |
| 59 | `2373b66a` | Monitor system resources with sar command | — | 🔲 | |
| 60 | `81c425f5` | Transfer LO Calc data to SQLite database | — | 🔲 | |
| 61 | `bb83cab4` | Convert Impress to Writer document | — | 🔲 | |
| 62 | `227d2f97` | Copy .xcf image to LibreOffice Writer | — | 🔲 | |
| 63 | `b337d106` | Configure Vim editor settings | — | 🔲 | |
| 64 | `20236825` | Algorithm practice with bubble sort tutorial | — | 🔲 | |
| 65 | `8df7e444` | Submit essay following reminder.docx guidelines | — | 🔲 | |
| 66 | `aad10cd7` | Save blog content as local file | — | 🔲 | |
| 67 | `02ce9a50` | Insert terminal screenshots into Linux tutorial | — | 🔲 | |
| 68 | `4c26e3f3` | Enhance brightness of dim slide image | — | 🔲 | |
| 69 | `a503b07f` | Convert receipt image to PDF | — | 🔲 | |
| 70 | `09a37c51` | Edit image per friend's request | — | 🔲 | |
| 71 | `3e3fc409` | Analyze movie watching records | — | 🔲 | |
| 72 | `f5c13cdd` | Draft email reminder for unpaid tuition | — | 🔲 | |
| 73 | `5990457f` | Add Yann LeCun entry from Google Scholar | — | 🔲 | |
| 74 | `415ef462` | Extract AWS invoice data from email | — | 🔲 | |
| 75 | `7ff48d5b` | Research Macau travel requirements | — | 🔲 | |
| 76 | `9f3bb592` | Remove subtitles from video | — | 🔲 | |
| 77 | `dd60633f` | Extract Python code from Karpathy's GPT colab | — | 🔲 | Google Drive task |
| 78 | `ce2b64a2` | Identify mountain names from photos | — | 🔲 | |
| 79 | `3f05f3b9` | Fix MP3 metadata from filenames | — | 🔲 | |
| 80 | `e1fc0df3` | Install LanguageTool extension for LibreOffice | — | 🔲 | |
| 81 | `f8369178` | Install Orchis GNOME theme | — | 🔲 | |
| 82 | `778efd0a` | Fix video playback in LO Impress | — | 🔲 | |
| 83 | `47f7c0ce` | Extract video frame and set as wallpaper | — | 🔲 | |
| 84 | `c2751594` | Export image from doc email attachment | — | 🔲 | |
| 85 | `788b3701` | Track story updates on GitHub | — | 🔲 | |
| 86 | `48c46dc7` | Auto set up workspace with tabs | — | 🔲 | |
| 87 | `42d25c08` | Convert web novel txt to ebook | — | 🔲 | |
| 88 | `e8172110` | Extract pixel art character from GIMP | — | 🔲 | |
| 89 | `42f4d1c7` | Configure VS Code for GIMP Script-Fu | — | 🔲 | |
| 90 | `3c8f201a` | Download and compress image to quality 60 | — | 🔲 | |
| 91 | `d68204bf` | Divide and rearrange image sections | — | 🔲 | |
| 92 | `91190194` | Crop top 20% off image in GIMP | — | 🔲 | |
| 93 | `7f35355e` | Export table to CSV and find medium price | — | 🔲 | |
| 94 | `98e8e339` | Merge txt files into single document | — | 🔲 | |
| 95 | `0e5303d4` | Download Python course materials | — | 🔲 | |
| 96 | `df67aebb` | Format paper references in thesis | — | 🔲 | |
| 97 | `5df7b33a` | Split bulky book into chapters | — | 🔲 | |
| 98 | `aceb0368` | Grade multiple choice English exam | — | 🔲 | |
| 99 | `22a4636f` | Convert docx to PDF and upload (Google Drive) | — | 🔲 | Google Drive task |
| 100 | `236833a3` | Find daily papers on Huggingface | — | 🔲 | |
| 101 | `67890eb6` | Check ACL best long paper awards 2019-2022 | — | 🔲 | |

## Blocked Tasks

| Task | Reason |
|------|--------|
| #5, #6, #10, #11, #13, #14, #29, #33, #77, #99 | Google Drive — missing `client_secrets.json` |

## Known Issues & Workarounds

| Issue | Workaround |
|-------|------------|
| Google Drive tasks fail at setup | Missing `client_secrets.json` — 10 tasks affected |
| LO Document Recovery dialog | `rm -f ~/.config/libreoffice/4/user/.~lock.*` before reopening |
| Chrome CDP port is 1337 | Not 9222 — check `ps aux \| grep chromium` |
| Thunderbird DB locked | `pkill -f thunderbird` before reading `abook.sqlite` |
| compare_csv is exact line match | Delimiter, row order must match gold exactly |
| VM pyautogui coords = screenshot coords | No scaling needed (1920×922 screenshot = 1920×922 screen) |

## Coordinate System

Using `ImageContext` (commit `1b22623`):
- `detect_all()` returns **image pixel coordinates** (no conversion)
- Cropping uses pixel coords directly (scale-independent)
- `pixel_scale` from `backingScaleFactor` (not `img_size / screen_size`)
- VM screenshots: `ImageContext.remote()` → scale=1.0, origin=(0,0)

## Files

- Results JSON: `~/OSWorld/results_official.json`
- GUI memory: `~/.openclaw/workspace/skills/gui-agent/memory/apps/`
- Test runner: `~/OSWorld/run_task.py`
