import shutil
import pytest
import requests
import zipfile
import os
from selene import browser, query


os.makedirs('content_folder', exist_ok=True)
CONTENT_DIR = os.path.abspath('content_folder')

def download_csv():
    browser.open("https://itsm365.com/documents_rus/web/Content/import/import_org_file.htm")
    download_url = browser.element("[href='../Resources/doc/import_ou_csv.csv']").get(query.attribute("href"))

    content = requests.get(url=download_url).content

    file_path = os.path.join(CONTENT_DIR, 'csv')
    with open(file_path, "wb") as file:
        file.write(content)

def download_xlsx():
    browser.open("https://itsm365.com/documents_rus/web/Content/import/import_org_file.htm")
    download_url = browser.element("[href='../Resources/doc/import_ou_xlsx.xlsx']").get(query.attribute("href"))

    content = requests.get(url=download_url).content

    file_path = os.path.join(CONTENT_DIR, 'xlsx')
    with open(file_path, "wb") as file:
        file.write(content)

def download_pdf():
    browser.open("http://ru.wondershare.com/pdf-editor/form-templates.html")
    download_url = browser.element("[href='http://images.ru.wondershare.com/images/pdf-files/"
                                   "Commercial_Invoice.pdf']").get(query.attribute("href"))

    content = requests.get(url=download_url).content

    file_path = os.path.join(CONTENT_DIR, 'pdf')
    with open(file_path, "wb") as file:
        file.write(content)

def create_archive():
    ARCHIVE_DIR = os.path.join(CONTENT_DIR, 'archive_folder')
    if not os.path.exists(ARCHIVE_DIR):
        os.mkdir(ARCHIVE_DIR)
#
    with (zipfile.ZipFile(os.path.join(ARCHIVE_DIR, 'archive.zip'), 'w') as zf):
        for file in os.listdir(CONTENT_DIR):
            zf.write(os.path.join(CONTENT_DIR, file), file)


@pytest.fixture(scope="session", autouse=True)
def setup_files():
    download_csv()
    download_xlsx()
    download_pdf()
    create_archive()

    yield

    shutil.rmtree(CONTENT_DIR)