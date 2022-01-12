import os
import xml.etree.ElementTree as ET


if __name__ == "__main__":

    this_file_path = os.path.dirname(os.path.realpath(__file__))
    print(this_file_path)

    sources_path = os.path.abspath(
        os.path.expanduser(
            os.path.join(this_file_path + "/../sources/")
        )
    )
    print(sources_path)

    oebps_path = os.path.abspath(
        os.path.expanduser(
            os.path.join(this_file_path + "/../sources/OEBPS/")
        )
    )

    ebook_path = os.path.abspath(
        os.path.expanduser(
            os.path.join(this_file_path + "/../ebook/")
        )
    )

    template_file = None
    with open(os.path.join(sources_path, "empty.html"), "r") as f:
        template_file = f.read()

    for root, dirs, files in os.walk(oebps_path):
        for xfile in files:
            if xfile.endswith(".html"):
                print(os.path.join(root, xfile))
                extracted_filenum = int(xfile.split("-")[2].split(".")[0])
                
                html_data = None
                with open(os.path.join(root, xfile), "r") as inhtml:
                    html_data = inhtml.read()
                
                root_tree = ET.fromstring(html_data)
                
                body = None
                for child in root_tree:
                    if child.tag == "{http://www.w3.org/1999/xhtml}body":
                        body = child
                        break
                
                for child in body:
                    body_value = ET.tostring(child, encoding="unicode", method="html").replace("html:", "").replace("xmlns:html=\"http://www.w3.org/1999/xhtml\"", "")
                    break

                out_filename = "{:02d}.html".format(extracted_filenum + 2)
                with open(os.path.join(ebook_path, out_filename), "w") as out:
                    out.write(
                        template_file.format(bodycontent=body_value)
                    )

