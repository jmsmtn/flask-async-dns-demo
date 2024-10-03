import asyncio

from flask import Flask
from flask import render_template, Response

import dns.asyncquery
import dns.asyncresolver
import dns.message

app = Flask(__name__)

DOMAINS = [
    "dmarcian.com",
    "fly.io",
    "google.com",
    "googleapis.com",
    "root-servers.net",
    "apple.com",
    "gstatic.com",
    "facebook.com",
    "tiktokcdn.com",
    "microsoft.com",
]


@app.route("/")
async def hello_world():
    queries = [dns.message.make_query(f"_dmarc.{domain}", "TXT") for domain in DOMAINS]
    tasks = [dns.asyncquery.udp(query, "1.1.1.1") for query in queries]

    dns_results = await asyncio.gather(*tasks)
    results = []

    for result in dns_results:
        if result.answer:
            results.append((str(result.question[0]), str(result.answer[0])))
        else:
            results.append((str(result.question[0]), str(result.answer)))

    return Response(
        render_template("demo.html", results=tuple(results)), content_type="text/html"
    )
