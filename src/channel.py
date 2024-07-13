import os
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.api_key = os.getenv("YOUTUBE_API_KEY_FOR_SKYPRO")
        if not self.api_key:
            raise ValueError("Не удалось найти API ключ. Проверьте переменную окружения YOUTUBE_API_KEY_FOR_SKYPRO.")
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        try:
            request = self.youtube.channels().list(
                part='snippet,statistics',
                id=self.channel_id
            )
            response = request.execute()
            print(json.dumps(response, indent=2, ensure_ascii=False))
        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
