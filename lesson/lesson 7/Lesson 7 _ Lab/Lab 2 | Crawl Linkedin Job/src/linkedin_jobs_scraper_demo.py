#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEMO: lấy 1 TRANG kết quả LinkedIn job search -> CSV.
"""

import csv, os, sys
from datetime import datetime, timezone
from urllib.parse import quote

import requests
from dotenv import load_dotenv

load_dotenv()          # nạp file .env cùng thư mục vào os.environ


# --- BƯỚC 0: nhận cấu hình từ MÔI TRƯỜNG (run.sh export vào đây) ----------
KEYWORDS = os.getenv("KEYWORDS", "data analyst")
GEO_ID   = int(os.getenv("GEO_ID", "104195383"))          # 104195383 = Vietnam
COUNT    = int(os.getenv("COUNT", "25"))
OUT      = os.getenv("OUT", "linkedin_jobs_demo.csv")
CARD = "com.linkedin.voyager.dash.jobs.JobPostingCard"
COLS = ["job_id", "title", "company", "location", "listed_date", "url"]


# --- BƯỚC 1: đọc cookie từ biến môi trường ---------------------------------
li_at = (os.getenv("LI_AT") or "").strip().strip('"')
jsess = (os.getenv("LI_JSESSIONID") or "").strip().strip('"')
if not li_at or not jsess:
    sys.exit("Thiếu cookie: export LI_AT và LI_JSESSIONID (lấy ở F12 > Application > Cookies).")

# --- BƯỚC 2: dựng chuỗi `query`  của LinkedIn ------------------
query = (f"(origin:JOB_SEARCH_PAGE_JOB_FILTER,keywords:{quote(KEYWORDS)}"
         f",locationUnion:(geoId:{GEO_ID}),selectedFilters:(),spellCorrectionEnabled:true)")


# --- BƯỚC 3: gọi Voyager API (API nội bộ mà chính web LinkedIn dùng) -------
url = ("https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards"
       "?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollection-207"
       f"&count={COUNT}&q=jobSearch&query={query}&start=0")

print(f"Đang tìm '{KEYWORDS}' ...", flush=True)
r = requests.get(url, timeout=30, headers={
    
    "cookie": f'li_at={li_at}; JSESSIONID="{jsess}"',
    "csrf-token": jsess,
    "accept": "application/vnd.linkedin.normalized+json+2.1",
    "x-restli-protocol-version": "2.0.0",                    
    "user-agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"),
})
if r.status_code != 200:
    sys.exit(f"HTTP {r.status_code} (401/403 = cookie sai hoặc hết hạn). {r.text[:200]}")


# --- BƯỚC 4: bóc JSON -> list[dict] ---------------------------------------
rows = []
for e in r.json().get("included", []):
    # ĐỪNG SỬA: phải check jobPostingTitle, payload có nhiều stub chỉ mang entityUrn.
    if e.get("$type") != CARD or not e.get("jobPostingTitle"):
        continue
    job_id = (e.get("jobPostingUrn") or "").split(":")[-1]
    listed = ""
    for f in e.get("footerItems") or []:
        if f.get("type") == "LISTED_DATE" and f.get("timeAt"):  # timeAt = epoch MILLIseconds
            listed = datetime.fromtimestamp(f["timeAt"] / 1000, timezone.utc).strftime("%Y-%m-%d")
    rows.append({
        "job_id": job_id,
        "title": e["jobPostingTitle"],
        # ĐỪNG SỬA: `or {}` chứ không phải .get(k, {}) -> LinkedIn trả null thật.
        "company": (e.get("primaryDescription") or {}).get("text", ""),
        "location": (e.get("secondaryDescription") or {}).get("text", ""),
        "listed_date": listed,
        "url": f"https://www.linkedin.com/jobs/view/{job_id}/",
    })

# --- BƯỚC 5: ghi CSV ------------------------------------------------------
# newline="" cho Windows; utf-8-sig để Excel đọc đúng tiếng Việt.
with open(OUT, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(rows)
print(f"Xong: {len(rows)} job -> {OUT}")
