
# Kafka Audio Processor

## 📌 Overview
Kafka Audio Processor is a Python-based project that leverages **Apache Kafka** for real-time audio streaming, transcription using **Whisper AI**, and translation with **DeepL**. The system consists of a Kafka producer that sends audio data and a Kafka consumer that reconstructs, transcribes, and translates the audio.

## 📂 Project Structure
/kafka-audio-processor
│── /producer                 # Kafka producer script
│── /consumer                 # Kafka consumer script
│   ├── .env.example          # Example environment file
│── /docker                   # Docker-related files (e.g., Dockerfile, docker-compose)
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

### **2. Set Up Virtual Environment**
```bash
# Create a virtual environment
python -m venv kafka_python_venv

# Activate the virtual environment
# Windows
kafka_python_venv\Scripts\activate

# macOS/Linux
source kafka_python_venv/bin/activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Configure Environment Variables**
Copy `.env.example` to `.env` and update the required API keys and Kafka configurations.
```bash
cp .env.example .env
```

### **5. Start Kafka (Using Docker-Compose)**
```bash
docker-compose up -d
```

### **6. Run Producer & Consumer**
```bash
# Start the Kafka producer
python producer/producer.py

# Start the Kafka consumer
python consumer/consumer.py
```

## 🐳 Running with Docker
If you prefer running everything inside Docker:
```bash
docker-compose up --build
```

## 📌 Usage
1. **Run the consumer script** to activate the listening process and transcription/translation of the audio.
2. **Run the producer script** to send audio chunks to Kafka.
3. **Check the output** for transcriptions and translations.

## 📜 License
This project is licensed under the [MIT License](LICENSE).

## 🤝 Contributing
Feel free to submit **issues** or **pull requests** if you’d like to contribute!

## 📧 Contact
For questions or suggestions, reach out at [ogunadeolaoluwa@gmail.com].

