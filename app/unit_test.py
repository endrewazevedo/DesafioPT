from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home_unauthenticated():
    response = client.get("/")
    assert response.status_code == 200
    assert "Olá visitante" in response.text
    assert "Entrar" in response.text
    assert "Cadastre-se" in response.text

def test_alterar_info():
    response = client.get("/alterar_informacoes", cookies={"user_id": "joao@example.com"})
    assert response.status_code == 200
    assert "Editar informações" in response.text
    assert "value=\"João Silva\"" in response.text
