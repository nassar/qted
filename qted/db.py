import psycopg2
import psycopg2.extras
import json

import config

def dict_to_json(d):
    return json.dumps(d, ensure_ascii=False)

def connect():
    """
    Open a connection to the database and return a connection object.
    """
    dbname = config.get_config('db_dbname')
    user = config.get_config('db_user')
    password = config.get_config('db_password')
    conn = psycopg2.connect(
        'dbname={:s} user={:s} password={:s}'.format(dbname, user, password) )
    return conn

def cursor(conn):
    return conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)

def get_all_surveys():
    """
    Return a list of all surveys as (id, surveyid, tracked) from the database.
    """
    with connect() as conn:
        with cursor(conn) as cur:
            sql = '''
                  select t.id, t.surveyid, t.tracked,
                      array_to_string(array_agg(t.followupid), ',') follow_up
                  from (
                      select s.id, s.surveyid, s.tracked, f.followupid
                      from survey s
                          left join follow_up f on f.baseline_id = s.id
                      order by s.surveyid, f.rank ) t
                  group by t.id, t.surveyid, t.tracked;
                  '''
            cur.execute(sql)
            return cur.fetchall()

def get_tracked_surveys():
    """
    Return a list of all tracked surveys as (id, surveyid) from the database.
    """
    with connect() as conn:
        with cursor(conn) as cur:
            sql = """
                select id, surveyid, last_responseid from survey
                where tracked = TRUE;
                """
            cur.execute(sql)
            return cur.fetchall()

def get_survey_by_surveyid(surveyid):
    """
    Given a surveyid, return (id, surveyid, tracked) from the database, or
    None if there is no match.
    """
    with connect() as conn:
        with cursor(conn) as cur:
            sql = """
                select id, surveyid, tracked, last_responseid
                from survey
                where surveyid = %s;
                """
            data = (surveyid, )
            cur.execute(sql, data)
            return cur.fetchone()

def set_tracking_survey(surveyid, id, track):
    """
    Given a surveyid, the database Id for the survey (or None if it does not
    exist in the database), and the Boolean value track, update the database to
    enable or disable tracking for the survey (track=True means enable,
    track=False means disable).
    """
    if id is None:
        if track == False:
            # If we want to stop tracking and the survey is not in the
            # database, then there is nothing to do.
            return
        else:  # track == True
            # To enable tracking, add the survey in the database if it isn't
            # there.
            with connect() as conn:
                with conn.cursor() as cur:
                    sql = '''
                          insert into survey (id, surveyid, tracked,
                                              last_responseid)
                          values (DEFAULT, %s, TRUE, NULL);
                          '''
                    data = (surveyid, )
                    cur.execute(sql, data)
    else:  # id is not None
        # If we have an id, set the tracking flag.
        with connect() as conn:
            with conn.cursor() as cur:
                sql = '''
                      update survey set tracked = %s where id = %s;
                      '''
                data = (track, id)
                cur.execute(sql, data)

def set_survey_last_responseid(id, last_responseid):
    """
    Update the survey having the given id with the given value of
    last_responseid.
    """
    with connect() as conn:
        with conn.cursor() as cur:
            sql = """
                update survey set last_responseid = %s where id = %s;
                """
            data = (last_responseid, id)
            cur.execute(sql, data)

def track_survey(surveyid, track):
    """
    Given a survey Id, turn on tracking of the survey by marking it as tracked
    in the database.
    """
    survey = get_survey_by_surveyid(surveyid)
    tracked = survey is not None and survey[2] == True
    id = None if survey is None else survey[0]
    # If tracking is not already in the desired state, change it.
    if (not tracked and track == True) or (tracked and track == False):
        set_tracking_survey(surveyid, id, track)

def get_response_by_responseid(responseid):
    """
    Given a response Id, return (id, responseid) from the database, or None if
    there is no match.
    """
    with connect() as conn:
        with cursor(conn) as cur:
            sql = """
                select id, responseid from response where responseid = %s;
                """
            data = (responseid, )
            cur.execute(sql, data)
            return cur.fetchone()

#def insert_response(responseid, response_data):
#    with connect() as conn:
#        with cursor(conn) as cur:
#            sql = """
#                insert into response (id, responseid, data)
#                values (DEFAULT, %s, %s);
#                """
#            data = (responseid, dict_to_json(response_data))
#            cur.execute(sql, data)

#def set_response_data(responseid, response_data):
#    with connect() as conn:
#        with cursor(conn) as cur:
#            sql = """
#                update response set data = %s where response_id = %s;
#                """
#            data = (dict_to_json(response_data), responseid)
#            cur.execute(sql, data)

#def store_response(responseid, response_data):
#    """
#    Store response data in the database, modifying an existing response if one
#    exists or otherwise inserting a new one.
#    """
#    response = get_response_by_responseid(responseid)
#    if response is None:
#        insert_response(responseid, response_data)
#    else:
#        set_response_data(response.id, response_data)

def select_panel_by_panelid(panelid):
    with connect() as conn:
        with cursor(conn) as cur:
            sql = '''
                  select id, panelid, surveyid, invited
                  from panel
                  where panelid = %s;
                  '''
            data = (panelid, )
            cur.execute(sql, data)
            return cur.fetchone()

def insert_panel(panelid, surveyid, invited):
    with connect() as conn:
        with cursor(conn) as cur:
            sql = '''
                  insert into panel (id, panelid, surveyid, invited)
                  values (DEFAULT, %s, %s, %s);
                  '''
            data = (panelid, surveyid, invited)
            cur.execute(sql, data)

def update_panel_by_panelid(panelid, invited):
    with connect() as conn:
        with cursor(conn) as cur:
            sql = '''
                  update panel set invited = %s where panelid = %s;
                  '''
            data = (invited, panelid)
            cur.execute(sql, data)

def queue_panel(panelid, surveyid):
    """
    Given a panel Id, queue the panel in the database.
    """
    panel = select_panel_by_panelid(panelid)
    if panel is None:
        insert_panel(panelid, surveyid, invited=False)
    else:
        update_panel_by_panelid(panel.id, invited=False)

def delete_follow_up_surveys(surveyid):
    with connect() as conn:
        with cursor(conn) as cur:
            sql = '''
                  delete from follow_up where baseline_id in (
                      select id from survey where surveyid = %s );
                  '''
            data = surveyid,
            cur.execute(sql, data)

def set_follow_up_surveys(surveyid, follow_up):
    # First delete the existing list of follow-ups from the database
    delete_follow_up_surveys(surveyid)
    # Add the new list
    with connect() as conn:
        with cursor(conn) as cur:
            # Retrieve database id of survey
            sql = '''
                  select id from survey where surveyid = %s;
                  '''
            data = surveyid,
            cur.execute(sql, data)
            baseline_id = cur.fetchone().id
            # Insert follow-up surveys
            rank = 0
            for followupid in follow_up:
                rank += 1000
                sql = '''
                      insert into follow_up (baseline_id, followupid, rank)
                      values (%s, %s, %s);
                      '''
                data = baseline_id, followupid, rank
                cur.execute(sql, data)

def get_next_followupid(surveyid):
    """
    Given a surveyid (which may be either a baseline or follow-up survey),
    return the next follow-up surveyid, or None if there is no follow-up.
    """
    # First check if surveyid is a baseline survey
    survey = get_survey_by_surveyid(surveyid)
    if survey is not None:
        # Return first follow-up
        with connect() as conn:
            with cursor(conn) as cur:
                sql = '''
                      select followupid from follow_up where baseline_id = %s
                          order by rank limit 1;
                      '''
                data = survey.id,
                cur.execute(sql, data)
                follow_up = cur.fetchone()
                return follow_up.followupid if follow_up is not None else None
    # Search for surveyid in follow-ups
    with connect() as conn:
        with cursor(conn) as cur:
            sql = '''
                  select baseline_id, rank
                        from follow_up
                        where followupid = %s;
                  '''
            data = surveyid,
            cur.execute(sql, data)
            follow_up = cur.fetchone()
            if follow_up is None:
                # Unable to find surveyid in baselines or follow-ups
                return None
    baseline_id = follow_up.baseline_id
    rank = follow_up.rank
    # Return next survey in follow-up list
    with connect() as conn:
        with cursor(conn) as cur:
            sql = '''
                  select followupid from follow_up
                      where (baseline_id = %s) and (rank > %s)
                      order by rank limit 1;
                  '''
            data = (baseline_id, rank)
            cur.execute(sql, data)
            follow_up = cur.fetchone()
            return follow_up.followupid if follow_up is not None else None

if __name__ == '__main__':
    pass

