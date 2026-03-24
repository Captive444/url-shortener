import pytest
from app.utils import generate_short_id

@pytest.mark.parametrize("url", [
    "https://example.com",
    "https://example.com/very/long/url",
    "https://example.com/" + "a" * 100,
])
def test_create_short_link(client, url):
    """Создание короткой ссылки возвращает корректные данные"""
    response = client.post(
        "/shorten",
        json={"url": url}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "short_id" in data
    assert "short_url" in data
    assert len(data["short_id"]) == 6  # TODO: вынести в конфиг???
    assert "localhost:8000" in data["short_url"]


def test_create_link_with_invalid_url_returns_error(client):
    """Невалидный URL возвращает 422"""
    response = client.post("/shorten", json={"url": "not-a-valid-url"})
    assert response.status_code == 422


def test_redirect_increments_click_count(client):
    """Редирект увеличивает счётчик кликов"""
    # Создаём ссылку
    create_resp = client.post("/shorten", json={"url": "https://google.com"})
    assert create_resp.status_code == 200
    short_id = create_resp.json()["short_id"]
    
   
    stats_before = client.get(f"/stats/{short_id}").json()
    assert stats_before["clicks"] == 0
    
   
    redirect_resp = client.get(f"/{short_id}", follow_redirects=False)
    assert redirect_resp.status_code == 307
    
    # убираем завершающий слэш на всякий пожарный
    location = redirect_resp.headers["location"].rstrip('/')
    assert location == "https://google.com"
    
   
    stats_after = client.get(f"/stats/{short_id}").json()
    assert stats_after["clicks"] == 1


def test_nonexistent_link_returns_404(client):
    """Несуществующая ссылка возвращает 404"""
    response = client.get("/nonexistent123")
    assert response.status_code == 404
    
    stats_response = client.get("/stats/nonexistent123")
    assert stats_response.status_code == 404



def test_generate_short_id_length():
    assert len(generate_short_id(6)) == 6
    assert len(generate_short_id(8)) == 8


def test_generate_short_id_alphanumeric():
    short_id = generate_short_id(100)
    assert short_id.isalnum()

