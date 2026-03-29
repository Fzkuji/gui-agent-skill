# OSWorld VM — Platform Notes

## VM API
- Execute: `POST http://172.16.105.128:5000/execute` with `{"command": ["cmd", "arg"]}`
- Screenshot: `GET http://172.16.105.128:5000/screenshot`
- File transfer: base64 encoding via execute endpoint (no direct download API)

## GUI Input (Linux aarch64)
- Best method: `xdotool type --delay 10 "text"` (handles special chars)
- Mouse: `pyautogui.click(x, y)` via execute API
- Keyboard shortcuts: `pyautogui.hotkey('ctrl', 's')` via execute API
- Window management: `wmctrl -a "title"` / `wmctrl -c "title"`
- OCR: Run `detect_text()` on host Mac (download screenshot first)
- Coordinates: 1:1 (no Retina scaling), resolution 1920x1080

## Common Issues
- HuggingFace downloads often fail with SSL errors
- pip install on VM times out frequently
- Config "open" type opens files in associated apps
