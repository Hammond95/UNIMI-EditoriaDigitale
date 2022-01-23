import re
import os
import shutil
import xml.etree.ElementTree as ET


if __name__ == "__main__":

    this_file_path = os.path.dirname(os.path.realpath(__file__))
    print(this_file_path)

    sources_path = os.path.abspath(
        os.path.expanduser(
            os.path.join(this_file_path + "/../ebook/")
        )
    )

    ebook_path = os.path.abspath(
        os.path.expanduser(
            os.path.join(this_file_path + "/../ebook/")
        )
    )

    template_file = None
    with open(os.path.join(this_file_path, "empty.html"), "r") as f:
        template_file = f.read()

    
    files_to_skip = ["00.html"]

    for root, dirs, files in os.walk(sources_path):
        for xfile in files:
            if xfile in files_to_skip:
                continue

            if xfile.endswith(".html"):
                print(os.path.join(root, xfile))
                
                html_data = None
                with open(os.path.join(root, xfile), "r") as inhtml:
                    html_data = inhtml.read()
                
                root_tree = ET.fromstring(
                    html_data
                        .replace("<br></br>", "<br/>")
                        .replace("<br>", "<br/>")
                )
                
                body = None
                for child in root_tree:
                    if child.tag == "{http://www.w3.org/1999/xhtml}body":
                        body = child
                        break
                
                for child in body:
                    body_value = ET.tostring(child, encoding="unicode", method="html").replace("html:", "").replace("xmlns:html=\"http://www.w3.org/1999/xhtml\"", "")
                    break

                # Move original to tmp to backup
                shutil.move(
                    os.path.join(ebook_path, xfile), 
                    "/tmp/{}".format(xfile)
                )

                # Removes all lines empty or with spaces only
                body_value = re.sub(r'^[\s]*\n', '', body_value, flags=re.MULTILINE)

                with open(os.path.join(ebook_path, xfile), "w") as out:
                    out.write(
                        template_file.format(bodycontent=body_value)
                    )

