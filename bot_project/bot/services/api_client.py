# bot/services/api_client.py

import httpx
from bot.config import Settings
from typing import Dict, Any, List, Tuple


class APIClient:
    """Клиент API для взаимодействия с сервером"""

    def __init__(self) -> None:
        self.client = httpx.AsyncClient(follow_redirects=True)
        self.access_token = None
        self.refresh_token = None
        self.base_api_url = f"{Settings.bot.API_URL}/api"

    async def close(self) -> None:
        if not self.client.is_closed:
            await self.client.aclose()

    async def authenticate(self, email: str, password: str) -> None:
        """Авторизация и получение токенов"""
        url = f"{self.base_api_url}/users/token/"
        try:
            response = await self.client.post(url, json={"email": email, "password": password})
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
        url = f"{self.base_api_url}/users/token/refresh/"
        try:
            response = await self.client.post(url, json={"refresh": self.refresh_token})
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

            print(response.json())
            return response.json()

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:  # Ошибка авторизации
                print("Access token expired. Attempting to refresh token.")
                try:
                    await self.refresh_access_token()
                    headers["Authorization"] = f"Bearer {self.access_token}"
                    response = await self.client.request(method, url, json=data, headers=headers)
                    response.raise_for_status()
                    return response.json()
                except httpx.HTTPStatusError as refresh_error:
                    if refresh_error.response.status_code == 401:
                        print("Refresh token expired. Re-authenticating.")
                        # Здесь можно реализовать повторную авторизацию, если необходимо
                        raise Exception("Both tokens expired. Please log in again.")
                    else:
                        raise refresh_error
            else:
                raise

    # Методы API

    async def upload_avatar(self, files: List[Tuple[str, Tuple[str, bytes, str]]], gender: str) -> Any:
        """Загрузка аватара"""
        url = f"{self.base_api_url}/avatars/upload/"
        data = {"gender": gender}
        return await self._make_request("POST", url, data, files)

    async def get_user_avatars(self) -> Any:
        """Получение списка аватаров"""
        url = f"{self.base_api_url}/avatars/"
        return await self._make_request("GET", url)

    async def get_styles_list(self) -> Any:
        """Получение списка стилей"""
        url = f"{self.base_api_url}/styles/"
        return await self._make_request("GET", url)

    async def get_categories_list(self) -> Any:
        """Получение списка категорий"""
        url = f"{self.base_api_url}/categories/"
        return await self._make_request("GET", url)

    async def generate_user_image(self, prompt: str, model_id: int) -> Any:
        """Генерация изображения"""
        url = f"{self.base_api_url}/generations/"
        data = {"prompt": prompt, "model_id": model_id}
        return await self._make_request("POST", url, data)

    async def purchase_generation_package(self, package_id: int) -> Any:
        """Покупка пакета генераций"""
        url = f"{self.base_api_url}/packages/yookassa-payment/create/"
        data = {"package_id": package_id}
        return await self._make_request("POST", url, data)

    async def enable_god_mode(self) -> Any:
        """Включение режима Бога"""
        url = f"{self.base_api_url}/god-mode/enable/"
        return await self._make_request("POST", url)

    async def disable_god_mode(self) -> Any:
        """Выключение режима Бога"""
        url = f"{self.base_api_url}/god-mode/disable/"
        return await self._make_request("POST", url)

    async def get_user_profile(self, user_id: str) -> Any:
        """Получение профиля пользователя"""
        url = f"{self.base_api_url}/users/{user_id}"
        return await self._make_request("GET", url)

    async def create_payment(self, user_id: str, package_type_id: int) -> dict:
        """Создание платежа через ЮKassa"""
        url = f"{self.base_api_url}/packages/yookassa-payment/create/"
        data = {"user_id": user_id, "package_type_id": package_type_id}
        return await self._make_request("POST", url, data)

    async def get_package_types(self) -> list:
        """Получение списка типов пакетов генераций"""
        url = f"{self.base_api_url}/packages/package-types/"
        return await self._make_request("GET", url)


# Экземпляр клиента
api_client = APIClient()
