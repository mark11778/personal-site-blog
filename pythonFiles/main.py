import flask
import geoip2.database
import os
import markdown

app = flask.Flask(__name__)
reader = geoip2.database.Reader(r'content/geolite/GeoLite2-City.mmdb')

@app.route("/")
def home():
    return flask.render_template("home.html")

@app.route("/resume")
def resume():
    user_ip = flask.request.remote_addr

    try:
        response = reader.city(user_ip)
        country = response.country.iso_code

        if country == 'US':
            return flask.send_file(r'content/resume/MarkRuzicka_UWMadison.pdf')
        else:
            return flask.send_file(r'content/resume/CV_Mark_Ruzicka.pdf')
    except geoip2.errors.AddressNotFoundError:
        return flask.send_file(r'content/resume/CV_Mark_Ruzicka.pdf')

@app.route("/blog", defaults={'post_name': None})
@app.route("/blog/<post_name>")
def blog(post_name):
    blog_dir = 'content/blog_posts'
    files = os.listdir(blog_dir)

    markdown_files = [f for f in files if f.endswith('.md')]

    markdown_files.sort(key=lambda f: os.path.getmtime(os.path.join(blog_dir, f)), reverse=True)
    
    if not markdown_files:
        return "No blog posts available", 404

    if post_name and f"{post_name}.md" in markdown_files:
        selected_file = f"{post_name}.md"
    else:
        selected_file = markdown_files[0]  

    selected_file_path = os.path.join(blog_dir, selected_file)
    
    with open(selected_file_path, 'r', encoding='utf-8') as file:
        markdown_content = file.read()

    with open(os.path.join('templates', 'blog_post_temp.html'), 'r') as file:
        blog_temp = file.read()

    blog_links = ''.join(
        f'<li><a href="/blog/{os.path.splitext(f)[0]}">{os.path.splitext(f)[0]}</a></li>'
        for f in markdown_files
    )

    html_content = blog_temp.replace("{{ blog_post_content }}", markdown.markdown(markdown_content))
    html_content = html_content.replace("{{ blog_post_links }}", blog_links)
    
    return flask.render_template_string(html_content)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=False)
