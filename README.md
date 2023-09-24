sudo ln -s /home/pi/voice-ai-app/voice_ai_service.service /etc/systemd/system/voice_ai_service.service
sudo systemctl enable voice_ai_service.service
sudo systemctl start voice_ai_service.service
sudo systemctl status voice_ai_service.service

sudo systemctl restart voice_ai_service.service

sudo journalctl -u voice_ai_service.service

source venv/bin/activate
pip3 install -r requirements.txt