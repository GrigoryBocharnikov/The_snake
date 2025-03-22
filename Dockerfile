FROM python:3.8.3-alpine

# Создаем пользователя и рабочую директорию
RUN adduser -D myuser && mkdir -p /app && chown -R myuser:myuser /app
USER myuser
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY --chown=myuser:myuser requirements.txt .
RUN pip install --user --no-warn-script-location -r requirements.txt

# Добавляем путь к локальным бинарникам пользователя
ENV PATH="/home/myuser/.local/bin:${PATH}"

# Копируем исходный код
COPY --chown=myuser:myuser . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
