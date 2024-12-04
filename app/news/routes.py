import feedparser

from app.news import bp


@bp.route("/news/")
def fetchNews():
	feed = feedparser.parse(requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).content)
	return render_template('news.html', feed=feed)
