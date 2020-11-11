from src import finder, parser
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/search", methods=["POST"])
def search():
    if request.method == "POST":
        main_par = {
            "query": request.form["query"],
            "lan": request.form["lan"],
            "documents": request.form["documents"],
            "date": request.form["date"],
            "links": request.form["links"],
            "search_depth": request.form["search_depth"],
        }

        list_url_sites = parser.parse_search_url(main_par)
        html_data_site = parser.parse_html_site(list_url_sites)
        soup_data_site = parser.research_html_site(html_data_site)
        text_site = parser.get_data_text(soup_data_site)
        lines_text = finder.break_lines(text_site)
        stat_index = finder.find_query(lines_text, main_par)
        research_stat_index = finder.research_find_query(stat_index)
        sort_stat_index = finder.sort_find_query(research_stat_index)
        depth_stat_index = finder.depth_find_query(sort_stat_index, main_par)
        result_text = finder.get_text_index(depth_stat_index, lines_text)

        return render_template("result.html", data=result_text)


if __name__ == "__main__":
    app.run()
