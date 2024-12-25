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

@app.route("/blog")
def blog():
    blog_dir = 'content/blog_posts'
    files = os.listdir(blog_dir)

    markdown_files = [f for f in files if f.endswith('.md')]

    markdown_files.sort(key=lambda f: os.path.getmtime(os.path.join(blog_dir, f)), reverse=True)
    
    if not markdown_files:
        return "No blog posts available", 404
    
    latest_file = markdown_files[0]
    latest_file_path = os.path.join(blog_dir, latest_file)
    
    with open(latest_file_path, 'r', encoding='utf-8') as file:
        markdown_content = file.read()

    with open(os.path.join('templates', 'blog_post_temp.html'), 'r') as file:
        blog_temp = file.read()

    html_content = blog_temp.replace("{{ blog_post_content }}", markdown.markdown(markdown_content))
    
    return flask.render_template_string(html_content)

if __name__ == '__main__':
    app.run("0.0.0.0", 8080)
