Проектирование API видеохостинга

Доступ к контенту каналов:
GET ~/channel/{channel_id} - получение начальной страницы канала
POST ~/channel - создание нового канала
PUT ~/channel/{channel_id} - изменение данных о канале
DELETE ~/channel/{channel_id} - удаление канала
GET ~/channel/{channel_id}/videos - получение страницы с видео канала
GET ~/channel/{channel_id}/about - получение страницы с информацией о канале

Доступ к видео:
GET ~/video/{video_id} - доступ к видео
POST ~/video - публикация видео
PUT ~/video/{video_id} - изменение данных о видео (название/описание)
DELETE ~/video/{video_id} - удаление видео

Лайки/комментарии: (реальных примеров этому я не нашел)
GET ~/video/{video_id}/comments - выгрузка комментариев 
POST ~/video/{video_id}/comment - публикация комментария
PUT ~/video/{video_id}/comment - изменение комментария
DELETE ~/video/{video_id}/comment - удаление комментария

GET ~/video/{video_id}/likes - выгрузка числа лайков 
POST ~/video/{video_id}/like - добавление лайка
DELETE ~/video/{video_id}/like - удаление лайка
