from datetime import timedelta
import time
import iso8601
import pandas as pd

import get_events as ge
# import private as pvt


def add_durations(evStartEvEnd_eventsDct):
    """ """

    (evStart_evEnd, eventsDct) = evStartEvEnd_eventsDct
    calEvDFsDct = {}
    calPerTots = []
    for key, value in eventsDct.items():
        evDurations = []
        events = value
        for event in events:
            dtEvEnd = iso8601.parse_date(event['end'])
            dtEvStart = iso8601.parse_date(event['start'])
            evDur = dtEvEnd - dtEvStart
            evDurations.append(evDur)
        eventDF = pd.DataFrame(events)
        eventDF['Durations'] = evDurations
        calEvDFsDct[key] = eventDF
    evStartEvEnd_calEvDfsDct = (evStart_evEnd, calEvDFsDct)
    ## TODO(eayoungs): Revise name of return variable for consistency
    return  evStartEvEnd_calEvDfsDct


def hrs_min_sec(td):
    """ """
    
    hrs = td.seconds//3600
    mins = (td.seconds//60)%60

    return str(td.days*24+hrs)+':'+str(mins)


def get_cals_durs(calEvDFsDct):
    """ """

    calPerTotHrsDct = {}
    for key, value in calEvDFsDct.items():
        calPerDurs = pd.Series(value['Durations'])
        calPerTotHrs = sum(value['Durations'], timedelta())
        calPerTotHrsDct[key] = calPerTotHrs

    return calPerTotHrsDct


def summarize_cals_durs(calPerTotHrsDct):
    """ """

    cumCalTotHrsLst = []
    for key, value in calPerTotHrsDct.items():
        cumCalTotHrsLst.append(value)
    
    sumCumCalTotHrs = sum(cumCalTotHrsLst, timedelta())
    allCalDurTotSec = sumCumCalTotHrs.total_seconds()

    colNames = ['Unique Events', 'Hours', 'Percent']
    calDursDF = pd.DataFrame()
    for key, value in calPerTotHrsDct.items():
        thisCalDurTotSec = value.total_seconds()
        thisCalDurPerc = (thisCalDurTotSec / allCalDurTotSec) * 100
        currRow = [key, hrs_min_sec(value), round(thisCalDurPerc, 1)]
        currFrame = pd.DataFrame([currRow],columns=colNames)
        calDursDF = calDursDF.append(currFrame)

    fmatSumCumCalTotHrs = hrs_min_sec(sumCumCalTotHrs)
    calDursDF_fmatSumCumCalTotHrs = (calDursDF, fmatSumCumCalTotHrs)

    return  calDursDF_fmatSumCumCalTotHrs


def get_work_types(evStartEvEnd_calEvDfsDct, calendar):
    """ """

    # TODO: Iterate to accomodate multiple calendars
    (evStart_evEnd, calEvDfDct) = evStartEvEnd_calEvDfsDct
    billingCal = calEvDfDct[calendar]
    workTypes = billingCal.summary.unique()
    workTypesDct = {}
    for workType in workTypes:
        workTypeDf = billingCal.ix[billingCal['summary']==workType]
        workTypesDct[workType] = workTypeDf

    return workTypesDct


def get_projects(workTypeDf, projectNm):
    """ """

    projectDf = workTypeDf.loc[workTypeDf['description'].str.contains(
                                                                    projectNm)]
    invoiceDf = pd.DataFrame(projectDf[['description', 'start', 'Durations']])
    invoiceDf['Durations'] = invoiceDf['Durations'].apply(hrs_min_sec)
    invoiceDf['description'] = invoiceDf['description'].str.extract(
                                                   '(- \[.\].+)', expand=True)

    return invoiceDf
