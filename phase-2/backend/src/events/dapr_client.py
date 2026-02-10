"""Dapr HTTP client wrapper for pub/sub and state operations."""
import os
from typing import Any, Optional

import httpx

# Dapr sidecar configuration
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
DAPR_BASE_URL = f"http://localhost:{DAPR_HTTP_PORT}"

# Component names
PUBSUB_NAME = os.getenv("DAPR_PUBSUB_NAME", "pubsub")
STATESTORE_NAME = os.getenv("DAPR_STATESTORE_NAME", "statestore")


class DaprClient:
    """HTTP client for Dapr sidecar operations."""

    def __init__(self, base_url: str = DAPR_BASE_URL):
        self.base_url = base_url
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create async HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=30.0,
            )
        return self._client

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None

    # Pub/Sub operations

    async def publish_event(
        self,
        topic: str,
        data: dict[str, Any],
        pubsub_name: str = PUBSUB_NAME,
        metadata: Optional[dict[str, str]] = None,
    ) -> bool:
        """
        Publish an event to a topic via Dapr pub/sub.

        Args:
            topic: Topic name to publish to
            data: Event data as dictionary
            pubsub_name: Name of the pub/sub component
            metadata: Optional metadata headers

        Returns:
            True if published successfully, False otherwise
        """
        client = await self._get_client()
        url = f"/v1.0/publish/{pubsub_name}/{topic}"

        headers = {"Content-Type": "application/json"}
        if metadata:
            for key, value in metadata.items():
                headers[f"metadata.{key}"] = value

        try:
            response = await client.post(url, json=data, headers=headers)
            return response.status_code in (200, 204)
        except httpx.HTTPError as e:
            print(f"Error publishing to {topic}: {e}")
            return False

    # State store operations

    async def save_state(
        self,
        key: str,
        value: Any,
        statestore_name: str = STATESTORE_NAME,
        metadata: Optional[dict[str, str]] = None,
    ) -> bool:
        """
        Save state to Dapr state store.

        Args:
            key: State key
            value: State value
            statestore_name: Name of the state store component
            metadata: Optional metadata

        Returns:
            True if saved successfully
        """
        client = await self._get_client()
        url = f"/v1.0/state/{statestore_name}"

        state_item = {"key": key, "value": value}
        if metadata:
            state_item["metadata"] = metadata

        try:
            response = await client.post(url, json=[state_item])
            return response.status_code in (200, 204)
        except httpx.HTTPError as e:
            print(f"Error saving state {key}: {e}")
            return False

    async def get_state(
        self,
        key: str,
        statestore_name: str = STATESTORE_NAME,
    ) -> Optional[Any]:
        """
        Get state from Dapr state store.

        Args:
            key: State key
            statestore_name: Name of the state store component

        Returns:
            State value or None if not found
        """
        client = await self._get_client()
        url = f"/v1.0/state/{statestore_name}/{key}"

        try:
            response = await client.get(url)
            if response.status_code == 200:
                return response.json()
            return None
        except httpx.HTTPError as e:
            print(f"Error getting state {key}: {e}")
            return None

    async def delete_state(
        self,
        key: str,
        statestore_name: str = STATESTORE_NAME,
    ) -> bool:
        """
        Delete state from Dapr state store.

        Args:
            key: State key
            statestore_name: Name of the state store component

        Returns:
            True if deleted successfully
        """
        client = await self._get_client()
        url = f"/v1.0/state/{statestore_name}/{key}"

        try:
            response = await client.delete(url)
            return response.status_code in (200, 204)
        except httpx.HTTPError as e:
            print(f"Error deleting state {key}: {e}")
            return False

    # Service invocation

    async def invoke_service(
        self,
        app_id: str,
        method: str,
        data: Optional[dict[str, Any]] = None,
        http_method: str = "POST",
    ) -> Optional[dict[str, Any]]:
        """
        Invoke a method on another service via Dapr.

        Args:
            app_id: Target app ID
            method: Method/endpoint to invoke
            data: Request body
            http_method: HTTP method (GET, POST, etc.)

        Returns:
            Response data or None on error
        """
        client = await self._get_client()
        url = f"/v1.0/invoke/{app_id}/method/{method}"

        try:
            if http_method.upper() == "GET":
                response = await client.get(url)
            else:
                response = await client.request(
                    http_method.upper(),
                    url,
                    json=data,
                )

            if response.status_code == 200:
                return response.json()
            return None
        except httpx.HTTPError as e:
            print(f"Error invoking {app_id}/{method}: {e}")
            return None

    # Secrets

    async def get_secret(
        self,
        secret_store: str,
        key: str,
    ) -> Optional[dict[str, str]]:
        """
        Get a secret from Dapr secret store.

        Args:
            secret_store: Name of the secret store component
            key: Secret key

        Returns:
            Secret value(s) or None if not found
        """
        client = await self._get_client()
        url = f"/v1.0/secrets/{secret_store}/{key}"

        try:
            response = await client.get(url)
            if response.status_code == 200:
                return response.json()
            return None
        except httpx.HTTPError as e:
            print(f"Error getting secret {key}: {e}")
            return None

    # Health check

    async def health_check(self) -> bool:
        """Check if Dapr sidecar is healthy."""
        client = await self._get_client()
        try:
            response = await client.get("/v1.0/healthz")
            return response.status_code == 200
        except httpx.HTTPError:
            return False


# Singleton instance
_dapr_client: Optional[DaprClient] = None


def get_dapr_client() -> DaprClient:
    """Get the Dapr client singleton."""
    global _dapr_client
    if _dapr_client is None:
        _dapr_client = DaprClient()
    return _dapr_client
