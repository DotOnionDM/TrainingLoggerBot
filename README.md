# TrainingLoggerBot
Тг-бот, который будет собирать информацию об обучении нейросетевых моделей с сервера,  подгружать информацию и рисовать графики. 

# Что сделано к КТ-2?
Реализован MVP продукта,  а именно:
1) Выбран хостинг для базы данных и самого тг-бота
2) Создана структура базы данных и добавлены тестовые значения в таблицы, а также собраны и добавлены мемы (куда без них?)
3) Создано ядро тг-бота, написаны основные функции работы с пользователем (присваивание id новому пользователю, отправка графика обучения нейросети по запросу пользователя, отправка мемов)
4) Созданы основные функции модуля логирования: логирование статуса всего обучения и по конкретным эпохам
В картинках:
![image](https://github.com/DotOnionDM/TrainingLoggerBot/assets/145100837/87b3910a-faec-462b-a7c4-c6b420afbaa8)
![image](https://github.com/DotOnionDM/TrainingLoggerBot/assets/145100837/60384f41-9571-4128-a3be-49c036fabcee)
![image](https://github.com/DotOnionDM/TrainingLoggerBot/assets/145100837/11332518-eac9-49bb-af1c-93811a07ca4f)

По ролям:
1) Александр Семикин - создание ядра бота, выбор хостинга и развертывание бота на хостинге, создание структуры базы данных, тестовые примеры обучения в базе данных + ноутбук с примером обучения нейросети.
2) 
3) 
4) 

TODO:
1)Расширение пользовательских сценариев
2)Тестирование и обработка ошибок
3)Расширение визуальной части
4)Добавление дополнительный фичей

# Цель
Наша команда реализовывает телеграм бота - логгера, который будет приносить пользу каждому занятому в сфере DL инженеру - следить и вовремя оповещать разработчика о процессе обучения его нейросети, пока он пьет кофе или играет с коллегами в настольный теннис. 

# Базовый функционал
В качестве MVP предполагается сделать телеграмм бота, который сможет по запросам пользователя отдавать текущую информацию о состоянии процесса обучения: номер текущей эпохи, примерное время до конца обучения, визуализировать данные и развлекать разработчика анекдотами и мемами, если модель слишком уж долго обучается и всех коллег в теннис он выиграл. То есть необходимо сделать:
1) Серверная часть бота
2) База данных, в которой храним текущую информацию и анекдоты
3) Модуль-обертка для взаимодействия сервера с обучением нейросети с нашей базой данных
4) Красивая визуализация и проработка различных вариантов подачи информации пользователю

# Примерный сценарий взаимодействия с ботом
1) Пользователь запускает обучение модели с нашей оберткой
2) На сервер поступает актуальная информация о процессе и статусе обучения модели
3) Пользователь имеет возможности получать информацию в своем телеграмме в активном (делая запросы) или пассивном (бот автоматически делает отчет через какой-то интервал времени) режимах.

# Команда и описание ролей
В соответствии с поставленными целями мы сделали разделение ролей:
1) Еремина Дарья - работа с серверной частью бота
2) Смирнова Валерия - работа с пользовательскими сценариями бота
3) Лагода Никита - разработка модуля-обертки
4) Семикин Александр - работа с базой данных

# Ну а если вы даже дочитали до этого момента - мем с попугаем.
![image](https://github.com/DotOnionDM/TrainingLoggerBot/assets/145100837/2e351f14-f814-44a8-a7f0-1940ffd30aef)
