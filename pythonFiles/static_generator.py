import os
import markdown
from jinja2 import Template

# Define paths
output_dir = 'static_site'
blog_dir = 'content/blog_posts'
template_dir = 'templates'

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Read and render the home page
with open(os.path.join(template_dir, 'home.html'), 'r') as file:
    home_content = file.read()

with open(os.path.join(output_dir, 'index.html'), 'w') as file:
    file.write(home_content)

# Read and render the resume page
resume_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume</title>
</head>
<body>
    <h1>Resume</h1>
    <p>Download the resume from the original site.</p>
</body>
</html>
"""

with open(os.path.join(output_dir, 'resume.html'), 'w') as file:
    file.write(resume_content)

# Read and render the blog posts
with open(os.path.join(template_dir, 'blog_post_temp.html'), 'r') as file:
    blog_template_content = file.read()

blog_template = Template(blog_template_content)

# List markdown files
markdown_files = [f for f in os.listdir(blog_dir) if f.endswith('.md')]
markdown_files.sort(key=lambda f: os.path.getmtime(os.path.join(blog_dir, f)), reverse=True)

# Generate blog post pages
for markdown_file in markdown_files:
    post_name = os.path.splitext(markdown_file)[0]
    with open(os.path.join(blog_dir, markdown_file), 'r', encoding='utf-8') as file:
        markdown_content = file.read()

    html_content = markdown.markdown(markdown_content)
    blog_links = ''.join(
        f'<li><a href="{os.path.splitext(f)[0]}.html">{os.path.splitext(f)[0]}</a></li>'
        for f in markdown_files
    )

    rendered_content = blog_template.render(
        blog_post_content=html_content,
        blog_post_links=blog_links
    )

    with open(os.path.join(output_dir, f'{post_name}.html'), 'w') as file:
        file.write(rendered_content)

# Generate a main blog page
blog_index_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog</title>
</head>
<body>
    <h1>Blog</h1>
    <ul>
"""

for markdown_file in markdown_files:
    post_name = os.path.splitext(markdown_file)[0]
    blog_index_content += f'<li><a href="{post_name}.html">{post_name}</a></li>\n'

blog_index_content += """
    </ul>
</body>
</html>
"""

with open(os.path.join(output_dir, 'blog.html'), 'w') as file:
    file.write(blog_index_content)