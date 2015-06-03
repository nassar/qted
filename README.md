

qted - a toolkit for scheduling Qualtrics surveys
=================================================

Copyright (C) 2015 University of North Carolina at Chapel Hill  
Portions Copyright (C) 2013-2015 Nassib Nassar

This software is distributed under the terms of the MIT License.

The MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Configuring qted
----------------

First set the configuration values for qted, such as qt_user, qt_token, etc.:

    $ qted config db_dbname DATABASE_NAME

    $ qted config db_user DATABASE_USER

    $ qted config db_password DATABASE_PASSWORD

    $ qted config user_email YOUR_EMAIL_ADDRESS

    $ qted config qt_user QUALTRICS_USER_NAME

    $ qted config qt_token QUALTRICS_TOKEN

    $ qted config qt_library QUALTRICS_LIBRARY

For example:

    $ qted config db_dbname qted_nassar

    $ qted config db_user nassar

    $ qted config db_password Jf9dv28WxnHt

    $ qted config user_email nassar278@email.unc.edu

    $ qted config qt_user 123456789#unc

    $ qted config qt_token fTWRbCf8Ufw6UyPWvrX2tYkVCe4U3d5orsPh8WTd

    $ qted config qt_library UR_2pwMtoRw5UeaHkV

These values are stored in .qted in your home directory.

The variable qt_server is set to the web service endpoint and defaults to

    https://survey.qualtrics.com/WRAPI/ControlPanel/api.php

It can be changed with

    $ qted config qt_server NEW_WEB_SERVICE_ENDPOINT

Create a Postgres database that qted can connect to using the database
connection parameters configured above.  The database will be used by qted to
store its data.  The database should be loaded with the qted schema (located in
the file database/database-schema.sql) using the psql tool, e.g.:

    $ psql -U nassar -d qted_nassar -f database-schema.sql


Tutorial
--------

To see a list of qted commands, enter

    $ qted

The output takes the form:

    qted - a toolkit for scheduling Qualtrics surveys

    usage: qted COMMAND [ARGUMENTS]...

    where COMMAND is one of:
    config       - modify the configuration file
    debug-server - send requests to the Qualtrics server
    responses    - retrieve response data for tracked surveys and optionally
                   create panels for any responses indicating a follow-up
    surveys      - list all surveys in account
    track        - add or remove surveys to tracking list

To get a list of surveys in your Qualtrics account, use the surveys command,
e.g.:

    $ qted surveys

The output takes the form:

    SurveyID           | SurveyName
    SV_eDrK72Xw7ywWhud | First Followup
    SV_3P3Og74F2syoitn | Baseline
    SV_0JOsg38Jt1EQ2Mt | Second Followup

Or add the --verbose (-v) option for more detail:

    $ qted surveys -v

    SurveyID           | SurveyName      | SurveyStatus | SurveyCreationDate
    SV_3P3Og74F2syoitn | Baseline        | Active       | 2015-02-13 12:07:18
    SV_eDrK72Xw7ywWhud | First Followup  | Active       | 2015-02-13 12:09:05
    SV_0JOsg38Jt1EQ2Mt | Second Followup | Active       | 2015-02-13 12:37:14

To start tracking a survey, use the track command and specify the first few
characters of the Survey ID (enough characters to uniquely identify a survey).
Follow-up surveys can be provided using the --follow-up option with a
comma-separated list of Survey IDs.  E.g.:

    $ qted track SV_3P3 --follow-up SV_eDr,SV_0JO

To see which surveys are being tracked:

    $ qted track

    SurveyID           | FollowupIDs
    SV_3P3Og74F2syoitn | SV_eDrK72Xw7ywWhud,SV_0JOsg38Jt1EQ2Mt

To stop tracking a survey, use the --stop option:

    $ qted track --stop SV_3P3

To retrieve responses from all currently tracked surveys, use the responses
command:

    $ qted responses

    ResponseID        | SurveyID           | EndDate             | PANEL
    R_2s1E04D6Hk8mw5C | SV_3P3Og74F2syoitn | 2015-02-13 14:43:35 | 1 *
    R_25WxkzMyIHXONos | SV_3P3Og74F2syoitn | 2015-02-13 14:45:09 | 1 *
    R_3h47oQtJMQf9SIL | SV_3P3Og74F2syoitn | 2015-02-13 14:46:17 | 2
    R_W87bGlrBt04vdoR | SV_3P3Og74F2syoitn | 2015-02-13 14:47:48 | 1 *

Note that responses indicating that a follow-up survey should be scheduled are
marked with an asterisk.

The responses command can be invoked with the --panel option, which causes new
panels to be created and queues the panels for scheduling with follow-up
surveys (though the invitations to the follow-up surveys are not yet sent):

    $ qted responses --panel

    ResponseID        | SurveyID           | EndDate             | PANEL
    R_2s1E04D6Hk8mw5C | SV_3P3Og74F2syoitn | 2015-02-13 14:43:35 | 1 *
    R_25WxkzMyIHXONos | SV_3P3Og74F2syoitn | 2015-02-13 14:45:09 | 1 *
    R_3h47oQtJMQf9SIL | SV_3P3Og74F2syoitn | 2015-02-13 14:46:17 | 2
    R_W87bGlrBt04vdoR | SV_3P3Og74F2syoitn | 2015-02-13 14:47:48 | 1 *

    PanelID            | SurveyID           | PanelName
    ML_4NJIGyusBBFw3cN | SV_3P3Og74F2syoitn | SV_3P3Og74F2syoitn 2015-05-26 150829

    RecipientID          | ResponseID        | PanelID
    MLRP_b4x9L4Y7j1F7PNP | R_2s1E04D6Hk8mw5C | ML_4NJIGyusBBFw3cN
    MLRP_aeK6D7paHQI3pRP | R_25WxkzMyIHXONos | ML_4NJIGyusBBFw3cN
    MLRP_0enxD9USXmMbeTz | R_W87bGlrBt04vdoR | ML_4NJIGyusBBFw3cN

Using the --panel option also has the effect of marking the responses as
having been processed, so that they will not be retrieved again on subsequent
invocations of the responses command:

    $ qted responses

    No new responses found

