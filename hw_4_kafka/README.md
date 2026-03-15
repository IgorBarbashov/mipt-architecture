# Брокеры сообщений

### Условия

В рамках данного задания вам необходимо установить брокер сообщений Kafka и реализовать через него взаимодействие двух микросервисов.

### Для этого выполните следующие шаги

- Установите Kafka на свой компьютер или сервер [kafka.apache.org...quickstart](https://kafka.apache.org/quickstart/). Если вы работаете на Windows, можете установить Kafka при помощи Docker
- Также установите в отдельный контейнер PostgreSQL, если вы еще не делали этого ранее. Если делали, запустите данный контейнер
- Создайте первое приложение на FastAPI, которое будет принимать запрос на создание записи об ошибке:

    ```
    POST /errors/

    {
    "code": 2043,
    "message": "Everything is broken",
    "details": "Some system details about error"
    }
    ```

    Данное приложение должно класть каждое такое сообщение в Kafka в определенную тему.

- Создайте второе приложение на FastAPI, которое будет получать сообщения об ошибках из Kafka и класть их в базу данных PostgreSQL в таблицу errors, имеющую следующую структуру: `id`, `time`, `code`, `message`, `details`
- Проверьте работу обоих приложений, используя Postman

### Детали реализации

- Посмотреть какие торики есть

    ```
    docker exec -it kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
    ```

- Посмотреть сообщения в топике

    ```
    docker exec -it kafka /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic error_messages --from-beginning
    ```

- Посмотреть список таблиц

    ```
    psql -h localhost -p 5433 -U admin -d app_db
    
    затем
    \d

    затем
    SELECT * FROM errors;
    ```
