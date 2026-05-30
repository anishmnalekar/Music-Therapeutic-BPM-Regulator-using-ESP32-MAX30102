#Music Therapeutic BPM Regulator

##Project Overview

The **Music Therapeutic BPM Regulator** is an IoT-based biofeedback system designed to monitor a user’s heart rate (BPM) in real time and regulate mood through therapeutic music playback.

The system uses an **ESP32 microcontroller**, **MAX30102 pulse sensor**, and **DFPlayer Mini MP3 module** to:

- Measure heart rate (BPM)
- Classify emotional/mood condition indirectly through BPM trends
- Play relaxing or energetic music accordingly
- Provide a web-based dashboard for interaction and monitoring
- Compare BPM before and after music therapy

This project combines:

- Embedded Systems
- IoT
- Biomedical Signal Processing
- Web Interface Development
- Music-Based Therapeutic Assistance

---

#Working Principle

1. The MAX30102 sensor continuously reads IR pulse data.
2. Signal filtering and peak detection algorithms calculate BPM.
3. User selects a music category:
   - Calm
   - Energetic
   - Neutral
4. The ESP32 communicates with the DFPlayer Mini module.
5. Music is played from the SD card.
6. BPM is measured again after therapy.
7. Results are displayed on a web dashboard.

---

#Hardware Components

| Component | Purpose |
|---|---|
| ESP32 | Main microcontroller |
| MAX30102 Sensor | Heart rate monitoring |
| DFPlayer Mini | MP3 playback module |
| Speaker | Audio output |
| MicroSD Card | Stores music tracks |
| WiFi Network | Hosts dashboard server |
| Jumper Wires | Connections |
| Breadboard | Prototyping |

---

#Software & Technologies Used

| Technology | Purpose |
|---|---|
| MicroPython | ESP32 programming |
| HTML/CSS/JavaScript | Web dashboard |
| AsyncIO | Async web server execution |
| UART Communication | DFPlayer control |
| I2C Protocol | MAX30102 communication |

---

#Project Structure

```bash
├── boot.py
├── main.py
├── bpm_sensor.py
├── dfplayer.py
├── index.html
├── webserver.py
├── max30102.py
└── music/
```

---

#BPM Detection Methodology

Heart Rate Formula:

\[
BPM = \frac{60000}{RR\ Interval\ (ms)}
\]

---

#Features

1.Real-time BPM monitoring  
2.Web dashboard interface  
3.Therapeutic music playback  
4.Mood improvement feedback buttons  
5.Automatic music stopping after 60 seconds  
6.Genre-based shuffle playback  
7.BPM comparison before and after therapy  
8.WiFi-enabled access  

---

#Installation & Setup

## Flash MicroPython on ESP32

```bash
esptool.py --chip esp32 erase_flash
esptool.py --chip esp32 --port COMX write_flash -z 0x1000 firmware.bin
```

## Configure WiFi

Edit `boot.py`

```python
sta_if.connect('YOUR_WIFI_NAME', 'YOUR_PASSWORD')
```

---

#Applications

- Stress monitoring systems
- Smart wellness devices
- Biomedical IoT research
- Smart healthcare
- Relaxation assistance systems

---

#Future Improvements

- AI-based emotion classification
- Spotify API integration
- ECG waveform visualization
- Mobile application support
- Machine learning mood prediction

---

#Author

**Anish Nalekar**  
MSc Computer Science

**Sanika Kambli**
MSc Bioinformatics

---

#License

This project is intended for educational and research purposes.
