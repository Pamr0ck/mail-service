import enum


class NotificationCategory(enum.Enum):
    """
    Категории пользовательских уведомлений (значения < 16 символов)

    Attributes
    ----------

    ----- АКТИВНОСТЬ -----
    POST_REPLY - Ответ на пост
    COMMENT_REPLY - Ответ на комментарий
    POST_UPVOTE - Апвоут поста
    COMMENT_UPVOTE - Апвоут комментария/ответа на комментарий
    MENTIONS - Упоминания

    ----- ОБУЧЕНИЕ -----
    HOMEWORK_SUBMISSION_STATUS - Изменение статуса домашнего задания
    HOMEWORK_MESSAGES - Уведомление о сообщениях преподавателя

    ----- АНАЛИТИКА -----

    ----- СОБЫТИЯ -----
    EVENTS - Уведомление о событии, в котором пользователь нажал «Участвую»

    ----- НОВОСТИ КЛУБА -----
    CLUB_NEWS - Новости клуба

    ----- СКИДКИ И ПРОМОАКЦИИ -----
    PROMO - Скидки и промоакции

    ----- ЭФИРЫ -----
    UPCOMING_EVENT - Ближайшие эфиры
    NEW_RECORDING - Новая запись эфиров
    """

    POST_REPLY = "club.post.reply"
    COMMENT_REPLY = "club.comment.reply"
    POST_UPVOTE = "club.post.upvote"
    COMMENT_UPVOTE = "club.comment.upvote"
    MENTIONS = "club.mentions"

    HOMEWORK_SUBMISSION_STATUS = "club.education.homework.status"
    HOMEWORK_MESSAGES = "club.education.homework.messages"

    ANALYTICAL_CONTENT_UPDATE = "club.analytics.update"
    INVEST_IDEA_STATUS_UPDATE = "club.analytics.idea.status.update"

    MEETING_UPCOMING_EVENT = "club.meeting.event.new"
    MEETING_NEW_RECORDING = "club.meeting.content.new"
    MEETING_NEW_LIVE_MASTERCLASS = "club.meeting.live_masterclass.new"
    MEETING_NEW_MARATHON = "club.meeting.marathon.new"
    MEETING_NEW_COMPETITION = "club.meeting.competition.new"

    EVENTS = "club.events"

    CLUB_NEWS = "club.news"

    PROMO = "club.promo"
