import glob
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID, NUMERIC, DATETIME
from irclog2html.irclog2html import LogParser
import dateutil.parser

schema = Schema(nick=ID(stored=True), line=TEXT(stored=True),
                path=ID(stored=True), lineno=NUMERIC(stored=True),
                timestamp=DATETIME(stored=True)
)

idx = create_in("indexdir", schema)
writer = idx.writer()

for file in sorted(glob.glob("cloud/*.log")):
    print "adding",  file
    with open(file) as f:
        for idx, (ts, what, info) in enumerate(LogParser(f)):
            if what == LogParser.COMMENT:
                dt = dateutil.parser.parse(ts)
                nick, msg = info
                writer.add_document(
                    nick=nick, line=msg, path=unicode(file, 'utf-8'),
                    lineno=idx, timestamp=dt)

print "committing"
writer.commit()
