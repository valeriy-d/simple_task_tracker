# simple_task_tracker
### Запуск проекта
```bash
./docker-compose-command.sh
```

- В диалоговом окне вам будет предложено собрать образ заново, необходимо выбрать [Y][N]
- Далее запустятся миграции и тесты
- После тестов Вам будет предложено создать суперпользователя для django, можно пропустить
- Наконец сервис запустится, обратиться к нему можно по адрессу [0.0.0.0:8000](http://0.0.0.0:8000)

Ссылка на образ в docker hub [valeriyd/task-tracker/](https://hub.docker.com/r/valeriyd/task-tracker/)

**Примечание:** в данном проекте _front-end_ не реализован