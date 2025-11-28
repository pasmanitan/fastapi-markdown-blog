from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import mistune
import os

markdown = mistune.create_markdown(escape=False)

router = APIRouter()

html_dir = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "../", "static", "html")
)

html_pages = Jinja2Templates(directory=f"{html_dir}")

blog_dir = os.path.normpath(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "../", "static", "markdown", "blog"
    )
)

markdown_path = Jinja2Templates(directory=f"{blog_dir}")


class BlogPost:
    def __init__(self, title: str, desc: str, date: str, slug: str, html: str):
        self.title = title
        self.desc = desc
        self.date = date
        self.slug = slug
        self.html = html


def post_split(post):
    pro = post.split("---", 1)
    pre = pro[1]
    sections = pre.split("---", 1)
    frontmatter = sections[0]
    content = sections[1]
    return frontmatter, content


def frontmatter_parse(frontmatter):
    frontmatter_contents = frontmatter.split(",", 3)
    pro_front = []
    for i in range(len(frontmatter_contents)):
        fc = frontmatter_contents[i]
        fs = fc.split(":", 1)
        fp = fs[1].strip()
        pro_front.append(fp)
    return pro_front


@router.get("/blog", response_class=HTMLResponse)
async def blog(request: Request):
    posts = []
    objs = []

    class PostData:
        def __init__(self, slug: str, title: str, date: str):
            self.slug = slug
            self.title = title
            self.date = date

    for file_path in os.listdir(blog_dir):
        if os.path.isfile(os.path.join(blog_dir, file_path)):
            posts.append(file_path)

    for i in posts:
        with open(f"{blog_dir}/{i}") as f:
            post = f.read()

        frontmatter = post_split(post)[0]
        p_f = frontmatter_parse(frontmatter)
        title, slug, date = p_f[0], p_f[1], p_f[2]
        postData = PostData(slug=slug, title=title, date=date)
        objs.append(postData)

    return html_pages.TemplateResponse(
        request=request,
        name="blog.html",
        context={"objs": objs},
    )


@router.get("/blog/{slug}", response_class=HTMLResponse)
async def blogpost(request: Request, slug: str):

    with open(f"{blog_dir}/{slug}.md") as f:
        post = f.read()

    frontmatter = post_split(post)[0]
    p_f = frontmatter_parse(frontmatter)
    title, slug, date, desc = p_f[0], p_f[1], p_f[2], p_f[3]
    content = post_split(post)[1]
    html = markdown(content)

    return html_pages.TemplateResponse(
        request=request,
        name="BlogPost.html",
        context={
            "title": title,
            "slug": slug,
            "date": date,
            "desc": desc,
            "html": html,
        },
    )
