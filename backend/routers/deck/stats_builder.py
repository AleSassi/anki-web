from __future__ import annotations

import json
import random
import time
from typing import Sequence

import anki.cards
import anki.collection
from anki.consts import *
from anki.lang import FormatTimeSpan
from anki.utils import base62, ids2str

##########################################################################
# Collection stats, but just the data
#
# Adapted from https://github.com/ankitects/anki/blob/main/pylib/anki/stats.py
##########################################################################

PERIOD_MONTH = 0
PERIOD_YEAR = 1
PERIOD_LIFE = 2

class RESTCollectionStats:
    def __init__(self, col: anki.collection.Collection) -> None:
        self.col = col.weakref()
        self._stats = None
        self.type = PERIOD_MONTH
        self.wholeCollection = False

    def report_data(self, period: int = PERIOD_MONTH) -> dict:
        self.type = period
        if self.wholeCollection:
            deck = "whole collection"
        else:
            deck = self.col.decks.current()["name"]
        return {
            "graphs_data": {
                "today_stats": self.today_stats_data(),
                "due_graph": self.due_graph_data(),
                "review_graphs": self.review_graphs_data(),
                "introduction_graph": self.introduction_graph_data(),
                "interval_graph": self.interval_graph_data(),
                "hourly_breakdown_graph": self.hour_graph_data(),
                "ease_graph_data": self.ease_graph_data(),
                "card_graph": self.card_graph_data()
            },
            "generation_time": time.asctime(time.localtime(time.time())),
            "scope": deck,
            "period": ["1 month", "1 year", "deck life"][self.type]
        }


    def today_stats_data(self) -> dict:
        # studied today
        lim = self._revlogLimit()
        if lim:
            lim = " and " + lim
        cards, thetime, failed, lrn, rev, relrn, filt = self.col.db.first(
            f"""
select count(), sum(time)/1000,
sum(case when ease = 1 then 1 else 0 end), /* failed */
sum(case when type = {REVLOG_LRN} then 1 else 0 end), /* learning */
sum(case when type = {REVLOG_REV} then 1 else 0 end), /* review */
sum(case when type = {REVLOG_RELRN} then 1 else 0 end), /* relearn */
sum(case when type = {REVLOG_CRAM} then 1 else 0 end) /* filter */
from revlog where type != {REVLOG_RESCHED} and id > ? """
            + lim,
            (self.col.sched.day_cutoff - 86400) * 1000,
        )
        # mature today
        mcnt, msum = self.col.db.first(
            """
select count(), sum(case when ease = 1 then 0 else 1 end) from revlog
where lastIvl >= 21 and id > ?"""
            + lim,
            (self.col.sched.day_cutoff - 86400) * 1000,
        )

        cards = cards or 0
        thetime = thetime or 0
        failed = failed or 0
        lrn = lrn or 0
        rev = rev or 0
        relrn = relrn or 0
        filt = filt or 0
        mcnt = mcnt or 0
        msum = msum or 0

        return {
            "studied_today": {
                "count": cards, # if 0 -> "No cards have been studied today"
                "seconds": float(thetime)
            },
            "again_count": failed,
            "correct_count": cards - failed,
            "learned": lrn,
            "reviewed": rev,
            "relearned": relrn,
            "filtered": filt,
            "mature_ans_stats": {
                "correct": msum,
                "total": mcnt # if 0 -> "No mature cards were studied today"
            }
        }
    
    def due_graph_data(self) -> dict:
        start, end, chunk = self.get_start_end_chunk()
        d = self._due(start, end, chunk)
        datapoints = []
        tot = 0
        for day in d:
            tot += day[1] + day[2]
            datapoints.append({
                "time": day[0],
                "young_count": day[1],
                "mature_count": day[2],
                "cumulative_total": tot
            })
        tomorrow = int(self.col.db.scalar(
            f"""
select count() from cards where did in %s and queue in ({QUEUE_TYPE_REV},{QUEUE_TYPE_DAY_LEARN_RELEARN})
and due = ?"""
            % self._limit(),
            self.col.sched.today + 1,
        ))

        return {
            "datapoints": datapoints,
            "total": tot,
            "average": 0 if len(datapoints) == 0 else float(tot) / float(len(datapoints) * chunk),
            "due_tomorrow": tomorrow,
            "chunk": chunk,
            "bin_count": len(datapoints) * chunk
        }
    
    def review_graphs_data(self) -> dict:
        start, days, chunk = self.get_start_end_chunk()
        data = self._done(days, chunk)
        if not data:
            return {}
        
        datapoints = []
        cumulatives = []
        init_cumulatives = True
        all_counts_total = 0
        all_time_total = 0
        for row in data:
            datapoints.append({
                "time": row[0],
                "learn_count": row[1],
                "young_count": row[2],
                "mature_count": row[3],
                "relearn_count": row[4],
                "cram_count": row[5],
                "learn_time": row[6],
                "young_time": row[7],
                "mature_time": row[8],
                "lapse_time": row[9],
                "cram_time": row[10],
                "learn_count_cumulative_sum": cumulatives[0],
                "young_count_cumulative_sum": cumulatives[1],
                "mature_count_cumulative_sum": cumulatives[2],
                "relearn_count_cumulative_sum": cumulatives[3],
                "cram_count_cumulative_sum": cumulatives[4],
                "learn_time_cumulative_sum": cumulatives[5],
                "young_time_cumulative_sum": cumulatives[6],
                "mature_time_cumulative_sum": cumulatives[7],
                "lapse_time_cumulative_sum": cumulatives[8],
                "cram_time_cumulative_sum": cumulatives[9],
            })
            for i in range(0, 10):
                if init_cumulatives:
                    cumulatives.append(row[i + 1])
                    init_cumulatives = False
                else:
                    cumulatives[i] += row[i + 1]
        
        for i in range(0, 5):
            all_counts_total += cumulatives[i]
        for i in range(5, 10):
            all_time_total += cumulatives[i]

        result = {
            "datapoints": datapoints
        }

        (daysStud, fstDay) = self._daysStudied()
        period = self._periodDays()
        if not period:
            # base off earliest repetition date
            period = self._deckAge("review")
        
        result["days_studied"] = daysStud
        result["period"] = period
        studied_every_day = {}
        if daysStud != period:
            studied_every_day = {
                "unit": "reviews/day",
                "value": 0 if period == 0 else (all_counts_total / float(period))
            }
        
        result["review_count_stats"] = {
            "unit": "Answers",
            "total": {
                "unit": "reviews",
                "value": all_counts_total
            },
            "avg_per_day_studied": {
                "unit": "reviews/day",
                "value": 0 if daysStud == 0 else (all_counts_total / float(daysStud))
            },
            "if_studied_every_day": studied_every_day
        }

        time_frame = "Minutes"
        convHours = False
        if self.type != PERIOD_MONTH:
            time_frame = "Hours"
            convHours = True
            
        studied_every_day = {}
        if daysStud != period:
            studied_every_day = {
                "unit": "minutes/day",
                "value": 0 if daysStud == 0 else ((all_time_total * (60 if convHours else 1)) / float(period))
            }
        
        perMin = all_counts_total / float(all_time_total)
        average_secs = (all_counts_total * 60) / all_time_total

        result["review_time_stats"] = {
            "unit": time_frame,
            "convert_hours": convHours,
            "total": {
                "unit": "hours" if convHours else "minutes",
                "value": all_time_total
            },
            "avg_per_day_studied": {
                "unit": "minutes/day",
                "value": 0 if daysStud == 0 else ((all_time_total * (60 if convHours else 1)) / float(daysStud))
            },
            "if_studied_every_day": studied_every_day,
            "avg_answer_time": {
                "avg_secs": average_secs,
                "cards_per_minute": perMin
            }
        }

        return result
    
    def introduction_graph_data(self) -> dict:
        start, days, chunk = self.get_start_end_chunk()
        data = self._added(days, chunk)
        if not data:
            return {}

        datapoints = []
        init_cumulatives = True
        all_counts_total = 0
        for row in data:
            datapoints.append({
                "time": row[0],
                "learn_count": row[1],
                "learn_count_cumulative_sum": all_counts_total,
            })
            if init_cumulatives:
                all_counts_total = row[1]
                init_cumulatives = False
            else:
                all_counts_total += row[1]
        
        period = self._periodDays()
        if not period:
            # base off date of earliest added card
            period = self._deckAge("add")
        
        return {
            "datapoints": datapoints,
            "total_cards": all_counts_total,
            "avg_cards_per_day": all_counts_total / float(period)
        }
    
    def interval_graph_data(self) -> dict:
        (ivls, all, avg, max_), chunk = self._ivls()
        tot: int = 0
        totd = []
        if not ivls or not all:
            return {}
        
        datapoints = []
        for grp, cnt in ivls:
            tot += cnt
            datapoints.append({
                "interval": grp,
                "count": cnt,
                "cumulative_perc": tot / float(all) * 100
            })
        
        if self.type == PERIOD_MONTH:
            ivlmax = 31
        elif self.type == PERIOD_YEAR:
            ivlmax = 52
        else:
            ivlmax = max(5, ivls[-1][0])
        
        return {
            "datapoints": datapoints,
            "min_interval": -0.5,
            "max_interval": ivlmax + 0.5,
            "unit": chunk,
            "avg_interval": self.col.format_timespan(avg * 86400),
            "longest_interval": self.col.format_timespan(max_ * 86400)
        }
    
    def ease_graph_data(self) -> dict:
        datapoints = {"learning": [], "young": [], "mature": []}
        types = ("learning", "young", "mature")
        eases = self._eases()
        for type, ease, cnt in eases:
            if type == CARD_TYPE_LRN:
                ease += 5
            elif type == CARD_TYPE_REV:
                ease += 10
            key = types[type]
            datapoints[key].append({
                "ease": ease,
                "count": cnt
            })

        types = {PERIOD_MONTH: [0, 0], PERIOD_YEAR: [0, 0], PERIOD_LIFE: [0, 0]}
        for type, ease, cnt in eases:
            if ease == 1:
                types[type][0] += cnt
            else:
                types[type][1] += cnt
        
        ease_stats = []
        for type in range(3):
            (bad, good) = types[type]
            tot = bad + good
            try:
                pct = good / float(tot) * 100
            except:
                pct = 0
            ease_stats.append({
                "correct_perc": pct,
                "correct": good,
                "total": tot
            })
        return {
            "datapoints": datapoints,
            "ease_stats": ease_stats
        }
    
    def hour_graph_data(self) -> dict:
        data = self._hourRet()
        if not data:
            return {}
        
        shifted = []
        counts = []
        mcount = 0
        trend: list[tuple[int, int]] = []
        peak = 0
        for d in data:
            hour = (d[0] - 4) % 24
            pct = d[1]
            if pct > peak:
                peak = pct
            shifted.append((hour, pct))
            counts.append((hour, d[2]))
            if d[2] > mcount:
                mcount = d[2]
        
        shifted.sort()
        counts.sort()
        
        if len(counts) < 4:
            return {}
        
        for d in shifted:
            hour = d[0]
            pct = d[1]
            if not trend:
                trend.append((hour, pct))
            else:
                prev = trend[-1][1]
                diff = pct - prev
                diff /= 3.0
                diff = round(diff, 1)
                trend.append((hour, prev + diff))
        
        assert len(shifted) == len(counts)
        datapoints = []

        for i in range(len(shifted)):
            datapoints.append({
                "hour": shifted[i][0],
                "perc_correct": shifted[i][1],
                "answer_count": counts[i][1]
            })
        
        return {
            "datapoints": datapoints,
            "peak_perc": peak,
            "max_count": mcount
        }
    
    def card_graph_data(self) -> dict:
        # graph data
        div = self._cards() # (mature, young, new, suspended)
        (tot_cards, tot_notes) = self.col.db.first(
            """
select count(id), count(distinct nid) from cards
where did in %s """
            % self._limit()
        )
        
        result = {
            "mature": div[0],
            "young": div[1],
            "new": div[2],
            "suspended": div[3],
            "total_cards": tot_cards,
            "total_notes": tot_notes
        }

        (low, avg, high) = self._factors()
        if low:
            result["lowest_ease"] = low
            result["avg_ease"] = avg
            result["highest_ease"] = high
        
        return result
    
    ######################################################################
    # Helper Methods
    ######################################################################

    def get_start_end_chunk(self, by: str = "review") -> tuple[int, int | None, int]:
        start = 0
        if self.type == PERIOD_MONTH:
            end, chunk = 31, 1
        elif self.type == PERIOD_YEAR:
            end, chunk = 52, 7
        else:  #  self.type == 2:
            end = None
            if self._deckAge(by) <= 100:
                chunk = 1
            elif self._deckAge(by) <= 700:
                chunk = 7
            else:
                chunk = 31
        return start, end, chunk
    
    def _due(
        self, start: int | None = None, end: int | None = None, chunk: int = 1
    ) -> list:
        lim = ""
        if start is not None:
            lim += " and due-%d >= %d" % (self.col.sched.today, start)
        if end is not None:
            lim += " and day < %d" % end
        return self.col.db.all(
            f"""
select (due-?)/? as day,
sum(case when ivl < 21 then 1 else 0 end), -- yng
sum(case when ivl >= 21 then 1 else 0 end) -- mtr
from cards
where did in %s and queue in ({QUEUE_TYPE_REV},{QUEUE_TYPE_DAY_LEARN_RELEARN})
%s
group by day order by day"""
            % (self._limit(), lim),
            self.col.sched.today,
            chunk,
        )

    def _added(self, num: int | None = 7, chunk: int = 1) -> list[tuple[int, int]]:
        lims = []
        if num is not None:
            lims.append(
                "id > %d" % ((self.col.sched.day_cutoff - (num * chunk * 86400)) * 1000)
            )
        lims.append("did in %s" % self._limit())
        if lims:
            lim = "where " + " and ".join(lims)
        else:
            lim = ""
        if self.type == PERIOD_MONTH:
            tf = 60.0  # minutes
        else:
            tf = 3600.0  # hours
        return self.col.db.all(
            """
select
(cast((id/1000.0 - ?) / 86400.0 as int))/? as day,
count(id)
from cards %s
group by day order by day"""
            % lim,
            self.col.sched.day_cutoff,
            chunk,
        )

    """
    Returns a list of 11-element tuples:
    - day (int)
    - learn_count (int)
    - young_count (int)
    - mature_count (int)
    - relearn_count (int)
    - cram_count (int)
    - learn_time (float?)
    - young_time (float?)
    - mature_time (float?)
    - lapse_time (float?)
    - cram_time (float?)
    """
    def _done(self, num: int | None = 7, chunk: int = 1) -> list:
        lims = []
        if num is not None:
            lims.append(
                "id > %d" % ((self.col.sched.day_cutoff - (num * chunk * 86400)) * 1000)
            )
        lim = self._revlogLimit()
        if lim:
            lims.append(lim)
        if lims:
            lim = "where " + " and ".join(lims)
        else:
            lim = ""
        if self.type == PERIOD_MONTH:
            tf = 60.0  # minutes
        else:
            tf = 3600.0  # hours
        return self.col.db.all(
            f"""
select
(cast((id/1000.0 - ?) / 86400.0 as int))/? as day,
sum(case when type = {REVLOG_LRN} then 1 else 0 end), -- lrn count
sum(case when type = {REVLOG_REV} and lastIvl < 21 then 1 else 0 end), -- yng count
sum(case when type = {REVLOG_REV} and lastIvl >= 21 then 1 else 0 end), -- mtr count
sum(case when type = {REVLOG_RELRN} then 1 else 0 end), -- lapse count
sum(case when type = {REVLOG_CRAM} then 1 else 0 end), -- cram count
sum(case when type = {REVLOG_LRN} then time/1000.0 else 0 end)/?, -- lrn time
-- yng + mtr time
sum(case when type = {REVLOG_REV} and lastIvl < 21 then time/1000.0 else 0 end)/?,
sum(case when type = {REVLOG_REV} and lastIvl >= 21 then time/1000.0 else 0 end)/?,
sum(case when type = {REVLOG_RELRN} then time/1000.0 else 0 end)/?, -- lapse time
sum(case when type = {REVLOG_CRAM} then time/1000.0 else 0 end)/? -- cram time
from revlog %s
group by day order by day"""
            % lim,
            self.col.sched.day_cutoff,
            chunk,
            tf,
            tf,
            tf,
            tf,
            tf,
        )

    def _daysStudied(self) -> tuple[int, int]:
        lims = []
        num = self._periodDays()
        if num:
            lims.append(
                "id > %d" % ((self.col.sched.day_cutoff - (num * 86400)) * 1000)
            )
        rlim = self._revlogLimit()
        if rlim:
            lims.append(rlim)
        if lims:
            lim = "where " + " and ".join(lims)
        else:
            lim = ""
        ret = self.col.db.first(
            """
select count(), abs(min(day)) from (select
(cast((id/1000 - ?) / 86400.0 as int)+1) as day
from revlog %s
group by day order by day)"""
            % lim,
            self.col.sched.day_cutoff,
        )
        assert ret
        return ret

    def _ivls(self) -> tuple[list[Any], int]:
        start, end, chunk = self.get_start_end_chunk()
        lim = "and grp <= %d" % end if end else ""
        data = [
            self.col.db.all(
                f"""
select ivl / ? as grp, count() from cards
where did in %s and queue = {QUEUE_TYPE_REV} %s
group by grp
order by grp"""
                % (self._limit(), lim),
                chunk,
            )
        ]
        return (
            data
            + list(
                self.col.db.first(
                    f"""
select count(), avg(ivl), max(ivl) from cards where did in %s and queue = {QUEUE_TYPE_REV}"""
                    % self._limit()
                )
            ),
            chunk,
        )

    def _eases(self) -> list[tuple[int, int, int]]:
        lims = []
        lim = self._revlogLimit()
        if lim:
            lims.append(lim)
        days = self._periodDays()
        if days is not None:
            lims.append(
                "id > %d" % ((self.col.sched.day_cutoff - (days * 86400)) * 1000)
            )
        if lims:
            lim = "and " + " and ".join(lims)
        else:
            lim = ""
        ease4repl = "ease"
        return self.col.db.all(
            f"""
select (case
when type in ({REVLOG_LRN},{REVLOG_RELRN}) then 0
when lastIvl < 21 then 1
else 2 end) as thetype,
(case when type in ({REVLOG_LRN},{REVLOG_RELRN}) and ease = 4 then %s else ease end), count() from revlog where type != {REVLOG_RESCHED} %s
group by thetype, ease
order by thetype, ease"""
            % (ease4repl, lim)
        )

    def _hourRet(self) -> list[tuple[int, float, int]]:
        lim = self._revlogLimit()
        if lim:
            lim = " and " + lim
        rolloverHour = self.col.conf.get("rollover", 4)
        pd = self._periodDays()
        if pd:
            lim += " and id > %d" % ((self.col.sched.day_cutoff - (86400 * pd)) * 1000)
        return self.col.db.all(
            f"""
select
23 - ((cast((? - id/1000) / 3600.0 as int)) %% 24) as hour,
sum(case when ease = 1 then 0 else 1 end) /
cast(count() as float) * 100,
count()
from revlog where type in ({REVLOG_LRN},{REVLOG_REV},{REVLOG_RELRN}) %s
group by hour having count() > 30 order by hour"""
            % lim,
            self.col.sched.day_cutoff - (rolloverHour * 3600),
        )

    # Cards
    ######################################################################

    def _factors(self) -> Any:
        return self.col.db.first(
            f"""
select
min(factor) / 10.0,
avg(factor) / 10.0,
max(factor) / 10.0
from cards where did in %s and queue = {QUEUE_TYPE_REV}"""
            % self._limit()
        )

    def _cards(self) -> Any:
        return self.col.db.first(
            f"""
select
sum(case when queue={QUEUE_TYPE_REV} and ivl >= 21 then 1 else 0 end), -- mtr
sum(case when queue in ({QUEUE_TYPE_LRN},{QUEUE_TYPE_DAY_LEARN_RELEARN}) or (queue={QUEUE_TYPE_REV} and ivl < 21) then 1 else 0 end), -- yng/lrn
sum(case when queue={QUEUE_TYPE_NEW} then 1 else 0 end), -- new
sum(case when queue<{QUEUE_TYPE_NEW} then 1 else 0 end) -- susp
from cards where did in %s"""
            % self._limit()
        )

    # Tools
    ######################################################################

    def _limit(self) -> Any:
        if self.wholeCollection:
            return ids2str([d["id"] for d in self.col.decks.all()])
        return self.col.sched._deck_limit()

    def _revlogLimit(self) -> str:
        if self.wholeCollection:
            return ""
        return "cid in (select id from cards where did in %s)" % ids2str(
            self.col.decks.active()
        )

    def _title(self, title: str, subtitle: str = "") -> str:
        return f"<h1>{title}</h1>{subtitle}"

    def _deckAge(self, by: str) -> int:
        lim = self._revlogLimit()
        if lim:
            lim = " where " + lim
        if by == "review":
            t = self.col.db.scalar("select id from revlog %s order by id limit 1" % lim)
        elif by == "add":
            if self.wholeCollection:
                lim = ""
            else:
                lim = "where did in %s" % ids2str(self.col.decks.active())
            t = self.col.db.scalar("select id from cards %s order by id limit 1" % lim)
        if not t:
            period = 1
        else:
            period = max(1, int(1 + ((self.col.sched.day_cutoff - (t / 1000)) / 86400)))
        return period

    def _periodDays(self) -> int | None:
        start, end, chunk = self.get_start_end_chunk()
        if end is None:
            return None
        return end * chunk

    def _avgDay(self, tot: float, num: int, unit: str) -> str:
        vals = []
        try:
            vals.append("%(a)0.1f %(b)s/day" % dict(a=tot / float(num), b=unit))
            return ", ".join(vals)
        except ZeroDivisionError:
            return ""