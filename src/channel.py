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
        self._initialize_channel_data()

    def _initialize_channel_data(self) -> None:
        """Инициализирует данные о канале с помощью YouTube API."""
        try:
            request = self.youtube.channels().list(
                part='snippet,statistics',
                id=self.channel_id
            )
            response = request.execute()
            channel_info = response['items'][0]

            self.title = channel_info['snippet']['title']
            self.description = channel_info['snippet']['description']
            self.url = f"https://www.youtube.com/channel/{self.channel_id}"
            self.subscriber_count = int(channel_info['statistics']['subscriberCount'])
            self.video_count = int(channel_info['statistics']['videoCount'])
            self.view_count = int(channel_info['statistics']['viewCount'])

        except HttpError as e:
            print(f"An HTTP error occurred: {e}")

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API."""
        api_key = os.getenv("YOUTUBE_API_KEY_FOR_SKYPRO")
        if not api_key:
            raise ValueError("Не удалось найти API ключ. Проверьте переменную окружения YOUTUBE_API_KEY_FOR_SKYPRO.")
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, filename: str) -> None:
        """Сохраняет значения атрибутов экземпляра Channel в JSON файл."""
        data = {
            "id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

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
