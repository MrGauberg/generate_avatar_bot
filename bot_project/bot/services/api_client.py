# bot/services/api_client.py

import httpx
from bot.config import Settings
from typing import Dict, Any, List, Tuple


class APIEndpoints:
    """Класс с API-эндпоинтами"""

    BASE_API_URL = Settings.bot.API_URL

    # Авторизация
    @property
    def auth_login(self):
        return f"{self.BASE_API_URL}/api/users/token/"

    @property
    def auth_refresh(self):
        return f"{self.BASE_API_URL}/api/users/token/refresh/"

    # Аватары
    @property
    def create_avatar(self):
        return f"{self.BASE_API_URL}/api/avatars/upload/"

    @property
    def get_avatars(self):
        return f"{self.BASE_API_URL}/avatars/"

    # Стили и категории
    @property
    def get_styles(self):
        return f"{self.BASE_API_URL}/styles/"

    @property
    def get_categories(self):
        return f"{self.BASE_API_URL}/categories/"

    # Генерация изображений
    @property
    def generate_image(self):
        return f"{self.BASE_API_URL}/generations/"

    # Покупка пакетов генераций
    @property
    def purchase_package(self):
        return f"{self.BASE_API_URL}/orders/"

    # Режим Бога
    @property
    def enable_god_mode(self):
        return f"{self.BASE_API_URL}/god-mode/enable/"

    @property
    def disable_god_mode(self):
        return f"{self.BASE_API_URL}/god-mode/disable/"
    
    @property
    def get_user_profile(self):
        return f"{self.BASE_API_URL}/api/user/profile/"


class APIClient(APIEndpoints):
    """Клиент API для взаимодействия с сервером"""

    def __init__(self) -> None:
        self.client = httpx.AsyncClient(follow_redirects=True)
        self.access_token = None
        self.refresh_token = None

    async def close(self) -> None:
        if not self.client.is_closed:
            await self.client.aclose()

    async def authenticate(self, email: str, password: str) -> None:
        """Авторизация и получение токенов"""
        try:
            response = await self.client.post(
                self.auth_login, json={"email": email, "password": password}
            )
            response.raise_for_status()
            tokens = response.json()
            self.access_token = tokens.get("access")
            self.refresh_token = tokens.get("refresh")
            print("Authentication successful!")
        except httpx.HTTPError as e:
            print(f"Authentication failed: {e}")
            raise

    async def refresh_access_token(self) -> None:
        """Обновление access-токена"""
        try:
            response = await self.client.post(
                self.auth_refresh, json={"refresh": self.refresh_token}
            )
            response.raise_for_status()
            tokens = response.json()
            self.access_token = tokens.get("access")
            print("Access token refreshed successfully.")
        except httpx.HTTPError as e:
            print(f"Failed to refresh token: {e}")
            raise

    async def _make_request(
        self,
        method: str,
        url: str,
        data: Dict[str, Any] = None,
        files: List[Tuple[str, Tuple[str, bytes, str]]] = None,
        headers: Dict[str, str] = None
    ) -> Any:
        try:
            headers = headers or {}
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            if files:
                response = await self.client.request(method, url, data=data, files=files, headers=headers)
            else:
                response = await self.client.request(method, url, json=data, headers=headers)

            # response.raise_for_status()
            print(response.json())
            return response.json()

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:  # Ошибка авторизации
                print("Access token expired. Attempting to refresh token.")
                try:
                    await self.refresh_access_token()  # Попробовать обновить токен
                    headers["Authorization"] = f"Bearer {self.access_token}"
                    response = await self.client.request(method, url, json=data, headers=headers)
                    response.raise_for_status()
                    return response.json()
                except httpx.HTTPStatusError as refresh_error:
                    if refresh_error.response.status_code == 401:  # Refresh тоже недействителен
                        print("Refresh token expired. Re-authenticating.")
                        await self.authenticate()  # Полная авторизация
                        headers["Authorization"] = f"Bearer {self.access_token}"
                        response = await self.client.request(method, url, json=data, headers=headers)
                        response.raise_for_status()
                        return response.json()
                    else:
                        raise refresh_error
            else:
                raise

    # Методы API

    async def upload_avatar(self, files: List[Tuple[str, Tuple[str, bytes, str]]], gender: str) -> Any:
        """Загрузка аватара"""
        return await self._make_request("POST", self.create_avatar, {"gender": gender}, files
        )


    async def get_user_avatars(self) -> Any:
        """Получение списка аватаров"""
        return await self._make_request("GET", self.get_avatars)

    async def get_styles_list(self) -> Any:
        """Получение списка стилей"""
        return await self._make_request("GET", self.get_styles)

    async def get_categories_list(self) -> Any:
        """Получение списка категорий"""
        return await self._make_request("GET", self.get_categories)

    async def generate_user_image(self, prompt: str, model_id: int) -> Any:
        """Генерация изображения"""
        data = {"prompt": prompt, "model_id": model_id}
        return await self._make_request("POST", self.generate_image, data)

    async def purchase_generation_package(self, package_id: int) -> Any:
        """Покупка пакета генераций"""
        data = {"package_id": package_id}
        return await self._make_request("POST", self.purchase_package, data)

    async def enable_god_mode(self) -> Any:
        """Включение режима Бога"""
        return await self._make_request("POST", self.enable_god_mode)

    async def disable_god_mode(self) -> Any:
        """Выключение режима Бога"""
        return await self._make_request("POST", self.disable_god_mode)
    
    async def get_user_profile(self, user_id) -> Any:
        """Получение профиля пользователя"""
        return await self._make_request("GET", self.get_user_profile)

        

# Экземпляр клиента
api_client = APIClient()
