# Мониторинг соединений к базам 1С Предприятия средствами Zabbix

Описание подготовлено для операционной системы Windows.
Для получения информации используются консольные утилиты RAS (сервер) и RAC (клиент).
Для установки сервера в качестве службы используется команда:

sc create "1C:Enterprise RAS" binpath= "C:\Program Files\1cv8\Х.Х.Х.ХХХХ\bin\ras.exe cluster --service" displayname= "1C:Enterprise RAS" start= auto 

Для запуска команда:

net start "1C:Enterprise RAS"
