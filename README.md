## 🚀 Деплой на удалённый сервер через GitHub Actions

### 📌 Подготовка удалённого сервера

Перед деплоем необходимо:

1. Создать виртуальную машину (например, в Yandex Cloud).
2. Установить на сервер:
   - Docker
   - Docker Compose
3. Настроить SSH-доступ через SSH-ключ.
4. Открыть порты:
   - `22` (SSH)
   - `80` (HTTP)
5. Не нужно вручную клонировать репозиторий — это сделает GitHub Actions.

---

### 🔐 Секреты GitHub

Перейди в:  
**Settings → Secrets and variables → Actions → New repository secret**

Добавь следующие секреты:

| Название                    | Значение                                         |
|-----------------------------|--------------------------------------------------|
| `SSH_USER`                  | логин пользователя на сервере (например, `ubuntu`) |
| `SERVER_IP`                 | публичный IP-адрес сервера                      |
| `SSH_KEY`                   | приватный SSH-ключ (в одном блоке, без пароля)  |
| `DOCKER_HUB_USERNAME`       | имя пользователя Docker Hub                     |
| `DOCKER_HUB_ACCESS_TOKEN`   | access token с правами push/pull                |
| `DOTENV`                    | содержимое `.env` файла, одной строкой          |

---

### ⚙️ Как работает workflow

GitHub Actions запускается при каждом `push` или `pull_request` и выполняет:

1. Проверку стиля кода с помощью `flake8`
2. Запуск тестов (`python manage.py test`)
3. Сборку Docker-образа и загрузку его в Docker Hub
4. Подключение по SSH и перезапуск контейнера на удалённой машине

---

### 🐳 Команды, выполняемые на сервере

```bash
sudo docker pull <ваш-образ>
sudo docker stop myapp || true
sudo docker rm myapp || true
sudo docker run -d --name myapp -p 80:8000 <ваш-образ>
