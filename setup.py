from setuptools import setup
import shutil

setup(
    name="okdesk_api",
    version="0.0.0",
    packages=[
        "okdesk_api",
        "okdesk_api.api",
        "okdesk_api.api.issues",
        "okdesk_api.api.shared",
        "okdesk_api.api.contacts",
        "okdesk_api.api.companies",
        "okdesk_api.api.employees",
        "okdesk_api.api.agreements",
        "okdesk_api.api.maintenance_entities",
        "okdesk_api.types",
        "okdesk_api.client",
        "okdesk_api.errors",
        "okdesk_api.helpers",
    ],
    url="",
    license="",
    author="apepenkov",
    author_email="",
    description="",
)
