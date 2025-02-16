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

    async def set_photo_format(self, user_id: int, photo_format: str) -> Any:
        url = f"{self.base_api_url}/users/set_photo_format/{user_id}/"
        return await self._make_request("POST", url, {"photo_format": photo_format})
    
    async def set_god_mode(self, user_id: int, god_mode: bool) -> Any:
        url = f"{self.base_api_url}/users/set_god_mode/{user_id}/"
        return await self._make_request("POST", url, {"god_mode": god_mode})

    async def get_avatar_price(self) -> float:
        """Получает стоимость аватара из API"""
        url = f"{self.base_api_url}/avatars/avatar/price/"
        response = await self._make_request("GET", url)
        return float(response.get("price", 490.00))
    

    async def get_user_packages(self, tg_user_id: int) -> Any:
        """Получение списка пакетов генерациий для пользователя"""
        url = f"{self.base_api_url}/packages/user-packages/{tg_user_id}/"
        return await self._make_request("GET", url)

    async def create_avatar(self, files: List[Tuple[str, Tuple[str, bytes, str]]], gender: str, tg_user_id: int) -> Any:
        """Загрузка фотографий для создания аватара"""
        url = f"{self.base_api_url}/avatars/upload/"
        data = {"gender": gender, "tg_user_id": tg_user_id}
        return await self._make_request("POST", url, data, files)
    
    async def check_avatar_slots(self, tg_user_id):
        url = f"{self.base_api_url}/avatars/check-slots/{tg_user_id}"
        return await self._make_request("GET", url)
    
    async def buy_avatart_slot(self, data):
        url = f"{self.base_api_url}/payments/avatar/"
        return await self._make_request("POST", url, data)

    async def get_user_avatars(self, user_tg_id) -> Any:
        """Получение списка аватаров"""
        url = f"{self.base_api_url}/avatars/{user_tg_id}/"
        return await self._make_request("GET", url)
    
    async def activate_avatar(self, avatar_id) -> Any:
        """Получение списка аватаров"""
        url = f"{self.base_api_url}/avatars/{avatar_id}/activate/"
        return await self._make_request("PATCH", url)

    async def get_styles_list(self, category_id: int = None) -> Any:
        """Получение списка стилей"""
        url = f"{self.base_api_url}/prompts/styles/"
        if category_id:
            url += f"?category={category_id}"
        return await self._make_request("GET", url)

    async def get_categories_list(self) -> Any:
        """Получение списка категорий"""
        url = f"{self.base_api_url}/prompts/categories/"
        return await self._make_request("GET", url)

    async def generate_user_image(self, prompt: str, model_id: int) -> Any:
        """Генерация изображения"""
        url = f"{self.base_api_url}/generations/"
        data = {"prompt": prompt, "model_id": model_id}
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
        url = f"{self.base_api_url}/users/{user_id}/"
        return await self._make_request("GET", url)

    async def create_payment(self, user_id: int, email: str, package_type_id: int, message_id: int, telegram_id: int) -> dict:
        """Создание платежа через ЮKassa"""
        url = f"{self.base_api_url}/payments/package/"
        data = {
            "user_id": user_id,
            "package_type_id": package_type_id,
            "email": email,
            "message_id": message_id,
            "telegram_id": telegram_id
        }
        return await self._make_request("POST", url, data)

    async def get_package_types(self) -> list:
        """Получение списка типов пакетов генераций"""
        url = f"{self.base_api_url}/packages/package-types/"
        return await self._make_request("GET", url)


# Экземпляр клиента
api_client = APIClient()
