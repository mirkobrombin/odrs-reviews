import os
import sys
import requests
import webbrowser
from datetime import datetime


class ReviewModel:
    def __init__(self, app_id):
        self.app_id = app_id
        self.date_created = None
        self.description = None
        self.distro = None
        self.karma_down = None
        self.karma_up = None
        self.locale = None
        self.rating = None
        self.reported = None
        self.review_id = None
        self.summary = None
        self.user_display = None
        self.version = None

        if not os.path.exists('reviews'):
            os.makedirs(os.path.realpath('reviews'))

    def get_json(self):
        url = f"https://odrs.gnome.org/1.0/reviews/api/app/{self.app_id}"
        response = requests.get(url)
        return response.json()

    def get_reviews(self):
        json_reviews = self.get_json()
        reviews = []
        for review in json_reviews:
            review_model = ReviewModel(review['app_id'])
            review_model.date_created = self.parse_date(review['date_created'])
            review_model.description = review['description']
            review_model.distro = review['distro']
            review_model.karma_down = review['karma_down']
            review_model.karma_up = review['karma_up']
            review_model.locale = review['locale']
            review_model.rating = review['rating']
            review_model.reported = review['reported']
            review_model.review_id = review['review_id']
            review_model.summary = review['summary']
            review_model.user_display = review['user_display']
            review_model.version = review['version']

            reviews.append(review_model)

        return reviews

    @staticmethod
    def parse_date(date_created):
        date = datetime.fromtimestamp(int(date_created))
        return date.strftime('%Y-%m-%d %H:%M:%S')

    def get_reviews_html(self):
        reviews = self.get_reviews()
        html = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8">
                <title>Reviews for {self.app_id}</title>
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/uikit@3.7.1/dist/css/uikit.min.css" />
                <script src="https://cdn.jsdelivr.net/npm/uikit@3.7.1/dist/js/uikit.min.js"></script>
                <script src="https://cdn.jsdelivr.net/npm/uikit@3.7.1/dist/js/uikit-icons.min.js"></script>
            </head>
            <body>
                <div class="uk-container uk-container-large uk-padding">
                    <h1 class="uk-h1">Reviews for {self.app_id}</h1>
                    <p class="uk-text-lead">Reviews coming from ODRS.</p>"""

        for review in reviews:
            template = f"""
            <div class="uk-card uk-card-default uk-card-body">
                <table class="uk-table uk-table-divider uk-table-hover">
                <tr>
                    <th>Date Created</th>
                    <th>Distro</th>
                    <th>Karma</th>
                    <th>Locale</th>
                    <th>Rating</th>
                    <th>Reported</th>
                    <th>Review ID</th>
                    <th>Summary</th>
                    <th>User Name</th>
                    <th>Version</th>
                </tr>
                <tr>
                    <td>{review.date_created}</td>
                    <td>{review.distro}</td>
                    <td><span uk-icon="arrow-up"></span>{review.karma_up}/<span uk-icon="arrow-down"></span>{review.karma_down}</td>
                    <td>{review.locale}</td>
                    <td>{review.rating}</td>
                    <td>{review.reported}</td>
                    <td>{review.review_id}</td>
                    <td>{review.summary}</td>
                    <td>{review.user_display}</td>
                    <td>{review.version}</td>
                </tr>
                </table>
                <p class="uk-text-default">{review.description}</p>
            </div>
            <hr class="uk-divider-icon" />"""
            html += template

        html += '</div></body></html>'
        return html

    def generate_html_file(self):
        html = self.get_reviews_html()
        file_path = os.path.realpath(f"reviews/{self.app_id}.html")

        with open(f"{file_path}", 'w') as f:
            f.write(html)

        webbrowser.open(f"file://{file_path}")

    def generate_csv_file(self):
        reviews = self.get_reviews()
        file_path = os.path.realpath(f"reviews/{self.app_id}.csv")

        with open(f"{file_path}", 'w') as f:
            f.write(
                f"Date Created,Distro,Karma,Locale,Rating,Reported,Review ID,Summary,User Name,Version,Description\n")
            for review in reviews:
                f.write(f"{review.date_created},\
                    {review.distro},\
                    {review.karma_up},\
                    {review.locale},\
                    {review.rating},\
                    {review.reported},\
                    {review.review_id},\
                    {review.summary},\
                    {review.user_display},\
                    {review.version},\
                    {review.description}\n")

    def generate_table(self):
        reviews = self.get_reviews()
        table = ""
        for review in reviews:
            table += f"""
----------------------------------------------------------
\033[1m Review ID:\033[0m {review.review_id} 
\033[1m Date Created:\033[0m {review.date_created}
\033[1m Distro:\033[0m {review.distro}
\033[1m Display Name:\033[0m {review.user_display}
\033[1m Rating:\033[0m {review.rating}
\033[1m Summary:\033[0m {review.summary}
\033[1m Up/Down:\033[0m {review.karma_up}/{review.karma_down}
\033[1m Locale:\033[0m {review.locale}
\033[1m Reported:\033[0m {review.reported}
\033[1m Version:\033[0m {review.version}
\033[1m Description:\033[0m {review.description}"""
        return table

    def __str__(self):
        return 'ReviewModel: app_id: {}'.format(self.app_id)


def main():
    usage = 'Usage: python app.py <app_id> <output_type: csv, html, table>'
    if len(sys.argv) != 3:
        print(usage)
        sys.exit(1)

    app_id = sys.argv[1]
    output_type = sys.argv[2]

    if output_type not in ['html', 'csv', 'table']:
        print(usage)
        sys.exit(1)

    review_model = ReviewModel(app_id)

    if output_type == 'html':
        review_model.generate_html_file()
    elif output_type == 'table':
        print(review_model.generate_table())
    elif output_type == "csv":
        review_model.generate_csv_file()


if __name__ == '__main__':
    main()
