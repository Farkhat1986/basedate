# Тестирование WordPress Comments API (CRUD операции)

Набор тест-кейсов для тестирования CRUD операций с пользователями через WordPress REST API.

## Общая информация

**Базовый URL:** `http://localhost:8000/wp-json/wp/v2/comments`  
**Аутентификация:** Требуются права администратора

## Быстрый старт

```bash
# Склонировать репозиторий
git clone https://github.com/Farkhat1986/basedate.git

# Зайти в проект 
cd basedate

# Создать и активировать виртуальное окружение 
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Установить зависимости
pip install -r requirements.txt

# Для запуску двух контейнеров Docker, база данных MySQL и Apache сервер с предустановленным WordPress
В командной строке выполнить команду – `docker-compose up`
```

## Тест кейс 1: Проверка создания нового комментария к посту

**Предусловие:** Существует опубликованный пост с ID = post_id

**Цель:** Создание комментария авторизованным пользователем
**Шаги:** 
	
1. Отправить POST запрос на адресс http://localhost:8000/wp-json/wp/v2/comments
2. Указать в заголовках Basic-Auth с логином и паролем ("Firstname.LastName", "123-Test")
3. Тело запроса (JSON)		
```
		{
			"post": post_id,
			"content": "Тестовый комментарий"
		}
```
**Ожидаемый результат:** 
* Статус 201 created
* В теле ответа:
	- id - целое число, 
	- post = post_id, 
	- content.rendered = "Тестовый комментарий", 
	- status = "approved", 
	- author_name - имя пользователя
	- В БД в wp_comments
		* comment_post_ID = {post_id}
		* comment_approved = '1'

## Тест кейс 2: Проверка получения комментария по ID

**Предусловие:**
* Создан комментарий, его ID = {comment_id}

**Цель:** Получение данных конкретного комментария по его ID

**Шаги:**
1. Отправить GET запрос на http://localhost:8000/wp-json/wp/v2/comments/{comment_id}

**Ожидаемый результат:** 
* Статус 200 created
* В теле ответа:
	- id - {comment_id}, 
	- post = ID поста, 
	- content.rendered - текст комментария, 
	- status = "approved"

## Тест кейс 3: Проверка получения списка всех комментариев

**Предусловие:**
* В системе существует как минимум 2 комментария

**Цель:** Получение списка всех комментариев

**Шаги:**
1. Отправить GET запрос на http://localhost:8000/wp-json/wp/v2/comments

**Ожидаемый результат:**
* Статус 200 created
* В теле ответа:
	* Массив из нескольких объектов
	* Каждый объект содержит:
		- id - целое число, 
		- post, 
		- content.rendered - текст комментария, 
		- status = "approved".

## Тест кейс 4: Проверка обновления существующего комментария

**Предусловие:**
* Создан комментарий, например как в Тест кейсе 1, его ID = {comment_id}

**Цель:** Получение данных об изменении комментария

**Шаги:**
1. Отправить POST запрос на http://localhost:8000/wp-json/wp/v2/comments/{comment_id}
2. Указать в заголовках Basic-Auth с логином и паролем ("Firstname.LastName", "123-Test")
3. В теле запроса 
```
	{
		'content": "Измененный текст комментария"
	}
```
**Ожидаемый результат:**
* Статус 200 created
* В теле ответа:
	* content.rendered = "Измененный текст комментария"
	* В БД в wp_comments поле comment_content обновлен comment_ID = {comment_id}

## Тест кейс 5: Проверка удаления комментария

**Предусловие:**
* Создан комментарий, например как в Тест кейсе 1, его ID = {comment_id}

**Цель:** Получение информации об удаленном комментарии

**Шаги:**
1. Отправить DELETE запрос на http://localhost:8000/wp-json/wp/v2/comments/{comment_id}
2. Указать в заголовках Basic-Auth с логином и паролем ("Firstname.LastName", "123-Test")

**Ожидаемый результат:**
* Статус 200 created
* В теле ответа:
	* status = "trash"
	* В БД в wp_comments запись с comment_ID = comment_id имеет comment_approved = 'trash'
















