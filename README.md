
# Kafka Audio Processor

## 📌 Overview
Kafka Audio Processor is a Python-based project that leverages **Apache Kafka** for real-time audio streaming, transcription using **Whisper AI**, and translation with **DeepL**. The system consists of a Kafka producer that sends audio data and a Kafka consumer that reconstructs, transcribes, and translates the audio.

## 📂 Project Structure
/kafka-audio-processor
│── /producer                 # Kafka producer script
│── /consumer                 # Kafka consumer script
├── .env.example              # Example environment file
│── /docker                   # Docker-related files (e.g., Dockerfile, docker-compose)
    │── docker-compose.yaml   # Docker compose script to load up kafka image based container 
│── /scripts                  # Any helper scripts
│── .gitignore                # Ignore unnecessary files
│── README.md                 # Project documentation
│── requirements.txt          # Dependencies
│── docker-compose.yml        # Docker setup

## 🚀 Features
- **Kafka Integration:** Streams audio data in real time.
- **Audio Processing:** Converts WAV to MP3.
- **Transcription:** Uses OpenAI's **Whisper** model for speech-to-text.
- **Language Detection:** Detects the spoken language using **DetectLanguage API**.
- **Translation:** Translates transcriptions into multiple languages using **DeepL**.
- **Docker Support:** Easily deployable with **Docker** and **Docker Compose**.

## 🛠️ Installation & Setup
### **1. Clone the Repository**
```bash
git clone https://github.com/your-username/kafka-audio-processor.git
cd kafka-audio-processor
```

### **2a. Set Up Virtual Environment**
```bash
# Create a virtual environment
python -m venv kafka_python_venv

# Activate the virtual environment
# Windows
kafka_python_venv\Scripts\activate

# macOS/Linux
source kafka_python_venv/bin/activate

# Upgrade PiP if necessary
pip install --upgrade pip setuptools wheel
```


### **3. Install Dependencies and system wide resources**
```bash
pip install -r requirements.txt
brew install ffmpeg      # macOS
sudo apt install ffmpeg  # Linux
```

### **4. Configure Environment Variables**
Copy `.env.example` to `.env` and update the required API keys and Kafka configurations.
```bash
cp .env.example .env
```

### **5. Start Kafka (Using Docker-Compose) in docker file **
```bash
docker-compose up -d
```

### **6. Run Main.py script**
```bash
# Starts the Kafka producer and consumer
python main.py
```

## 🐳 Running with Docker
If you prefer running everything inside Docker:
```bash
docker-compose up --build
```

## 📌 Usage
1. **Run the main script**  Activate the listening process and transcription/translation of the audio. Then send audio chunks to Kafka and **Check the output** for transcriptions and translations.

## 📜 License
This project is licensed under the [MIT License](LICENSE).

## 🤝 Contributing
Feel free to submit **issues** or **pull requests** if you’d like to contribute!

## 📧 Contact
For questions or suggestions, reach out at [ogunadeolaoluwa@gmail.com].

