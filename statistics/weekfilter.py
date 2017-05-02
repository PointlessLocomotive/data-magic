import psycopg2

WEEKS = [
    ('20170303'),
    ('20170303', '20170315'),
    ('20170316', '20170322'),
    ('20170323', '20170329'),
    ('20170330', '20170406'),
    ('20170407', '20170418'),
    ('20170419', '20170420'),
    ('20170421', '20170427'),
    ('20170428', '20170503'),
    ('20170504', '20170510'),
]


def week_filter(week_num, cursor=None):
    if not cursor:
        return False
    if 0 > week_num >= len(WEEKS):
        err_ms = "week index can't be greater than %d and less than 0" % (
            len(WEEKS) - 1)
        raise ReferenceError(err_ms)

    dates = WEEKS[week_num]
    if week_num == 0:
        query = (
            "SELECT text_analysis FROM tweets "
            "WHERE created_at < '%s';"
        )
    else:
        query = (
            "SELECT text, text_analysis FROM tweets "
            "WHERE created_at >= '%s' "
            "AND created_at <= '%s';"
        )
    cursor.execute(query % dates)

    rows = cursor.fetchall()
    return rows


def candidate_week_filter(week_num, candidate, cursor=None):
    if not cursor:
        return False

    if 0 > week_num >= len(WEEKS):
        err_ms = "week index can't be greater than %d and less than 0" % (
            len(WEEKS) - 1)
        raise ReferenceError(err_ms)

    query = ("select candidate_id from candidates where screen_name = '%s';")
    cursor.execute(query % candidate)
    candidate_id = cursor.fetchall()[0]
    dates = WEEKS[week_num]

    query = (
        "SELECT text_analysis FROM tweets "
        "WHERE created_at >= '%s' "
        "AND created_at <= '%s' "
        "AND author_id='%s';"
    )
    values = dates + candidate_id
    if week_num == 0:
        query = (
            "SELECT text_analysis FROM tweets "
            "WHERE created_at < '%s' "
            "AND author_id='%s';"
        )

    cursor.execute(query % values)

    rows = cursor.fetchall()
    return rows
